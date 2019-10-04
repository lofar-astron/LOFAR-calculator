import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from datetime import date 

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
msgBoxTAvg = dbc.Modal([
                         dbc.ModalHeader(modalHeader),
                         dbc.ModalBody('Invalid time averaging factor specified'),
                         dbc.ModalFooter(
                                        dbc.Button('Close', id='mbtAvgClose')
                                        )
                       ], id='msgboxTAvg', centered=True)
msgBoxFAvg = dbc.Modal([
                         dbc.ModalHeader(modalHeader),
                         dbc.ModalBody('Invalid frequency averaging factor specified'),
                         dbc.ModalFooter(
                                        dbc.Button('Close', id='mbfAvgClose')
                                        )
                       ], id='msgboxFAvg', centered=True)
msgBoxResolve = dbc.Modal([
                         dbc.ModalHeader(modalHeader),
                         dbc.ModalBody('Unable to resolve the source name. Please ' + \
                                       'specify the coordinates manually.'),
                         dbc.ModalFooter(
                                        dbc.Button('Close', id='mbResolveClose')
                                        )
                         ], id='msgboxResolve', centered=True)
msgBoxGenPdf = dbc.Modal([
                         dbc.ModalHeader(modalHeader),
                         dbc.ModalBody('Nothing to generate. Please use the ' + \
                                       'calculate button before exporting to PDF'),
                         dbc.ModalFooter(
                                        dbc.Button('Close', id='mbGenPdfClose')
                                        )
                         ], id='msgboxGenPdf', centered=True)
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
                 
                 'targetName':'', 'target_coord':'',
                }

###############################################################################
# Layout of the header
###############################################################################
header = html.Div(children=[
            html.H1('LOFAR Unified Calculator for Imaging (LUCI)')
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
                dbc.Col(dbc.Button('Reset inputs', id='reset', color='dark')),
                dbc.Col(dbc.Button('Generate PDF', id='genpdf', color='dark'))
            ])
          ])
link = html.Div([
          html.A(id='download-link', children='Download file')
       ])
obsGUISetup = dbc.Form([obsTime, Ncore, Nremote, Nint, Nchan, 
                        Nsb, intTime, hbaDual, buttons, link])
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
                        {'label':'Preprocessing', 'value':'preprocessing'},
                        #{'label':'Prefactor', 'value':'prefactor'}
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
targetName = dbc.FormGroup([
                dbc.Label('Target', width=labelWidth-inpWidth, 
                          id='targetNameRowL'
                ),
                dbc.Col(
                   dbc.Input(id='targetNameRow', min=0), 
                   width=inpWidth
                ),
                dbc.Col(
                   dbc.Button('Resolve', id='resolve', color='dark')
                )
             ], row=True)
targetCoord = dbc.FormGroup([
                 dbc.Label('Coordinates', width=labelWidth-inpWidth),
                 dbc.Col(dbc.Input(id='coordRow'), width=inpWidth*2)                    
              ], row=True)
obsDate = dbc.FormGroup([
             dbc.Label('Observation date', width=labelWidth-inpWidth),
             dbc.Col(dcc.DatePickerSingle(date=date.today(), 
                                          display_format='DD/MM/YYYY',
                                          id='dateRow')
             )
          ], row=True)
targetGUISetup = dbc.Form([targetName, targetCoord, obsDate])
pipeGUIFrame = html.Div(children=[
                html.H3('Pipeline setup'),
                html.Hr(),
                pipeGUISetup,
                html.H3('Target setup'),
                html.Hr(),
                targetGUISetup
               ], style={'width':'95%', 'padding':'20px'})

###############################################################################
# Layout of the results tab
###############################################################################
imNoise = dbc.FormGroup([
            dbc.Label('Theoretical image sensitivity (uJy/beam)', width=labelWidth),
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
            dbc.Label('Processed data size (in GB)', width=labelWidth,
                      id='pipeSizeRowL'),
            dbc.Col(
                dbc.Input(type='text', id='pipeSizeRow', value='', 
                          disabled=True
                ), width=inpWidth
            )
          ], row=True)
pipeProcTime = dbc.FormGroup([
                  dbc.Label('Pipeline processing time (in hours)', 
                            width=labelWidth, id='pipeProcTimeRowL'),
                  dbc.Col(
                     dbc.Input(type='text', id='pipeProcTimeRow', value='',
                               disabled=True
                     ), width=inpWidth
                  )
               ], row=True)
warntext = '**Caution:** The sensitivity calculation performed by this tool follow '+\
           ' [SKA Memo 113](http://www.skatelescope.org/uploaded/59513_113_Memo_Nijboer.pdf) '+\
           'by Nijboer, Pandey-Pommier & de Bruyn.'+\
           ' It uses theoretical SEFD values. So, please use it with caution.'
cautiontext = html.Div([
                  dcc.Markdown(children=warntext)
              ], style={'width':'85%'})
resultGUISetup = dbc.Form([imNoise, rawSize, pipeSize, pipeProcTime, cautiontext])
resultGUIFrame = html.Div(children=[
                    html.H3('Results'),
                    html.Hr(),
                    resultGUISetup
                 ], style={'width':'95%', 'padding':'20px'})

###############################################################################
# Layout of the graph
###############################################################################
graph = dbc.Row(dbc.Col(
           html.Div([ 
               dcc.Graph(id='elevation-plot', 
                         figure={'layout':{'title':'Target visibility plot'}}
               )
           ])
        ), id='graphRow', style={'width':'66%'})

###############################################################################
# Define the layout of the calculator
###############################################################################
layout = html.Div([
                     dbc.Row(dbc.Col(header)),
                     dbc.Row([
                                dbc.Col(obsGUIFrame),
                                dbc.Col(pipeGUIFrame),
                                dbc.Col(resultGUIFrame)
                     ]),
                     graph,
                     
                     msgBoxObsT, msgBoxnSB, msgBoxIntT, msgBoxTAvg, msgBoxFAvg,
                     msgBoxResolve, msgBoxGenPdf, msgBox
                  ])
