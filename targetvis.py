from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astropy import units as u
from datetime import datetime, timedelta
from ephem import Observer, FixedBody, degrees
import numpy as np      

def resolve_source(name):
   """For a given source name, use astroquery to find its coordinates"""
   try:
      query = Simbad.query_object(name)
      ra = query['RA'][0]
      dec= query['DEC'][0]
      coord = SkyCoord('{} {}'.format(ra, dec), unit=(u.hourangle, u.deg))
   except:
      return None
   return coord.to_string('hmsdms')

def findTargetElevation(coord, obsDate):
   """For a given date and coordinate, find the elevation of the source every
      10 mins. Return both the datetime object array and the elevation array"""
   # Find the start and the end times
   d = obsDate.split('-')
   startTime = datetime(int(d[0]), int(d[1]), int(d[2]), 0, 0, 0)
   endTime   = startTime + timedelta(days=1)
   # Get a list of values along the time axis
   xaxis = []
   xaxis.append(startTime)
   tempTime = startTime
   while(tempTime < endTime):
      xaxis.append(tempTime)
      tempTime += timedelta(minutes=10)
   
   # Create the telescope object
   # LOFAR coordinates were taken from Aleksandar's code
   lofar = Observer()
   lofar.lon = '6.869882'
   lofar.lat = '52.915129'
   lofar.elevation = 15.
   
   # Create a target object
   target = FixedBody()
   target._epoch = '2000'
   try:
      coordTarget = SkyCoord(coord)
   except:
      return None, None
   target._ra = coordTarget.ra.radian
   target._dec= coordTarget.dec.radian
   
   # Iterate over each time interval and estimate the elevation of the target
   yaxis = []
   for item in xaxis:
      lofar.date = item
      target.compute(lofar)
      yaxis.append( float(target.alt)*180./np.pi )
   
   return xaxis, yaxis
