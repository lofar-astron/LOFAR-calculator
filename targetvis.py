from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astropy import units as u
from datetime import datetime, timedelta
from ephem import Observer, FixedBody, degrees
import numpy as np      
from plotly.graph_objs import Scatter, Data

# Define coordinates of calibrators
calib_coordinates = {
                       '3C48' :'01h37m41.2994s +33d09m35.134s',
                       '3C196':'08h13m36.033s +48d13m02.56s',
                       '3C295':'14h11m20.519s +52d12m09.97s',
                       '3C147':'05h42m36.1379s +49d51m07.234s' 
                    }

# Define coordinates of A-team sources
ateam_coordinates = {
                       'CygA' :'19h59m28.3566s +40d44m02.096s',
                       'CasA':'23h23m24.000s +58d48m54.00s',
                       'TauA':'05h34m31.94s +22d00m52.2s',
                       'VirA':'12h30m49.4233s +12d23m28.043s' 
                    }

def resolve_source(names):
   """For a given source name, use astroquery to find its coordinates.
      The source name can be a single source or a comma separated list."""
   retString = []
   try:
      for name in names.split(','):
         query = Simbad.query_object(name)
         ra = query['RA'][0]
         dec= query['DEC'][0]
         coord = SkyCoord('{} {}'.format(ra, dec), unit=(u.hourangle, u.deg))
         retString.append( coord.to_string('hmsdms') )
   except:
      return None
   return retString

def findTargetElevation(srcName, coord, obsDate):
   """For a given date and coordinate, find the elevation of the source every
      10 mins. Return both the datetime object array and the elevation array"""
   # Find the start and the end times
   d = obsDate.split('-')
   startTime = datetime(int(d[0]), int(d[1]), int(d[2]), 0, 0, 0)
   endTime   = startTime + timedelta(days=1)
   # Get a list of values along the time axis
   xaxis = []
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
   retData = []
   srcNameList = srcName.split(',')
   for i in range(len(coord)):
      target = FixedBody()
      target._epoch = '2000'
      coordTarget = SkyCoord(coord[i])
      target._ra = coordTarget.ra.radian
      target._dec= coordTarget.dec.radian
   
      # Iterate over each time interval and estimate the elevation of the target
      yaxis = []
      for item in xaxis:
         lofar.date = item
         target.compute(lofar)
         yaxis.append( float(target.alt)*180./np.pi )
      
      # Create a Plotly Scatter object that can be plotted later
      retData.append( Scatter(x=xaxis, y=yaxis, mode='lines', 
                               line={}, name=srcNameList[i] ) )
   
   return retData
