"""Functions and constants for target visibility calculations"""

from datetime import datetime, timedelta
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astropy import units as u
from ephem import Observer, FixedBody, Sun, Moon, Jupiter
import numpy as np
from plotly.graph_objs import Scatter
from plotly.graph_objects import Table

# Define coordinates of calibrators
CALIB_COORDINATES = {
    '3C48' :'01h37m41.2994s +33d09m35.134s',
    '3C196':'08h13m36.033s +48d13m02.56s',
    '3C295':'14h11m20.519s +52d12m09.97s',
    '3C147':'05h42m36.1379s +49d51m07.234s'
    }

# Define coordinates of A-team sources
ATEAM_COORDINATES = {
    'CygA':'19h59m28.3566s +40d44m02.096s',
    'CasA':'23h23m24.000s +58d48m54.00s',
    'TauA':'05h34m31.94s +22d00m52.2s',
    'VirA':'12h30m49.4233s +12d23m28.043s'
    }

# FWHM of HBA tile beam in deg
TILE_BEAM_SIZE = 20

# TODO: FWHM of LBA dipole beam in deg

def get_dutch_lofar_object():
    """Return an ephem.Observer() object with details containing the Dutch
       Lofar array"""
    lofar = Observer()
    lofar.lon = '6.869882'
    lofar.lat = '52.915129'
    lofar.elevation = 15.
    return lofar

def get_lv_lofar_object():
    """Return an ephem.Observer() object with details containing the LV station"""
    lv = Observer()
    lv.lon = '21.854916'
    lv.lat = '57.553493'
    return lv

def get_ie_lofar_object():
    """Return an ephem.Observer() object with details containing the IE station"""
    ie = Observer()
    ie.lon = '-7.921790'
    ie.lat = '53.094967'
    return ie

def get_station_beam_size(n_core, n_remote, n_int, antenna_mode):
    """Return FWHM of station beam for a given antenna list and array mode"""
    # FWHM of station beams in deg
    corefwhm = {'lba':5.16, 'hba':3.80}
    remotefwhm = {'lba':5.16, 'hba':2.85}
    intfwhm = {'lba':6.46, 'hba':2.07}
    if 'lba' in antenna_mode:
        mode = 'lba'
        station_beam = corefwhm[mode]
    else:
        mode = 'hba'
        if n_int > 0:
            station_beam = intfwhm[mode]
        elif n_remote > 0 and 'inner' not in antenna_mode:
            # Antenna set is untapered remote station
            station_beam = remotefwhm[mode]
        else:
            # Antenna set is either just the core or core + tapered remote
            station_beam = corefwhm[mode]
    return station_beam

def get_tile_beam(coord):
    """Returns the midpoint between the different pointings in coord.
       If coord has one item, midpoint is the same as that item.
       Note that the midpoint on the sky for large angular separation
       is ill-defined. In our case, it is almost always within ~7 degrees
       and so this should be fine. For more details, see
       https://github.com/astropy/astropy/issues/5766"""
    temp_ra = 0.
    temp_dec = 0.
    n_beams = len(coord)
    for c in coord:
        this_coord = SkyCoord(c)
        temp_ra += this_coord.ra.degree
        temp_dec += this_coord.dec.degree
    temp_ra=(temp_ra+180)%(360)-180 # fix a problem near 24h/0h
    t_beam = SkyCoord(temp_ra/n_beams, temp_dec/n_beams, unit=u.deg)
    return t_beam

def get_axes_range(layout):
    """For a given layout dict, find the axes limits"""
    xmin = 0.
    ymin = 0.
    xmax = 0.
    ymax = 0.
    temp_xmin = []
    temp_ymin = []
    temp_xmax = []
    temp_ymax = []
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

def find_beam_layout(src_name, coord, n_core, n_remote, n_int, antenna_mode):
    """For a given set of source coordinates, station list, and array mode,
       generate a plotly Data object for the dipole/tile/station beams"""
    src_name_list = src_name.split(',')
    coord_list = coord.split(',')
    station_beam_size = get_station_beam_size(n_core, n_remote,
                                              n_int, antenna_mode)/2
    # Create an initial layout and data object
    layout = {'shapes': [],
              'xaxis':{'title':'Right Ascension (degree)'},
              'yaxis':{'title':'Declination (degree)'},
              'title':'Beam layout',
              'showlegend': False
             }
    data = []

    label_offset = 0.5
    # Iterate over coord and plot the station beam
    # 23h40m +72d, 0h20m +72d
    index = 0
    s_beams = [SkyCoord(c) for c in coord_list]
    # check if we're crossing zero degrees
    s_ras = [s_beam.ra.deg for s_beam in s_beams]
    crossing_zero_degrees=False
    if np.max(np.abs(np.diff(s_ras))) > 50:
        crossing_zero_degrees=True
    for s_beam in s_beams:#c in coord_list:
        #s_beam = SkyCoord(c)
        layout['shapes'].append({
            'type':'circle',
            'xref':'x',
            'yref':'y',
            'x0': s_beam.ra.deg-station_beam_size,
            'x1': s_beam.ra.deg+station_beam_size,
            'y0': s_beam.dec.deg-station_beam_size,
            'y1': s_beam.dec.deg+station_beam_size,
            'line': {'color':'rgba(50, 171, 96, 1)'}
        })
        if crossing_zero_degrees:
            if s_beam.ra.deg>180:
                layout['shapes'].append({
                    'type':'circle',
                    'xref':'x',
                    'yref':'y',
                    'x0': (s_beam.ra.deg-station_beam_size+180)%360-180,
                    'x1': (s_beam.ra.deg+station_beam_size+180)%360-180,
                    'y0': s_beam.dec.deg-station_beam_size,
                    'y1': s_beam.dec.deg+station_beam_size,
                    'line': {'color':'rgba(50, 171, 96, 1)'}
                })
                data.append(
                Scatter(x=[(s_beam.ra.deg+180)%360-180],
                    y=[s_beam.dec.deg+station_beam_size+label_offset],
                    text=[src_name_list[index]],
                    mode='text')
                )
            else:
                layout['shapes'].append({
                    'type':'circle',
                    'xref':'x',
                    'yref':'y',
                    'x0': (s_beam.ra.deg-station_beam_size-180)%360+180,
                    'x1': (s_beam.ra.deg+station_beam_size-180)%360+180,
                    'y0': s_beam.dec.deg-station_beam_size,
                    'y1': s_beam.dec.deg+station_beam_size,
                    'line': {'color':'rgba(50, 171, 96, 1)'}
                })
                data.append(
                Scatter(x=[(s_beam.ra.deg-180)%360+180],
                    y=[s_beam.dec.deg+station_beam_size+label_offset],
                    text=[src_name_list[index]],
                    mode='text')
                )

        data.append(
            Scatter(x=[s_beam.ra.deg],
                    y=[s_beam.dec.deg+station_beam_size+label_offset],
                    text=[src_name_list[index]],
                    mode='text')
        )
        index += 1

    # If antenna_mode is hba, plot the tile beam
    if 'hba' in antenna_mode:
        # Calculate the reference tile beam
        t_beam = get_tile_beam(coord_list)
        layout['shapes'].append({
            'type':'circle',
            'xref':'x',
            'yref':'y',
            'x0': t_beam.ra.deg-TILE_BEAM_SIZE/2,
            'x1': t_beam.ra.deg+TILE_BEAM_SIZE/2,
            'y0': t_beam.dec.deg-TILE_BEAM_SIZE/2,
            'y1': t_beam.dec.deg+TILE_BEAM_SIZE/2,
            'line': {'color':'rgba(250, 0, 250, 1)'}
        })
        if crossing_zero_degrees:
            if t_beam.ra.deg > 180:
                t_offset=-360
            else:
                t_offset=360
            layout['shapes'].append({
            'type':'circle',
            'xref':'x',
            'yref':'y',
            'x0': t_beam.ra.deg-TILE_BEAM_SIZE/2+t_offset,
            'x1': t_beam.ra.deg+TILE_BEAM_SIZE/2+t_offset,
            'y0': t_beam.dec.deg-TILE_BEAM_SIZE/2,
            'y1': t_beam.dec.deg+TILE_BEAM_SIZE/2,
            'line': {'color':'rgba(250, 0, 250, 1)'}
            })

        data.append(
            Scatter(x=[t_beam.ra.deg],
                    y=[t_beam.dec.deg+TILE_BEAM_SIZE/2 + label_offset],
                    text=['Tile beam'],
                    mode='text')
        )

    # Set the axes range to display
    bufsize = 2 # Buffer space in degrees
    xmin, xmax, ymin, ymax = get_axes_range(layout)
    # Swap xmin and xmax so that declination decreases to the right.
    layout['xaxis']['range'] = [xmax+bufsize, xmin-bufsize]
    layout['yaxis']['range'] = [ymin-bufsize, ymax+bufsize]
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
    return_string = []
    try:
        for name in names.split(','):
            query = Simbad.query_object(name)
            if query is None:
                # Source is not a valid Simbad object. Is it a LoTSS pointing?
                query = resolve_lotss_source(name)
            ra = query['RA'][0]
            dec = query['DEC'][0]
            coord = SkyCoord('{} {}'.format(ra, dec), unit=(u.hourangle, u.deg))
            return_string.append(coord.to_string('hmsdms'))
        # Convert the list to a comma separated list before returning
        return_string = ','.join(return_string)
    except:
        return_string = None
    return return_string

def get_elevation_solar(obs_date, offender):
    """For a given observation date and bright solar system object, return its
       elevation over the course of that day.
       Input parameters:
       * obs_date: Observation date in datetime.datetime format
       * offender: Name of the solar system object. Allowed names are
                   Sun, Moon, and Jupiter.
       Returns:
       List of elevations in degrees. If offender is invalid, return None.
    """
    # Create the telescope object
    lofar = get_dutch_lofar_object()
    if offender == 'Sun':
        obj = Sun()
    elif offender == 'Moon':
        obj = Moon()
    elif offender == 'Jupiter':
        obj = Jupiter()
    else:
        return None

    yaxis = []
    for time in obs_date:
        lofar.date = time
        obj.compute(lofar)
        elevation = float(obj.alt)*180./np.pi
        if elevation < 0:
            elevation = np.nan
        yaxis.append(elevation)

    return yaxis

def get_elevation_target(target, obs_date, n_int):
    """For a given target and list of times, return a list of its elevation.
       If n_int is 0, compute elevation with respect to the NL array. If n_int>0,
       elevation needs to take into account the entire European array.
       Input Parameters:
       * target: An ephem.FixedBody() object
       * obs_date: List of datetime.datetime objects
       * n_int: Number of international stations to use in the observation.
    """
    lofar = get_dutch_lofar_object()
    yaxis = []
    if n_int == 0:
        # We are observing with the Dutch array
        for time in obs_date:
            lofar.date = time
            target.compute(lofar)
            elevation = float(target.alt)*180./np.pi
            if elevation < 0:
                elevation = np.nan
            yaxis.append(elevation)
    else:
        # We are observing with the entire ILT array
        # In addition to lofar, we also need IE and LV Observer() objects
        lv = get_lv_lofar_object()
        ie = get_ie_lofar_object()
        elevation = [0, 0, 0]
        for time in obs_date:
            lofar.date = time
            lv.date = time
            ie.date = time
            target.compute(lofar)
            elevation[0] = float(target.alt)*180./np.pi
            target.compute(lv)
            elevation[1] = float(target.alt)*180./np.pi
            target.compute(ie)
            elevation[2] = float(target.alt)*180./np.pi
            if np.min(elevation) < 0:
                yaxis.append(np.nan)
            else:
                yaxis.append(np.min(elevation))
    return yaxis

def find_target_elevation(src_name, coord, obs_date, n_int):
    """For a given date and coordinate, find the elevation of the source every
       10 mins. Return both the datetime object array and the elevation array"""
    # Find the start and the end times
    d = obs_date.split('-')
    start_time = datetime(int(d[0]), int(d[1]), int(d[2]), 0, 0, 0)
    end_time = start_time + timedelta(days=1)
    # Get a list of values along the time axis
    xaxis = []
    temp_time = start_time
    while temp_time < end_time:
        xaxis.append(temp_time)
        temp_time += timedelta(minutes=5)

    # Create a target object
    return_data = []
    src_name_list = src_name.split(',')
    for i in range(len(coord)):
        target = FixedBody()
        target._epoch = '2000'
        coord_target = SkyCoord(coord[i])
        target._ra = coord_target.ra.radian
        target._dec = coord_target.dec.radian

        # Iterate over each time interval and estimate the elevation of the target
        yaxis = get_elevation_target(target, xaxis, n_int)
        # Create a Plotly Scatter object that can be plotted later
        return_data.append(Scatter(x=xaxis, y=yaxis, mode='lines',
                                   line={}, name=src_name_list[i]))

    # We should also plot Sun, Moon, and Jupiter by default
    yaxis = get_elevation_solar(xaxis, 'Sun')
    return_data.append(Scatter(x=xaxis, y=yaxis, mode='lines',
                               line={}, name='Sun'))
    yaxis = get_elevation_solar(xaxis, 'Moon')
    return_data.append(Scatter(x=xaxis, y=yaxis, mode='lines',
                               line={}, name='Moon'))
    yaxis = get_elevation_solar(xaxis, 'Jupiter')
    return_data.append(Scatter(x=xaxis, y=yaxis, mode='lines',
                               line={}, name='Jupiter'))
    return return_data

def add_sun_rise_and_set_times(obs_date, n_int, elevation_fig):
    """
    For a given obs_date, find the sun rise and set times. Add these to the supplied
    elevation_fig and return the modified elevation_fig.
    """
    d = obs_date.split('-')
    start_time = datetime(int(d[0]), int(d[1]), int(d[2]), 0, 0, 0)
    sun = Sun()
    sun._epoch = '2000'
    if n_int == 0:
        # Only Dutch array is being used. Calculate Sun rise and set times in NL
        lofar = get_dutch_lofar_object()
        lofar.date = start_time
        sun_rise = lofar.next_rising(sun).datetime()
        sun_set = lofar.next_setting(sun).datetime()
        # Define a 1 hour window around Sun rise and Sun set.
        sun_rise_beg = sun_rise - timedelta(minutes=30)
        sun_rise_end = sun_rise + timedelta(minutes=30)
        sun_set_beg = sun_set - timedelta(minutes=30)
        sun_set_end = sun_set + timedelta(minutes=30)
    else:
        # Calculate sun rise and set times using Latvian and Irish stations
        lv = get_lv_lofar_object()
        ie = get_ie_lofar_object()
        lv.date = start_time
        ie.date = start_time
        lv_sun_rise = lv.next_rising(sun).datetime()
        lv_sun_set = lv.next_setting(sun).datetime()
        ie_sun_rise = ie.next_rising(sun).datetime()
        ie_sun_set = ie.next_setting(sun).datetime()
        # Define a window around sun rise and sun set.
        sun_rise_beg = lv_sun_rise - timedelta(minutes=30)
        sun_rise_end = ie_sun_rise + timedelta(minutes=30)
        sun_set_beg = lv_sun_set - timedelta(minutes=30)
        sun_set_end = ie_sun_set + timedelta(minutes=30)
    # Add to elevation_fig
    elevation_fig['layout']['shapes'].append({
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
    elevation_fig['layout']['shapes'].append({
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
    return elevation_fig

def get_distance_solar(target, obs_date, offender):
    """Compute the angular distance in degrees between the specified target and
       the offending radio source in the solar system on the specified observing
       date.
       Input parameters:
       * target   - Coordinate of the target as an Astropy SkyCoord object
       * obs_date  - Observing date in datetime.datetime format
       * offender - Name of the offending bright source. Allowed values are
                    Sun, Moon, Jupiter.
       Returns:
       For Moon, the minimum and maximum separation are returned. For others,
       distance,None is returned."""
    # Get a list of values along the time axis
    d = obs_date.split('-')
    start_time = datetime(int(d[0]), int(d[1]), int(d[2]), 0, 0, 0)
    end_time = start_time + timedelta(hours=24)
    taxis = []
    temp_time = start_time
    while temp_time < end_time:
        taxis.append(temp_time)
        temp_time += timedelta(hours=1)
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

def make_distance_table(src_name_input, coord_input, obs_date):
    """Generate a plotly Table showing the distances between user-specified
       targets and a few offending sources"""
    src_name_list = src_name_input.split(',')
    coord_list = coord_input.split(',')
    col_names = ['Sources']+src_name_list
    header = {
        'values': col_names,
        'font'  : {'size':12, 'color':'white'},
        'align' : 'left',
        'fill_color': 'grey',
        'line_color': 'darkslategray'
    }
    col_values = [['CasA', 'CygA', 'TauA', 'VirA', 'Sun',
                   'Moon(min,max)', 'Jupiter']]

    # Iterate through each source and compute the distances
    for idx, target in enumerate(src_name_list):
        # Get the coordinate of this target
        t_coord = SkyCoord(coord_list[idx])
        # CasA
        s_coord = SkyCoord(ATEAM_COORDINATES['CasA'])
        d_casa = s_coord.separation(t_coord).deg
        # CygA
        s_coord = SkyCoord(ATEAM_COORDINATES['CygA'])
        d_cyga = s_coord.separation(t_coord).deg
        # TauA
        s_coord = SkyCoord(ATEAM_COORDINATES['TauA'])
        d_taua = s_coord.separation(t_coord).deg
        # VirA
        s_coord = SkyCoord(ATEAM_COORDINATES['VirA'])
        d_vira = s_coord.separation(t_coord).deg
        # Sun
        d_sun, _ = get_distance_solar(t_coord, obs_date, 'Sun')
        # Moon
        d_moon_min, d_moon_max = get_distance_solar(t_coord, obs_date, 'Moon')
        # Jupiter
        d_jupiter, _ = get_distance_solar(t_coord, obs_date, 'Jupiter')
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
