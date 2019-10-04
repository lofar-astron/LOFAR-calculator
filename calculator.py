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
import targetvis as tv
import generatepdf as g
import os
from random import randint

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
        Output('dyCompressRow','style'),
        Output('pipeSizeRowL', 'style'),
        Output('pipeSizeRow', 'style'),
        Output('pipeProcTimeRow', 'style'),
        Output('pipeProcTimeRowL', 'style')
    ],
    [Input('pipeTypeRow','value')]
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
# What should the resolve button do?
#######################################
@app.callback(
   [  Output('coordRow', 'value'),
      Output('msgboxResolve', 'is_open')
   ],
   [  Input('resolve', 'n_clicks'),
      Input('mbResolveClose', 'n_clicks')
   ],
   [  State('targetNameRow', 'value'),
      State('msgboxResolve', 'is_open')
   ]
)
def on_resolve_click(n, closeMsgBox, targetName, is_open):
   """Function defines what to do when the resolve button is clicked"""
   if is_open is True and closeMsgBox is not None:
      # The message box is open and the user has clicked the close
      # button. Close the alert message
      return '', False
   if n is None:
      # The page has just loaded.
      return '', False
   else:
      # Resole button has been clicked
      coord_str = tv.resolve_source(targetName)
      if coord_str is None:
         # Display error message. 
         return '', True
      else:
         return coord_str, False

#######################################
# What should the export button do?
#######################################
@app.callback(
   [  Output('download-link', 'style'),
      Output('download-link', 'href'),
      Output('msgboxGenPdf', 'is_open')
   ],
   [  Input('genpdf', 'n_clicks'),
      Input('mbGenPdfClose', 'n_clicks')
   ],
   [  State('obsTimeRow', 'value'),
      State('nCoreRow',   'value'),
      State('nRemoteRow','value'),
      State('nIntRow','value'),
      State('nChanRow','value'),
      State('nSbRow','value'),
      State('intTimeRow','value'),
      State('hbaDualRow', 'value'),
      
      State('pipeTypeRow','value'),
      State('tAvgRow','value'),
      State('fAvgRow','value'),
      State('dyCompressRow','value'),
      
      State('imNoiseRow','value'),
      State('rawSizeRow', 'value'),
      State('pipeSizeRow', 'value'),
      State('pipeProcTimeRow', 'value'),
      
      State('msgboxGenPdf', 'is_open')
   ]
)
def on_genpdf_click(n_clicks, closeMsgBox, obsT, nCore, nRemote, nInt, nChan,
                    nSb, integT, antSet, pipeType, tAvg, fAvg, isDysco, 
                    imNoiseVal, rawSize, procSize, pipeTime, isMsgBoxOpen):
   """Function defines what to do when the generate pdf button is clicked"""
   if isMsgBoxOpen is True and closeMsgBox is not None:
      # The message box is open and the user has clicked the close
      # button. Close the alert message.
      return {'display':'none'}, '', False
   if n_clicks is None:
      # Generate button has not been clicked. Hide the download link
      return {'display':'none'}, '', False
   else:
      if imNoiseVal is '':
         # User has clicked generate PDF button before calculate
         return {'display':'none'}, '', True
      else:
         # Generate a random number so that this user's pdf can be stored here 
         randnum = '{:04d}'.format(randint(0,1000))
         relPath = os.path.join('static', randnum)
         # Create this folder
         absPath = os.path.join(os.getcwd(), relPath)
         os.mkdir(absPath)
         # Generate a relative and absolute filenames to the pdf file
         relPath = os.path.join(relPath, 'summary.pdf')
         absPath = os.path.join(os.getcwd(), relPath)
         g.generatepdf(relPath, obsT, nCore, nRemote, nInt, nChan,
                    nSb, integT, antSet, pipeType, tAvg, fAvg, isDysco, 
                    imNoiseVal, rawSize, procSize, pipeTime, isMsgBoxOpen)
         return {'display':'block'}, relPath, False

#######################################
# What should the reset button do?
#######################################
@app.callback(
    [  Output('obsTimeRow', 'value'),
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
    [  Output('imNoiseRow','value'),
       Output('rawSizeRow','value'),
       Output('pipeSizeRow','value'),
       Output('pipeProcTimeRow','value'),
       Output('msgBoxBody', 'children'),
       Output('msgbox', 'is_open'),
       Output('graphRow', 'style')
    ],
    [  Input('calculate','n_clicks'), 
       Input('msgBoxClose', 'n_clicks')
    ],
    [  State('obsTimeRow','value'),
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
       return '', '', '', '', '', False, {'display':'none'}
    if n is None:
        # Calculate button has not been clicked yet
        # So, do nothing and set default values to results field
        return '', '', '', '', '', False, {'display':'none'}
    else:
        # Calculate button has been clicked.
        # First, validate all command line inputs
        status, msg = bk.validate_inputs(obsT, nSB, integT, tAvg, fAvg)
        if status is False:
           print(msg)
           return '', '', '', '', msg, True, {'display':'none'}
        else:
           # Estimate the raw data size
           nBaselines = bk.compute_baselines(int(nCore), int(nRemote), 
                                             int(nInt), hbaMode)
           imNoise = bk.calculate_im_noise(int(nCore), int(nRemote),
                                           int(nInt), hbaMode, float(obsT), int(nSB))
           rawSize = bk.calculate_raw_size(float(obsT), float(integT), 
                                           nBaselines, int(nChan), int(nSB))
           avgSize = bk.calculate_proc_size(float(obsT), float(integT), nBaselines,
                                            int(nChan), int(nSB), pipeType, 
                                            int(tAvg), int(fAvg), dyCompress)
           return imNoise, rawSize, avgSize, 0, '', \
                  False, {'display':'block'}

if __name__ == '__main__':
    app.run_server(debug=True)
