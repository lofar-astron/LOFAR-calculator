#!/usr/bin/env python

__author__ = "Sarrvesh S. Sridhar"
__email__  = "sarrvesh@astron.nl"

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from gui import layout
from gui import header, obsGUIFrame, pipeGUIFrame, resultGUIFrame
from gui import defaultParams, msgBoxObsT, msgBoxnSB, msgBoxIntT, msgBox
import backend as bk

# Initialize the dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

#######################################
# Setup the layout of the web interface
#######################################
app.layout = layout

##############################################
# TODO: Move all callbacks to a separate file
# See https://community.plot.ly/t/dash-callback-in-a-separate-file/14122/16
##############################################

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
    elif value == 'preprocessing' or value=='prefactor':
        #style['display'] = 'block'
        return {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}, \
               {'display':'block'}, {'display':'block'}

#######################################
# Validate observation time
#######################################
@app.callback(
   Output('msgboxObsT', 'is_open'),
   [ 
      Input('obsTimeRow', 'n_blur'), 
      Input('mbObsTClose', 'n_clicks') 
   ],
   [ 
      State('obsTimeRow', 'value'),
      State('msgboxObsT', 'is_open')
   ]
)
def validate_obsT(n_blur, n_clicks, value, is_open):
   """Validate observation time and display error message if needed"""   
   if is_open is True and n_clicks is not None:
      # The message box is open and the user has clicked the close
      # button. Close the alert message
      return False
   if n_blur is None:
      # The page is loading. Do not validate anything
      return False
   else:
      # Observation time text box has lost focus. 
      # Go ahead and validate the text in it.
      try:
         float(value)
      except ValueError:
         return True
      if not float(value) > 0:
         return True
      return False

#######################################
# Validate number of subbands
#######################################
@app.callback(
   Output('msgboxnSB', 'is_open'),
   [ 
      Input('nSbRow', 'n_blur'), 
      Input('mbnSBClose', 'n_clicks') 
   ],
   [ 
      State('nSbRow', 'value'),
      State('msgboxnSB', 'is_open')
   ]
)
def validate_nSB(n_blur, n_clicks, value, is_open):
   """Validate the number of subbands and display error message if needed"""   
   if is_open is True and n_clicks is not None:
      # The message box is open and the user has clicked the close
      # button. Close the alert message
      return False  
   if n_blur is None:
      # The page is loading. Do not validate anything
      return False
   else:
      # Observation time text box has lost focus. 
      # Go ahead and validate the text in it.
      try:
         int(value)
      except ValueError:
         return True
      if not int(value) > 0:
         return True
      return False

#######################################
# Validate integration time
#######################################
@app.callback(
   Output('msgboxIntT', 'is_open'),
   [ 
      Input('intTimeRow', 'n_blur'), 
      Input('mbintTClose', 'n_clicks') 
   ],
   [ 
      State('intTimeRow', 'value'),
      State('msgboxIntT', 'is_open')
   ]
)
def validate_integT(n_blur, n_clicks, value, is_open):
   """Validate the integration time and display error message if needed"""   
   if is_open is True and n_clicks is not None:
      # The message box is open and the user has clicked the close
      # button. Close the alert message
      return False  
   if n_blur is None:
      # The page is loading. Do not validate anything
      return False
   else:
      # Observation time text box has lost focus. 
      # Go ahead and validate the text in it.
      try:
         int(value)
      except ValueError:
         return True
      if not int(value) > 0:
         return True
      return False

#######################################
# Validate time averaging factor
#######################################
@app.callback(
   Output('msgboxTAvg', 'is_open'),
   [ 
      Input('tAvgRow', 'n_blur'), 
      Input('mbtAvgClose', 'n_clicks') 
   ],
   [ 
      State('tAvgRow', 'value'),
      State('msgboxTAvg', 'is_open')
   ]
)
def validate_tAvg(n_blur, n_clicks, value, is_open):
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
   [ 
      Input('fAvgRow', 'n_blur'), 
      Input('mbfAvgClose', 'n_clicks') 
   ],
   [ 
      State('fAvgRow', 'value'),
      State('msgboxFAvg', 'is_open')
   ]
)
def validate_tAvg(n_blur, n_clicks, value, is_open):
   """Validate frequency averaging factor and display error message if needed"""
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
        Output('msgBoxBody', 'children'),
        Output('msgbox', 'is_open')
    ],
    [ 
       Input('calculate','n_clicks'), 
       Input('msgBoxClose', 'n_clicks')
    ],
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
        State('dyCompressRow','value'),
        State('msgbox', 'is_open')
    ]
)
def on_calculate_click(n, n_clicks, obsT, nCore, nRemote, nInt, nChan, nSB, 
                       integT, hbaMode, pipeType, tAvg, fAvg, dyCompress, is_open):
    """Function defines what to do when the calculate button is clicked"""
    if is_open is True:
       # User has closed the error message box
       return '', '', '', '', '', False
    if n is None:
        # Calculate button has not been clicked yet
        # So, do nothing and set default values to results field
        return '', '', '', '', '', False
    else:
        # Calculate button has been clicked.
        # First, validate all command line inputs
        status, msg = bk.validate_inputs(obsT, nSB, integT, tAvg, fAvg)
        if status is False:
           print(msg)
           return '', '', '', '', msg, True
        else:
           # Estimate the raw data size
           nBaselines = bk.compute_baselines(int(nCore), int(nRemote), 
                                             int(nInt), hbaMode)
           rawSize = bk.calculate_raw_size(float(obsT), float(integT), 
                                           nBaselines, int(nChan), int(nSB))
           avgSize = bk.calculate_avg_size(float(obsT), float(integT), nBaselines,
                                           int(nChan), int(nSB), pipeType, 
                                           int(tAvg), int(fAvg), dyCompress)
           return 0, rawSize, avgSize, 0, '', False

if __name__ == '__main__':
    app.run_server(debug=True)
