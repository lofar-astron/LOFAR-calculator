#!/usr/bin/env python

__author__ = "Sarrvesh S. Sridhar"
__email__  = "sarrvesh@astron.nl"

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from gui import header, obsGUIFrame, pipeGUIFrame, resultGUIFrame
from gui import defaultParams
import backend as bk

# Initialize the dash app
# dbc.themes.LUMEN looks nice
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

#######################################
# Setup the layout of the web interface
#######################################
app.layout = html.Div([
                dbc.Row(dbc.Col(header)),
                dbc.Row([
                   dbc.Col(obsGUIFrame),
                   dbc.Col(pipeGUIFrame),
                   dbc.Col(resultGUIFrame)
                ]),
             ])

##############################################
# Show pipeline fields based on dropdown value
##############################################
@app.callback(
    [
        Output('tAvgRowL','style'),
        Output('tAvgRow','style'),
        Output('fAvgRowL','style'),
        Output('fAvgRow','style'),
        Output('dyCompressRowL','style'),
        Output('dyCompressRow','style')
    ],
    [Input('pipeTypeRow','value')]
)
def toggle_pipeline(value):
    """Function to show relevant pipeline fields depending on
       the user's pipeline choice."""
    if value == 'none':
        return {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}, \
               {'display':'none'}, {'display':'none'}
    elif value == 'preprocessing':
        #style['display'] = 'block'
        return {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}

#######################################
# What should the reset button do?
#######################################
@app.callback(
    [
       Output('obsTimeRow', 'value'),
       Output('nCoreRow',   'value'),
       Output('nRemoteRow','value'),
       Output('nIntRow','value'),
       Output('nChanRow','value'),
       Output('nSbRow','value'),
       Output('intTimeRow','value'),
       
       Output('tAvgRow','value'),
       Output('fAvgRow','value'),
       
       Output('hbaDualRow','value'),
       Output('pipeTypeRow','value'),
       Output('dyCompressRow','value')
    ],
    [Input('reset', 'n_clicks')]
)
def on_reset_click(n):
   """Function defines what to do when the reset button is clicked"""
   return defaultParams['obsTime'], defaultParams['Ncore'], \
          defaultParams['Nremote'], defaultParams['Nint'], \
          defaultParams['Nchan'], defaultParams['Nsb'], \
          defaultParams['intTime'], defaultParams['tAvg'], \
          defaultParams['fAvg'], defaultParams['hbaDual'], \
          defaultParams['pipeType'], defaultParams['dyCompress']

#######################################
# What should the submit button do?
#######################################
@app.callback(
    [
        Output('imNoiseRow','value'),
        Output('rawSizeRow','value'),
        Output('pipeSizeRow','value'),
        Output('pipeProcTimeRow','value'),
    ],
    [ Input('calculate','n_clicks') ],
    [
        State('obsTimeRow','value'),
        State('nCoreRow','value'),
        State('nRemoteRow','value'),
        State('nIntRow','value'),
        State('nChanRow','value'),
        State('nSbRow','value'),
        State('intTimeRow','value'),
        State('hbaDualRow','value'),
        State('pipeTypeRow','value'),
        State('tAvgRow','value'),
        State('fAvgRow','value'),
        State('dyCompressRow','value')
    ]
)
def on_calculate_click(n, obsT, nCore, nRemote, nInt, nChan, nSB, 
                       integT, hbaMode, pipeType, tAvg, fAvg, dyCompress):
    """Function defines what to do when the calculate button is clicked"""
    if n is None:
        # Calculate button has not been clicked yet
        # So, do nothing and set default values to results field
        return '', '', '', ''
    else:
        # Calculate button has been clicked.
        # First, validate all command line inputs
        status, msg = bk.validate_inputs(obsT, nSB, integT)
        if status is False:
           print(msg)
           return '', '', '', ''
        else:
           # Estimate the raw data size
           nBaselines = bk.compute_baselines(int(nCore), int(nRemote), 
                                             int(nInt), hbaMode)
           rawSize = bk.calculate_raw_size(float(obsT), float(integT), 
                                           nBaselines, int(nChan), int(nSB))
           avgSize = bk.calculate_avg_size(float(obsT), float(integT), nBaselines,
                                           int(nChan), int(nSB), pipeType, 
                                           int(tAvg), int(fAvg), dyCompress)
           return 0, rawSize, avgSize, 0

if __name__ == '__main__':
    app.run_server(debug=True)
