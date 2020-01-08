from datetime import datetime, timedelta
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astropy import units as u
from ephem import Observer, FixedBody, Sun, Moon, Jupiter
import numpy as np      
import csv
from plotly.graph_objs import Scatter, Layout
from plotly.graph_objects import Table

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
                text=['Tile beam'], 
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

def resolve_lotss_source(name):
   """Check if a given source name is a LoTSS pointing? If it is, return its 
      coordinates in (hourangle, deg) units. Else, return None."""
   coord = None
   with open('lotss_pointings.txt', newline='\n') as f:
      text = f.readlines()
      for line in text:
         if name == line.split()[0]:
            coord = {'RA':[line.split()[3]], 'DEC':[line.split()[4]]}
            break
   return coord

def resolve_source(names):
   """For a given source name, use astroquery to find its coordinates.
      The source name can be a single source or a comma separated list."""
   retString = []
   try:
      for name in names.split(','):
         query = Simbad.query_object(name)
         if query is None:
            # Source is not a valid Simbad object. Is it a LoTSS pointing?
            query = resolve_lotss_source(name)
         ra = query['RA'][0]
         dec= query['DEC'][0]
         coord = SkyCoord('{} {}'.format(ra, dec), unit=(u.hourangle, u.deg))
         retString.append( coord.to_string('hmsdms') )
      # Convert the list to a comma separated list before returning
      retString = ','.join(retString)
   except:
      retString = None
   return retString

def findTargetElevation(srcName, coord, obsDate, nInt):
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
      tempTime += timedelta(minutes=5)
   
   # Create the telescope object
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
         elevation = float(target.alt)*180./np.pi
         if elevation < 0:
            elevation = np.nan
         yaxis.append(elevation)
      
      # Create a Plotly Scatter object that can be plotted later
      retData.append( Scatter(x=xaxis, y=yaxis, mode='lines', 
                               line={}, name=srcNameList[i] ) )
   # We should also plot Sun, Moon, and Jupiter by default
   sun = Sun()
   sun._epoch = '2000'
   yaxis = []
   for item in xaxis:
      lofar.date = item
      sun.compute(lofar)
      elevation = float(sun.alt)*180./np.pi
      if elevation < 0:
         elevation = np.nan
      yaxis.append(elevation)
   retData.append( Scatter(x=xaxis, y=yaxis, mode='lines',
                           line={}, name='Sun') )

   moon = Moon()
   yaxis = []
   for item in xaxis:
      lofar.date = item
      moon.compute(lofar)
      elevation = float(moon.alt)*180./np.pi
      if elevation < 0:
         elevation = np.nan
      yaxis.append(elevation)
   retData.append( Scatter(x=xaxis, y=yaxis, mode='lines',
                           line={}, name='Moon') )

   jupiter = Jupiter()
   yaxis = []
   for item in xaxis:
      lofar.date = item
      jupiter.compute(lofar)
      elevation = float(jupiter.alt)*180./np.pi
      if elevation < 0:
         elevation = np.nan
      yaxis.append(elevation)
   retData.append( Scatter(x=xaxis, y=yaxis, mode='lines',
                           line={}, name='Jupiter') )
   return retData

def addSunRiseAndSetTimes(obsDate, nInt, elevationFig):
   """
   For a given obsDate, find the sun rise and set times. Add these to the supplied 
   elevationFig and return the modified elevationFig.
   """
   d = obsDate.split('-')
   startTime = datetime(int(d[0]), int(d[1]), int(d[2]), 0, 0, 0)
   sun = Sun()
   sun._epoch = '2000'
   if nInt == 0:
      # Only Dutch array is being used. Calculate Sun rise and set times in NL
      lofar = Observer()
      lofar.lon = '6.869882'
      lofar.lat = '52.915129'
      lofar.elevation = 15.
      lofar.date = startTime
      sun_rise = lofar.next_rising(sun).datetime()
      sun_set = lofar.next_setting(sun).datetime()
      # Define a 1 hour window around Sun rise and Sun set.
      sun_rise_beg = sun_rise - timedelta(minutes=30) 
      sun_rise_end = sun_rise + timedelta(minutes=30)
      sun_set_beg = sun_set - timedelta(minutes=30)
      sun_set_end = sun_set + timedelta(minutes=30)
   else:
      # Calculate sun rise and set times using Latvian and Irish stations
      lv = Observer()
      lv.lon = '21.854916'
      lv.lat = '57.553493'
      lv.date = startTime
      ie = Observer()
      ie.lon = '-7.921790'
      ie.lat = '53.094967'
      ie.date = startTime
      lv_sun_rise = lv.next_rising(sun).datetime()
      lv_sun_set = lv.next_setting(sun).datetime()
      ie_sun_rise = ie.next_rising(sun).datetime()
      ie_sun_set = ie.next_setting(sun).datetime()
      # Define a window around sun rise and sun set.
      sun_rise_beg = lv_sun_rise - timedelta(minutes=30)
      sun_rise_end = ie_sun_rise + timedelta(minutes=30)
      sun_set_beg = lv_sun_set - timedelta(minutes=30)
      sun_set_end = ie_sun_set + timedelta(minutes=30)
   # Add to elevationFig
   elevationFig['layout']['shapes'].append({
      'type': "rect",
      'xref': 'x',
      'yref': 'y',
      'x0'  : sun_rise_beg,
      'x1'  : sun_rise_end,
      'y0'  : 0,
      'y1'  : 90,
      'fillcolor': 'LightSkyBlue',
      'opacity': 0.4,
      'line': {'width': 0,}
   })
   elevationFig['layout']['shapes'].append({
      'type': "rect",
      'xref': 'x',
      'yref': 'y',
      'x0'  : sun_set_beg,
      'x1'  : sun_set_end,
      'y0'  : 0,
      'y1'  : 90,
      'fillcolor': 'LightSkyBlue',
      'opacity': 0.4,
      'line': {'width': 0,}
   })      
   return elevationFig

def getDistanceSolar(target, obsDate, offender):
   """Compute the angular distance in degrees between the specified target and 
      the offending radio source in the solar system on the specified observing date. 
      Input parameters:
      * target   - Coordinate of the target as an Astropy SkyCoord object
      * obsDate  - Observing date in datetime.datetime format
      * offender - Name of the offending bright source. Allowed values are
                   Sun, Moon, Jupiter.
      Returns:
      For Moon, the minimum and maximum separation are returned. For others, 
      distance,None is returned."""
   # Get a list of values along the time axis
   d = obsDate.split('-')
   startTime = datetime(int(d[0]), int(d[1]), int(d[2]), 0, 0, 0)
   endTime = startTime + timedelta(hours=24)
   taxis = []
   tempTime = startTime
   while(tempTime < endTime):
      taxis.append(tempTime)
      tempTime += timedelta(hours=1)
   angsep = []
   if offender == 'Sun':
      obj = Sun()
   elif offender == 'Moon':
      obj = Moon()
   elif offender == 'Jupiter':
      obj = Jupiter()
   else: pass
   # Estimate the angular distance over the entire time axis
   for time in taxis:
      obj.compute(time)
      coord = SkyCoord('{} {}'.format(obj.ra, obj.dec), unit=(u.hourangle, u.deg))
      angsep.append(coord.separation(target).deg)
   # Return appropriate result
   if offender == 'Moon':
      return np.min(angsep), np.max(angsep)
   else:
      return np.mean(angsep), None

def makeDistanceTable(srcNameInput, coordInput, obsDate):
   """Generate a plotly Table showing the distances between user-specified 
      targets and a few offending sources"""
   srcNameList = srcNameInput.split(',')
   coordList = coordInput.split(',')
   col_names = ['Sources']+srcNameList
   header = {
      'values': col_names,
      'font'  : {'size':12, 'color':'white'},
      'align' : 'left',
      'fill_color': 'grey',
      'line_color': 'darkslategray'
   }
   col_values = [['CasA', 'CygA', 'TauA', 'VirA', 'Sun', 'Moon(min,max)', 'Jupiter']]
   
   # Iterate through each source and compute the distances
   for idx, target in enumerate(srcNameList):
      # Get the coordinate of this target
      t_coord = SkyCoord(coordList[idx])
      # CasA
      s_coord = SkyCoord(ateam_coordinates['CasA'])
      d_casa = s_coord.separation(t_coord).deg
      # CygA
      s_coord = SkyCoord(ateam_coordinates['CygA'])
      d_cyga = s_coord.separation(t_coord).deg
      # TauA
      s_coord = SkyCoord(ateam_coordinates['TauA'])
      d_taua = s_coord.separation(t_coord).deg
      # VirA
      s_coord = SkyCoord(ateam_coordinates['VirA'])
      d_vira = s_coord.separation(t_coord).deg
      # Sun
      d_sun, _ = getDistanceSolar(t_coord, obsDate, 'Sun')
      # Moon
      d_moon_min, d_moon_max = getDistanceSolar(t_coord, obsDate, 'Moon')
      # Jupiter
      d_jupiter, _ = getDistanceSolar(t_coord, obsDate, 'Jupiter')
      # Consolidate all into a list
      this_row = ['{:0.2f}'.format(d_casa), 
                  '{:0.2f}'.format(d_cyga), 
                  '{:0.2f}'.format(d_taua), 
                  '{:0.2f}'.format(d_vira), 
                  '{:0.2f}'.format(d_sun), 
                  '{:0.2f},{:0.2f}'.format(d_moon_min, d_moon_max),
                  '{:0.2f}'.format(d_jupiter)]
      # Add this row to the col_values table
      col_values.append(this_row)
   
   tab = Table(
            header=header,
            cells=dict(values=col_values, align='left')
         )
   return tab
