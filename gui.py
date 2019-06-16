import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

###############################################################################
# Define a modal to display error messages for observation time
###############################################################################
modalHeader = html.H2('Error')
msgBoxObsT = dbc.Modal([
                       dbc.ModalHeader(modalHeader),                       
                       dbc.ModalBody('Invalid observation time specified'),
                       dbc.ModalFooter(
                                      dbc.Button('Close', id='mbObsTClose')
                                      )
                       ], id='msgboxObsT', centered=True)
msgBoxnSB = dbc.Modal([
                         dbc.ModalHeader(modalHeader),
                         dbc.ModalBody('Invalid number of subbands specified'),
                         dbc.ModalFooter(
                                        dbc.Button('Close', id='mbnSBClose')
                                        )
                      ], id='msgboxnSB', centered=True)
msgBoxIntT = dbc.Modal([
                         dbc.ModalHeader(modalHeader),
                         dbc.ModalBody('Invalid integration time specified'),
                         dbc.ModalFooter(
                                        dbc.Button('Close', id='mbintTClose')
                                        )
                       ], id='msgboxIntT', centered=True)
msgBox = dbc.Modal([
                      dbc.ModalHeader(modalHeader),
                      dbc.ModalBody('', id='msgBoxBody'),
                      dbc.ModalFooter(
                                     dbc.Button('Close', id='msgBoxClose')
                                     )
                   ], id='msgbox', centered=True)

###############################################################################
# Default values for various input fields
###############################################################################
defaultParams = {'obsTime':'28800', 'Ncore':'24', 'Nremote':'14',
                 'Nint':'13', 'Nchan':'64', 'Nsb':'488',
                 'intTime':'1', 'hbaDual':'disable',
                 
                 'pipeType':'none', 'tAvg':'1', 'fAvg':'1', 
                 'dyCompress':'enable',
                }

###############################################################################
# Layout of the header
###############################################################################
header = html.Div(children=[
            html.H1('LOFAR data size and processing time calculator')
         ], style={'padding':'10px 10px'})

# Parameters common for all 3 sub-panels
labelWidth = 8
inpWidth = 3
dropWidth = 4

###############################################################################
# Layout of observational setup
###############################################################################
obsTime = dbc.FormGroup([
            dbc.Label('Observation time (in seconds)', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='obsTimeRow'), width=inpWidth
            )
          ], row=True)
Ncore = dbc.FormGroup([
            dbc.Label('Number of core stations', width=labelWidth),
            dbc.Col(
                dbc.Input(type='number', id='nCoreRow', min=0, max=24),
                width=inpWidth
            )
        ], row=True)
Nremote = dbc.FormGroup([
            dbc.Label('Number of remote stations', width=labelWidth),
            dbc.Col(
                dbc.Input(type='number', id='nRemoteRow', min=0, max=14), 
                width=inpWidth
            )            
        ], row=True)
Nint = dbc.FormGroup([
            dbc.Label('Number of international stations', width=labelWidth),
            dbc.Col(
                dbc.Input(type='number', id='nIntRow', min=0, max=13), 
                width=inpWidth
            )
        ], row=True)
Nchan = dbc.FormGroup([
            dbc.Label('Number of channels per subband', width=labelWidth),
            dbc.Col(
                dbc.Input(type='number', id='nChanRow', min=0, max=256), width=inpWidth
            )
        ], row=True)
Nsb = dbc.FormGroup([
            dbc.Label('Number of subbands', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='nSbRow'), width=inpWidth
            )
        ], row=True)
intTime = dbc.FormGroup([
            dbc.Label('Integration time (in seconds)', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='intTimeRow'), width=inpWidth
            )
        ], row=True)
hbaDual = dbc.FormGroup([
            dbc.Label('Observe in HBA Dual mode?', width=labelWidth),
            dbc.Col(
                dcc.Dropdown(
                    options=[
                        {'label':'Disable', 'value':'disable'},
                        {'label':'Enable', 'value':'enable'}
                    ], value='disable', searchable=False, 
                       clearable=False, id='hbaDualRow',
                ), width=dropWidth
            )
          ], row=True)
buttons = html.Div([
            dbc.Row([
                dbc.Col(dbc.Button('Calculate', id='calculate', color='dark')),
                dbc.Col(dbc.Button('Reset inputs', id='reset', color='dark'))
            ])
          ])
obsGUISetup = dbc.Form([obsTime, Ncore, Nremote, Nint, Nchan, 
                        Nsb, intTime, hbaDual, buttons])
obsGUIFrame = html.Div(children=[
                html.H3('Observational setup'),
                html.Hr(),
                obsGUISetup
              ], style={'width':'95%', 'padding':'20px'})

###############################################################################
# Define the layout of the pipeline setup
###############################################################################
pipeType = dbc.FormGroup([
            dbc.Label('Pipeline', width=labelWidth),
            dbc.Col(
                dcc.Dropdown(
                    options=[
                        {'label':'None', 'value':'none'},
                        {'label':'Preprocessing', 'value':'preprocessing'}
                    ], value='none', searchable=False, 
                       clearable=False, id='pipeTypeRow'
                ), width=dropWidth
            )
          ], row=True)
tAvg = dbc.FormGroup([
           dbc.Label('Time averaging factor', width=labelWidth, 
                     id='tAvgRowL'
           ),
           dbc.Col(
            dbc.Input(type='number', id='tAvgRow', min=0), 
            width=inpWidth
           )
       ], row=True)
fAvg = dbc.FormGroup([
           dbc.Label('Frequency averaging factor', width=labelWidth,
                     id='fAvgRowL'
           ),
           dbc.Col(
            dbc.Input(type='number', id='fAvgRow', min=0), 
            width=inpWidth
           )
       ], row=True)
dyCompress = dbc.FormGroup([
                dbc.Label('Enable dysco compression?', width=labelWidth,
                          id='dyCompressRowL'
                ),
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                            {'label':'Disable', 'value':'disable'},
                            {'label':'Enable', 'value':'enable'}
                        ], value='enable', searchable=False, 
                           clearable=False, id='dyCompressRow'
                    ), width=dropWidth
                )
             ], row=True)
pipeGUISetup = dbc.Form([pipeType, tAvg, fAvg, dyCompress])
pipeGUIFrame = html.Div(children=[
                html.H3('Pipeline setup'),
                html.Hr(),
                pipeGUISetup
               ], style={'width':'95%', 'padding':'20px'})

###############################################################################
# Layout of the results tab
###############################################################################
imNoise = dbc.FormGroup([
            dbc.Label('Theoretical image noise', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='imNoiseRow', value='', 
                          disabled=True
                ), width=inpWidth
            )
          ], row=True)
rawSize = dbc.FormGroup([
            dbc.Label('Raw data size (in GB)', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='rawSizeRow', value='', 
                          disabled=True
                ), width=inpWidth
            )
          ], row=True)
pipeSize = dbc.FormGroup([
            dbc.Label('Processed data size (in GB)', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='pipeSizeRow', value='', 
                          disabled=True
                ), width=inpWidth
            )
          ], row=True)
pipeProcTime = dbc.FormGroup([
                  dbc.Label('Pipeline processing time (in hours)', 
                            width=labelWidth),
                  dbc.Col(
                     dbc.Input(type='text', id='pipeProcTimeRow', value='',
                               disabled=True
                     ), width=inpWidth
                  )
               ], row=True)
resultGUISetup = dbc.Form([imNoise, rawSize, pipeSize, pipeProcTime])
resultGUIFrame = html.Div(children=[
                    html.H3('Results'),
                    html.Hr(),
                    resultGUISetup
                 ], style={'width':'95%', 'padding':'20px'})
