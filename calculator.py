#!/usr/bin/env python

__author__ = "Sarrvesh S. Sridhar"
__email__  = "sarrvesh@astron.nl"

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from gui import header, obsGUIFrame, pipeGUIFrame, resultGUIFrame
from gui import defaultParams

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
       
       Output('inNoiseRow','value'),
       Output('rawSizeRow','value'),
       Output('pipeSizeRow','value'),
       Output('pipeProcTimeRow','value'),
       
       Output('hbaDualRow','value'),
       Output('pipeTypeRow','value'),
       Output('dyCompressRow','value')
    ],
    [Input('reset', 'n_clicks')]
)
def on_reset_click(n):
   """Function defines what to do when the reset button is clicked"""
   if n is None:
      # Reset button has not been clicked yet 
      # So, do nothing
      return defaultParams['obsTime'], defaultParams['Ncore'], \
             defaultParams['Nremote'], defaultParams['Nint'], \
             defaultParams['Nchan'], defaultParams['Nsb'], \
             defaultParams['intTime'], defaultParams['tAvg'], \
             defaultParams['fAvg'], defaultParams['imSize'], \
             defaultParams['rawSize'], defaultParams['pipeSize'], \
             defaultParams['pipeProcTime'], defaultParams['hbaDual'], \
             defaultParams['pipeType'], defaultParams['dyCompress']
   else:
      # Reset button has been clicked
      # Restore all input and output fields to default
      return defaultParams['obsTime'], defaultParams['Ncore'], \
             defaultParams['Nremote'], defaultParams['Nint'], \
             defaultParams['Nchan'], defaultParams['Nsb'], \
             defaultParams['intTime'], defaultParams['tAvg'], \
             defaultParams['fAvg'], defaultParams['imSize'], \
             defaultParams['rawSize'], defaultParams['pipeSize'], \
             defaultParams['pipeProcTime'], defaultParams['hbaDual'], \
             defaultParams['pipeType'], defaultParams['dyCompress']
      

if __name__ == '__main__':
    app.run_server(debug=True)
