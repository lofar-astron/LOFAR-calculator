"""Main file for LUCI"""

__author__ = "Sarrvesh S. Sridhar"
__email__ = "sarrvesh@astron.nl"

from random import randint
import os
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import flask
from gui import layout
import backend as bk
import targetvis as tv
import generatepdf as g

# Initialize the dash app
server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], \
                server=server, url_base_pathname='/luci/')
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

#######################################
# Setup the layout of the web interface
#######################################
app.layout = layout
app.title = 'LUCI - LOFAR Unified Calculator for Imaging'

##############################################
# TODO: Move all callbacks to a separate file
# See https://community.plot.ly/t/dash-callback-in-a-separate-file/14122/16
##############################################

##############################################
# Show observational setup fields based on
# obsMode dropdown value
##############################################
@app.callback(
    [Output('tabModeForm', 'style'),
     Output('tabModeRowL', 'style'),
     Output('tabModeRow', 'style'),
     Output('tabModeRow', 'value'),

     Output('stokesForm', 'style'),
     Output('stokesRowL', 'style'),
     Output('stokesRow', 'style'),

     Output('nRingsForm', 'style'),
     Output('nRingsRow', 'style'),
     Output('nRingsRowL', 'style'),

     Output('pipeTypeRow', 'options'),
     Output('pipeTypeRow', 'value')
    ],
    [Input('obsModeRow', 'value')]
)
def toggle_obs_mode(obs_value):
    """Function to show relevant observational setup fields
       depending on the user's choice"""
    all_pipelines = {
        'Interferometric': ['none', 'preprocessing'],
        'Beamformed': ['none', 'pulp']
    }
    valid_pipes = [{'label':i, 'value':i} for i in all_pipelines[obs_value]]
    if obs_value == 'Interferometric':
        return {'display':'none'}, {'display':'none'}, {'display':'none'}, 'Incoherent', \
               {'display':'none'}, {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}, {'display':'none'}, \
               valid_pipes, 'none'
    else:
        return {}, {'display':'block'}, {'display':'block'}, 'Incoherent', \
               {}, {'display':'block'}, {'display':'block'}, \
               {}, {'display':'block'}, {'display':'block'}, \
               valid_pipes, 'none'

################################################
# Show TAb stokes fields based on dropdown value
################################################
@app.callback(
    [Output('stokesRow', 'options'),
     Output('stokesRow', 'value'),

     Output('nRemoteForm', 'style'),
     Output('nRemoteRow', 'style'),
     Output('nRemoteRowL', 'style'),

     Output('nIntForm', 'style'),
     Output('nIntRow', 'style'),
     Output('nIntRowL', 'style'),
    ],
    [Input('tabModeRow', 'value')]
)
def toggle_stokes(value):
    """Function to show relevant Stokes products depending
       on the user's TAB choice"""
    if value == '':
        value = 'Coherent'
    all_stokes = {
        'Coherent': ['I', 'IQUV', 'XXYY'],
        'Incoherent': ['I', 'IQUV']
    }
    valid_stokes = [{'label':i, 'value':i} for i in all_stokes[value]]
    if value == 'Incoherent':
        return valid_stokes, 'I', \
               {}, {'display':'block'}, {'display':'block'}, \
               {}, {'display':'block'}, {'display':'block'}
    else:
        return valid_stokes, 'I', \
               {'display':'none'}, {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}, {'display':'none'},


##############################################
# Show pipeline fields based on dropdown value
##############################################
@app.callback(
    [Output('tAvgRowL', 'style'),
     Output('tAvgRow', 'style'),
     Output('fAvgRowL', 'style'),
     Output('fAvgRow', 'style'),
     Output('dyCompressRowL', 'style'),
     Output('dyCompressRow', 'style'),
     Output('pipeSizeRowL', 'style'),
     Output('pipeSizeRow', 'style'),
     Output('pipeProcTimeRow', 'style'),
     Output('pipeProcTimeRowL', 'style')
    ],
    [Input('pipeTypeRow', 'value')]
)
def toggle_pipeline(value):
    """Function to show relevant pipeline fields depending on
       the user's pipeline choice."""
    if value == 'none':
        return {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}
    elif value == 'preprocessing':
        return {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}

#######################################
# Validate time averaging factor
#######################################
@app.callback(
    Output('msgboxTAvg', 'is_open'),
    [Input('tAvgRow', 'n_blur'),
     Input('mbtAvgClose', 'n_clicks')
    ],
    [State('tAvgRow', 'value'),
     State('msgboxTAvg', 'is_open')
    ]
)
def validate_t_avg(n_blur, n_clicks, value, is_open):
    """Validate time averaging factor and display error message if needed"""
    if is_open is True and n_clicks is not None:
        # The message box is open and the user has clicked the close
        # button. Close the alert message
        return False
    if n_blur is None:
        # The page is loading. Do not validate anything
        return False
    else:
        # Text box has lost focus.
        # Go ahead and validate the text in it.
        try:
            int(str(value))
        except ValueError:
            return True
        return False

#######################################
# Validate freq averaging factor
#######################################
@app.callback(
    Output('msgboxFAvg', 'is_open'),
    [Input('fAvgRow', 'value'),
     Input('mbfAvgClose', 'n_clicks')
    ],
    [State('msgboxFAvg', 'is_open'),
     State('nChanRow','value')
    ]
)
def validate_f_avg(value, n_clicks, is_open, channels_per_subband):
    """Validate frequency averaging factor and display error message if needed"""
    if is_open is True and n_clicks is not None:
        # The message box is open and the user has clicked the close
        # button. Close the alert message
        return False
    #if n_blur is None:
        # The page is loading. Do not validate anything
    #    return False
    else:
        # Text box has lost focus.
        # Go ahead and validate the text in it.
        try:
            int(str(value))
        except ValueError:
            return True
        try:
            assert int(str(channels_per_subband))>=int(str(value))
        except:
            return True
        return False


#######################################
# Limit freq averaging factor
#######################################
@app.callback(
    Output('fAvgRow', 'options'),
    [Input('nChanRow', 'value'),
     Input('mbfAvgClose', 'n_clicks')
    ],
    [State('msgboxFAvg', 'is_open'),
    ]
)
def validate_f_avg(value, n_clicks, is_open):
    """Validate frequency averaging factor and display error message if needed"""
    if is_open is True and n_clicks is not None:
        # The message box is open and the user has clicked the close
        # button. Close the alert message
        return False
    #if n_blur is None:
        # The page is loading. Do not validate anything
    #    return False
    else:
        # Text box has lost focus.
        # Go ahead and validate the text in it.
        if int(str(value))==64:
            return [
                        {'label':'1', 'value':1},
                        {'label':'2', 'value':2},
                        {'label':'4', 'value':4},
                        {'label':'8', 'value':8},
                        {'label':'16', 'value':16},
                        {'label':'32', 'value':32},
                        {'label':'64', 'value':64},
                    ]
        elif  int(str(value))==128:
            return [
                        {'label':'1', 'value':1},
                        {'label':'2', 'value':2},
                        {'label':'4', 'value':4},
                        {'label':'8', 'value':8},
                        {'label':'16', 'value':16},
                        {'label':'32', 'value':32},
                        {'label':'64', 'value':64},
                        {'label':'128', 'value':128},
                    ]
        # else, return default, max 256 averaging factor
        return [
                        {'label':'1', 'value':1},
                        {'label':'2', 'value':2},
                        {'label':'4', 'value':4},
                        {'label':'8', 'value':8},
                        {'label':'16', 'value':16},
                        {'label':'32', 'value':32},
                        {'label':'64', 'value':64},
                        {'label':'128', 'value':128},
                        {'label':'256', 'value':256}
                    ]



#######################################
# What should the resolve button do?
#######################################
@app.callback(
    [Output('coordRow', 'value'),
     Output('msgboxResolve', 'is_open')
    ],
    [Input('resolve', 'n_clicks'),
     Input('mbResolveClose', 'n_clicks')
    ],
    [State('targetNameRow', 'value'),
     State('msgboxResolve', 'is_open')
    ]
)
def on_resolve_click(n, close_msg_box, target_name, is_open):
    """Function defines what to do when the resolve button is clicked"""
    if is_open is True and close_msg_box is not None:
        # The message box is open and the user has clicked the close
        # button. Close the alert message
        return '', False
    if n is None:
        # The page has just loaded.
        return '', False
    else:
        # Resole button has been clicked
        coord_str = tv.resolve_source(target_name)
        if coord_str is None:
            # Display error message.
            return '', True
        else:
            return coord_str, False

#######################################
# What should the export button do?
#######################################
@app.callback(
    [Output('download-link', 'style'),
     Output('download-link', 'href'),
     Output('msgboxGenPdf', 'is_open')
    ],
    [Input('genpdf', 'n_clicks'),
     Input('mbGenPdfClose', 'n_clicks')
    ],
    [State('obsTimeRow', 'value'),
     State('calTimeRow', 'value'),
     State('nCalRow', 'value'),
     State('nCoreRow', 'value'),
     State('nRemoteRow', 'value'),
     State('nIntRow', 'value'),
     State('nChanRow', 'value'),
     State('nSbRow', 'value'),
     State('intTimeRow', 'value'),
     State('hbaDualRow', 'value'),
     State('coordRow', 'value'),

     State('pipeTypeRow', 'value'),
     State('tAvgRow', 'value'),
     State('fAvgRow', 'value'),
     State('dyCompressRow', 'value'),

     State('imNoiseRow', 'value'),
     State('rawSizeRow', 'value'),
     State('pipeSizeRow', 'value'),
     State('pipeProcTimeRow', 'value'),

     State('msgboxGenPdf', 'is_open'),

     State('elevation-plot', 'figure'),
     State('distance-table', 'figure'),

     State('dateRow', 'date')
    ]
)
def on_genpdf_click(n_clicks, close_msg_box, obs_t, cal_t, n_cal, n_core, n_remote, n_int, n_chan,
                    n_sb, integ_t, ant_set, coord, pipe_type, t_avg, f_avg, is_dysco,
                    im_noise_val, raw_size, proc_size, pipe_time, is_msg_box_open,
                    elevation_fig, distance_table, obs_date):
    """Function defines what to do when the generate pdf button is clicked"""
    if is_msg_box_open is True and close_msg_box is not None:
        # The message box is open and the user has clicked the close
        # button. Close the alert message.
        return {'display':'none'}, '', False
    if n_clicks is None:
        # Generate button has not been clicked. Hide the download link
        return {'display':'none'}, '', False
    else:
        if im_noise_val is '':
            # User has clicked generate PDF button before calculate
            return {'display':'none'}, '', True
        else:
            # Generate a random number so that this user's pdf can be stored here
            randnum = '{:05d}'.format(randint(0, 10000))
            rel_path = 'static/'
            # Generate a relative and absolute filenames to the pdf file
            rel_path = os.path.join(rel_path, 'summary_{}.pdf'.format(randnum))
            abs_path = os.path.join(os.getcwd(), rel_path)
            g.generate_pdf(rel_path, obs_t, cal_t, n_cal, n_core, n_remote, n_int, n_chan,
                           n_sb, integ_t, ant_set, coord, pipe_type, t_avg, f_avg,
                           is_dysco, im_noise_val, raw_size, proc_size, pipe_time,
                           elevation_fig, distance_table, obs_date)
            return {'display':'block'}, '/luci/{}'.format(rel_path), False

@app.server.route('/luci/static/<resource>')
def serve_static(resource):
    path = os.path.join(os.getcwd(), 'static')
    return flask.send_from_directory(path, resource)

#######################################
# What should the submit button do?
#######################################
@app.callback(
    [Output('imNoiseRow', 'value'),
     Output('rawSizeRow', 'value'),
     Output('pipeSizeRow', 'value'),
     Output('pipeProcTimeRow', 'value'),
     Output('msgBoxBody', 'children'),
     Output('msgbox', 'is_open'),
     Output('elevation-plot', 'style'),
     Output('elevation-plot', 'figure'),
     Output('beam-plot', 'style'),
     Output('beam-plot', 'figure'),
     Output('distance-table', 'style'),
     Output('distance-table', 'figure')
    ],
    [Input('calculate', 'n_clicks'),
     Input('msgBoxClose', 'n_clicks'),
    ],
    [State('obsTimeRow', 'value'),
     State('calTimeRow', 'value'),
     State('nCalRow', 'value'),
     State('nCoreRow', 'value'),
     State('nRemoteRow', 'value'),
     State('nIntRow', 'value'),
     State('nChanRow', 'value'),
     State('nSbRow', 'value'),
     State('intTimeRow', 'value'),
     State('hbaDualRow', 'value'),
     State('pipeTypeRow', 'value'),
     State('tAvgRow', 'value'),
     State('fAvgRow', 'value'),
     State('dyCompressRow', 'value'),
     State('msgbox', 'is_open'),
     State('targetNameRow', 'value'),
     State('coordRow', 'value'),
     State('dateRow', 'date'),
     State('calListRow', 'value'),
     State('demixListRow', 'value')
    ]
)
def on_calculate_click(n, n_clicks, obs_t, cal_t, n_cal, n_core, n_remote, n_int, n_chan, n_sb,
                       integ_t, hba_mode, pipe_type, t_avg, f_avg, dy_compress,
                       is_open, src_name, coord, obs_date, calib_names,
                       ateam_names):
    """Function defines what to do when the calculate button is clicked"""
    if is_open is True:
        # User has closed the error message box
        return '', '', '', '', '', False, \
               {'display':'none'}, {}, {'display':'none'}, \
               {}, {'display':'none'}, {}
    if n is None:
        # Calculate button has not been clicked yet
        # So, do nothing and set default values to results field
        return '', '', '', '', '', False, \
               {'display':'none'}, {}, {'display':'none'}, {}, \
               {'display':'none'}, {}
    else:
        # Calculate button has been clicked.
        # First, validate all command line inputs

        # If the user sets n_core, n_remote, or n_int to 0, dash return None.
        # Why is this?
        # Correct this manually, for now.
        if n_core is None:
            n_core = '0'
        if n_remote is None:
            n_remote = '0'
        if n_int is None:
            n_int = '0'
        status, msg = bk.validate_inputs(obs_t, cal_t, int(n_cal), int(n_core), int(n_remote), \
                                         int(n_int), n_sb, integ_t, t_avg, f_avg, \
                                         src_name, coord, hba_mode, pipe_type, \
                                         ateam_names)
        if status is False:
            return '', '', '', '', msg, True, \
                   {'display':'none'}, {}, {'display':'none'}, {}, \
                   {'display':'none'}, {}
        else:
            # Estimate the raw data size
            if coord is not '':
                coord_list = coord.split(',')
                coord_input_list = coord.split(',')
                n_sap=len(coord_list)
            else:
                n_sap=1

            n_baselines = bk.compute_baselines(int(n_core), int(n_remote),
                                               int(n_int), hba_mode)
            im_noise = bk.calculate_im_noise(int(n_core), int(n_remote),
                                             int(n_int), hba_mode, float(obs_t),
                                             int(n_sb))
            raw_size = bk.calculate_raw_size(float(obs_t), float(cal_t), int(n_cal), float(integ_t),
                                             n_baselines, int(n_chan), int(n_sb), n_sap)
            avg_size = bk.calculate_proc_size(float(obs_t), float(cal_t), int(n_cal), float(integ_t),
                                              n_baselines, int(n_chan), int(n_sb), n_sap,
                                              pipe_type, int(t_avg), int(f_avg),
                                              dy_compress)
            if pipe_type == 'none':
                # No pipeline
                pipe_time = None
            else:
                pipe_time = bk.calculate_pipe_time(float(obs_t), float(cal_t), int(n_cal), int(n_sb), n_sap,
                                                   hba_mode, ateam_names,
                                                   pipe_type)

            # It is useful to have coord as a list from now on

            # Add calibrator names to the target list so that they can be
            # plotted together. Before doing that, make a copy of the input
            # target list and its coordinates
            src_name_input = src_name
            coord_input = coord
            if calib_names is not None:
                for i in range(len(calib_names)):
                    if i == 0 and src_name is None:
                        src_name = '{}'.format(calib_names[i])
                        coord_list = [tv.CALIB_COORDINATES[calib_names[i]]]
                    else:
                        src_name += ', {}'.format(calib_names[i])
                        coord_list.append(tv.CALIB_COORDINATES[calib_names[i]])

            # Add A-team names to the target list so that they can be
            # plotted together
            if ateam_names is not None:
                for i in range(len(ateam_names)):
                    if i == 0 and src_name is None:
                        src_name = '{}'.format(ateam_names[i])
                        coord_list = [tv.ATEAM_COORDINATES[ateam_names[i]]]
                    else:
                        src_name += ', {}'.format(ateam_names[i])
                        coord_list.append(tv.ATEAM_COORDINATES[ateam_names[i]])

            if coord is '':
                # No source is specified under Target setup
                display_fig = {'display':'none'}
                elevation_fig = {}
                beam_fig = {}
                display_tab = {'display':'none'}
                distance_tab = {}
            else:
                # User has specified a coordinate and it has passed validation
                # in the validate_inputs function.
                # Check if the number of SAPs is less than 488
                n_point = len(coord_input_list)
                n_beamlet = n_point * int(n_sb)
                max_beamlet = 488
                if n_beamlet > max_beamlet:
                    msg = 'Number of targets times number of subbands cannot ' + \
                          'be greater than {}.'.format(max_beamlet)
                    return '', '', '', '', msg, True, \
                           {'display':'none'}, {}, {'display':'none'}, {}, \
                           {'display':'none'}, {}
                # Find target elevation across a 24-hour period
                data = tv.find_target_elevation(src_name, coord_list,
                                                obs_date, int(n_int))
                display_fig = {'display':'block', 'height':600}
                elevation_fig = {'data':data,
                                 'layout':{
                                     'xaxis':{'title':'Time (UTC)'},
                                     'yaxis':{'title':'Elevation'},
                                     'title':'Target visibility plot',
                                     'shapes':[]
                                 }
                                }
                elevation_fig = tv.add_sun_rise_and_set_times(obs_date,
                                                              int(n_int),
                                                              elevation_fig)
                # Find the position of the station and tile beam
                beam_fig = tv.find_beam_layout(src_name_input, coord_input, \
                                   int(n_core), int(n_remote), int(n_int), hba_mode)
                # Calculate distance between all the targets and offending sources
                display_tab = {'display':'block'}
                table_data = [tv.make_distance_table(src_name_input,
                                                     coord_input, obs_date)]
                table_title = 'Angular distances in degrees between specified ' +\
                             'targets and other bright sources'
                distance_tab = {'data':table_data,
                                'layout':{'title':table_title, 'autosize':True}
                               }

            return im_noise, raw_size, avg_size, pipe_time, '', \
                   False, display_fig, elevation_fig, display_fig, beam_fig, \
                   display_tab, distance_tab

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8051)
    #app.run_server(debug=False, host='0.0.0.0', port=8051, \
    #              dev_tools_ui=False, dev_tools_props_check=False)
