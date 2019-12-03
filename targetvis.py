from datetime import datetime, timedelta
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astropy import units as u
from ephem import Observer, FixedBody
import numpy as np      
from plotly.graph_objs import Scatter, Layout

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

# FWHM of HBA tile beam in deg
tile_beam_size = 20

# TODO: FWHM of LBA dipole beam in deg

def getStationBeamSize(nCore, nRemote, nInt, antenna_mode):
   """Return FWHM of station beam for a given antenna list and array mode"""
   # FWHM of station beams in deg
   corefwhm =   {'lba':5.16, 'hba':3.80}
   remotefwhm = {'lba':5.16, 'hba':2.85}
   intfwhm =    {'lba':6.46, 'hba':2.07}
   if 'lba' in antenna_mode:
      mode = 'lba'
      station_beam = corefwhm[mode]
   else:
      mode = 'hba'
      if nInt > 0:
         station_beam = intfwhm[mode]
      elif nRemote > 0 and 'inner' not in antenna_mode:
         # Antenna set is untapered remote station
         station_beam = remotefwhm[mode]
      else:
         # Antenna set is either just the core or core + tapered remote
         station_beam = corefwhm[mode]
   return station_beam

def getTileBeam(coord):
   """Returns the midpoint between the different pointings in coord.
      If coord has one item, midpoint is the same as that item.
      Note that the midpoint on the sky for large angular separation 
      is ill-defined. In our case, it is almost always within ~7 degrees
      and so this should be fine. For more details, see 
      https://github.com/astropy/astropy/issues/5766"""
   tempRA = 0.
   tempDec= 0.
   nBeams = len(coord)
   for c in coord:
      this_coord = SkyCoord(c)
      tempRA += this_coord.ra.degree
      tempDec+= this_coord.dec.degree
   t_beam = SkyCoord(tempRA/nBeams, tempDec/nBeams, unit=u.deg)
   return t_beam

def getAxesRange(layout):
   """For a given layout dict, find the axes limits"""
   xmin = 0.
   ymin = 0.
   xmax = 0.
   ymax = 0.
   temp_xmin = []; temp_ymin = []
   temp_xmax = []; temp_ymax = []
   for item in layout['shapes']:
      temp_xmin.append(item['x0'])
      temp_xmax.append(item['x1'])
      temp_ymin.append(item['y0'])
      temp_ymax.append(item['y1'])
   xmin = int(np.min(temp_xmin))
   xmax = int(np.max(temp_xmax))
   ymin = int(np.min(temp_ymin))
   ymax = int(np.max(temp_ymax))
   return xmin, xmax, ymin, ymax

def findBeamLayout(srcName, coord, nCore, nRemote, nInt, antenna_mode):
   """For a given set of source coordinates, station list, and array mode,
      generate a plotly Data object for the dipole/tile/station beams"""
   srcNameList = srcName.split(',')
   coordList = coord.split(',')
   station_beam_size = getStationBeamSize(nCore, nRemote, nInt, antenna_mode)/2
   # Create an initial layout and data object
   layout = {'shapes': [], 
             'xaxis':{'title':'Right Ascension (degree)'}, 
             'yaxis':{'title':'Declination (degree)'},
             'title':'Beam layout',
             'showlegend': False
            }
   data = []
   
   LABEL_OFFSET = 0.5
   
   # Iterate over coord and plot the station beam
   index = 0
   for c in coordList:
      s_beam = SkyCoord(c)
      layout['shapes'].append(
         {
         'type':'circle',
         'xref':'x',
         'yref':'y',
         'x0': s_beam.ra.deg-station_beam_size,
         'x1': s_beam.ra.deg+station_beam_size,
         'y0': s_beam.dec.deg-station_beam_size,
         'y1': s_beam.dec.deg+station_beam_size,
         'line': {'color':'rgba(50, 171, 96, 1)'}            
         }
      )
      data.append(
        Scatter(x=[s_beam.ra.deg], 
                y=[s_beam.dec.deg+station_beam_size+LABEL_OFFSET],
                text=[srcNameList[index]], 
                mode='text'
        )
      )
      index += 1
      
   # If antenna_mode is hba, plot the tile beam
   if 'hba' in antenna_mode:   
      # Calculate the reference tile beam 
      t_beam = getTileBeam(coordList)
      layout['shapes'].append(
         {
         'type':'circle',
         'xref':'x',
         'yref':'y',
         'x0': t_beam.ra.deg-tile_beam_size/2,
         'x1': t_beam.ra.deg+tile_beam_size/2,
         'y0': t_beam.dec.deg-tile_beam_size/2,
         'y1': t_beam.dec.deg+tile_beam_size/2,
         'line': {'color':'rgba(250, 0, 250, 1)'}            
         }
      )
      data.append( 
        Scatter(x=[t_beam.ra.deg], 
                y=[t_beam.dec.deg+tile_beam_size/2 + LABEL_OFFSET],
                text=['Station beam'], 
                mode='text'
        ) 
      )
   
   # Set the axes range to display
   bufsize = 2 # Buffer space in degrees
   xmin, xmax, ymin, ymax = getAxesRange(layout)
   # Swap xmin and xmax so that declination decreases to the right.
   layout['xaxis']['range'] = [xmax+bufsize,xmin-bufsize]
   layout['yaxis']['range'] = [ymin-bufsize,ymax+bufsize]
   return {'layout': layout, 'data':data}

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
      # Convert the list to a comma separated list before returning
      retString = ','.join(retString)
   except:
      retString = None
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
      coord_target = SkyCoord(coord[i])
      target._ra = coord_target.ra.radian
      target._dec= coord_target.dec.radian
   
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
