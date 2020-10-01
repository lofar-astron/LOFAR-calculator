import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from datetime import date

###############################################################################
# Define a modal to display error messages for observation time
###############################################################################
modalHeader = html.H2('Error')
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
defaultParams = {'obsMode':'Interferometric',
                 'tabMode':'Coherent',
                 'obsTime':'28800',
                 'calTime':'600',
                 'Ncal': '2',
                 'Ncore':'24',
                 'Nremote':'14',
                 'Nint':'14',
                 'Nchan':'64',
                 'Nsb':'488',
                 'intTime':'1',
                 'hbaDual':'hbadualinner',
                 'Nrings':'0',

                 'pipeType':'none',
                 'tAvg':'1',
                 'fAvg':'4',
                 'dyCompress':'enable',

                 'tAvgPulp':'60',
                 '8bit':'NO',
                 'digifil':'NO',
                 'no_pdmp':'NO',
                 'single_pulse':'NO',
                 'rrats':'NO',

                 'targetName':'',
                 'target_coord':'',
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
obsMode = dbc.FormGroup([
          dbc.Label('Observation mode', width=labelWidth),
          dbc.Col(
            dcc.Dropdown(
                options=[
                    {'label':'Interferometric', 'value':'Interferometric'},
                    {'label':'Beamformed', 'value':'Beamformed'}
                ], value=defaultParams['obsMode'], searchable=False,
                   clearable=False, id='obsModeRow'
            ), width=dropWidth
          )
        ], row=True)
tabMode = dbc.FormGroup([
          dbc.Label('Tied array mode', width=labelWidth, id='tabModeRowL'),
          dbc.Col(
            dcc.Dropdown(
                options=[
                    {'label':'Coherent', 'value':'Coherent'},
                    {'label':'Incoherent', 'value':'Incoherent'}
                ], value=defaultParams['tabMode'], searchable=False,
                   clearable=False, id='tabModeRow'
            ), width=dropWidth, id='tabModeCol'
          )
        ], row=True, id='tabModeForm')
stokes = dbc.FormGroup([
          dbc.Label('Stokes products to record', width=labelWidth, id='stokesRowL'),
          dbc.Col(
            dcc.Dropdown(
                options=[], searchable=False,
                   clearable=False, id='stokesRow'
            ), width=dropWidth
          )
        ], row=True, id='stokesForm')
obsTime = dbc.FormGroup([
            dbc.Label('Observation time (in seconds)', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text',
                          id='obsTimeRow',
                          value=defaultParams['obsTime']
                ), width=inpWidth
            )
          ], row=True)

calTime = dbc.FormGroup([
            dbc.Label('Calibrator duration (in seconds)', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text',
                          id='calTimeRow',
                          value=defaultParams['calTime']
                ), width=inpWidth
            )
          ], row=True)

Ncal = dbc.FormGroup([
            dbc.Label('No. of calibrator observations', width=labelWidth),
            dbc.Col(
                dbc.Input(type='number',
                          id='nCalRow',
                          value=defaultParams['Ncal']
                ), width=inpWidth
            )
        ], row=True)


Ncore = dbc.FormGroup([
            dbc.Label('No. of core stations (0 - 24)', width=labelWidth),
            dbc.Col(
                dbc.Input(type='number',
                          id='nCoreRow',
                          value=defaultParams['Ncore']
                ), width=inpWidth
            )
        ], row=True)
Nremote = dbc.FormGroup([
            dbc.Label('No. of remote stations (0 - 14)', width=labelWidth,
                      id='nRemoteRowL'
            ),
            dbc.Col(
                dbc.Input(type='number',
                          id='nRemoteRow',
                          value=defaultParams['Nremote']
                ), width=inpWidth
            )
        ], row=True, id='nRemoteForm')
Nint = dbc.FormGroup([
            dbc.Label('No. of international stations (0 - 14)', width=labelWidth,
                      id='nIntRowL'
            ),
            dbc.Col(
                dbc.Input(type='number',
                          id='nIntRow',
                          value=defaultParams['Nint']
                ), width=inpWidth
            )
        ], row=True, id='nIntForm')
Nchan = dbc.FormGroup([
          dbc.Label('Number of channels per subband', width=labelWidth),
          dbc.Col(
            dcc.Dropdown(
                options=[
                    {'label':'64', 'value':'64'},
                    {'label':'128', 'value':'128'},
                    {'label':'256', 'value':'256'}
                ], value=defaultParams['Nchan'], searchable=False,
                   clearable=False, id='nChanRow'
            ), width=dropWidth
          )
        ], row=True)
Nsb = dbc.FormGroup([
            dbc.Label('Number of subbands', width=labelWidth),
            dbc.Col(
                dbc.Input(type='number',
                          id='nSbRow',
                          value=defaultParams['Nsb']
                ), width=inpWidth
            )
        ], row=True)
intTime = dbc.FormGroup([
            dbc.Label('Integration time (in seconds)', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text',
                          id='intTimeRow',
                          value=defaultParams['intTime']
                ), width=inpWidth
            )
        ], row=True)
hbaDual = dbc.FormGroup([
            dbc.Label('Antenna set', width=labelWidth),
            dbc.Col(
                dcc.Dropdown(
                    options=[
                        {'label':'LBA Outer', 'value':'lbaouter'},
                        {'label':'HBA Dual', 'value':'hbadual'},
                        {'label':'HBA Dual Inner', 'value':'hbadualinner'}
                    ], value=defaultParams['hbaDual'], searchable=False,
                       clearable=False, id='hbaDualRow',
                ), width=dropWidth
            )
          ], row=True)
buttons = html.Div([
            dbc.Row([
                dbc.Col(),
                dbc.Col(dbc.Button('Calculate', id='calculate', color='dark')),
                dbc.Col(dbc.Button('Generate PDF', id='genpdf', color='dark'))
            ])
          ])
link = html.Div([
          html.A(id='download-link',
                 children='Download file',
                 style={'display':'none'}
          )
       ])
obsGUISetup = dbc.Form([obsMode, tabMode, stokes, obsTime, calTime, Ncal, Ncore, Nremote, Nint, Nchan,
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
            dbc.Label('Pipeline', width=labelWidth-inpWidth),
            dbc.Col(
                dcc.Dropdown(
                    options=[
                        {'label':'None', 'value':'none'},
                        {'label':'Preprocessing', 'value':'preprocessing'},
                        {'label':'Pulsar pipeline', 'value':'pulp'},

                        #{'label':'Prefactor', 'value':'prefactor'}
                    ], value=defaultParams['pipeType'], searchable=False,
                       clearable=False, id='pipeTypeRow'
                ), width=dropWidth
            )
          ], row=True)
tAvg = dbc.FormGroup([
           dbc.Label('Time averaging factor', width=labelWidth-inpWidth,
                     id='tAvgRowL'
           ),
           dbc.Col(
            dbc.Input(type='number',
                      id='tAvgRow',
                      min=0,
                      value=defaultParams['tAvg']
            ), width=inpWidth
           )
       ], row=True)
fAvg = dbc.FormGroup([
           dbc.Label('Frequency averaging factor', width=labelWidth-inpWidth,
                     id='fAvgRowL'
           ),
           dbc.Col(
            dcc.Dropdown(
                    options=[
                        {'label':'1', 'value':1},
                        {'label':'2', 'value':2},
                        {'label':'4', 'value':4},
                        {'label':'8', 'value':8},
                        {'label':'16', 'value':16},
                        {'label':'32', 'value':32},
                        {'label':'64', 'value':64},
                        {'label':'128', 'value':128},
                        {'label':'256', 'value':256}
                    ], value=defaultParams['fAvg'],
                       clearable=False, id='fAvgRow',
                ), width=dropWidth


#            dbc.Input(type='number',
#                      id='fAvgRow',
#                      min=0,
#                      value=defaultParams['fAvg']
#            ), width=inpWidth
           )
       ], row=True)
dyCompress = dbc.FormGroup([
                dbc.Label('Enable dysco compression?', width=labelWidth-inpWidth,
                          id='dyCompressRowL'
                ),
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                            {'label':'Disable', 'value':'disable'},
                            {'label':'Enable', 'value':'enable'}
                        ], value=defaultParams['dyCompress'], searchable=False,
                           clearable=False, id='dyCompressRow'
                    ), width=dropWidth
                )
             ], row=True)
pipeGUISetup = dbc.Form([pipeType, tAvg, fAvg, dyCompress])

###############################################################################
# Define the layout of the pulp setup
###############################################################################

tAvgPulp = dbc.FormGroup([
           dbc.Label('Length of subintegration (sec)', width=labelWidth-inpWidth,
                     id='tAvgPulpRowL'
           ),
           dbc.Col(
            dbc.Input(type='number',
                      id='tAvgPulpRow',
                      min=0,
                      value=defaultParams['tAvgPulp']
            ), width=inpWidth
           )
       ], row=True)


rawTo8bitPulp = dbc.FormGroup([
           dbc.Label('Convert raw data to 8-bit', width=labelWidth-inpWidth,
                     id='8bitRowL'
           ),
           dbc.Col(
            dcc.Dropdown(
                    options=[
                        {'label':'YES', 'value':'YES'},
                        {'label':'NO', 'value':'NO'},
                        {'label':'ONLY', 'value':'ONLY'},
                    ], value=defaultParams['8bit'],
                       clearable=False, id='8bitRow',
                ), width=dropWidth
           )
       ], row=True)

digifilPulp =  dbc.FormGroup([
           dbc.Label('Run digifil', width=labelWidth-inpWidth,
                     id='digifilRowL'
           ),
           dbc.Col(
            dcc.Dropdown(
                    options=[
                        {'label':'YES', 'value':'YES'},
                        {'label':'NO', 'value':'NO'},
                    ], value=defaultParams['digifil'],
                       clearable=False, id='digifilRow',
                ), width=dropWidth
                           )
       ], row=True)

pdmpPulp =  dbc.FormGroup([
           dbc.Label('Skip pdmp', width=labelWidth-inpWidth,
                     id='pdmpRowL'
           ),
           dbc.Col(
            dcc.Dropdown(
                    options=[
                        {'label':'YES', 'value':'YES'},
                        {'label':'NO', 'value':'NO'},
                    ], value=defaultParams['no_pdmp'],
                       clearable=False, id='pdmpRow',
                ), width=dropWidth
                           )
       ], row=True)

singlePulsePulp =  dbc.FormGroup([
           dbc.Label('Single pulse search', width=labelWidth-inpWidth,
                     id='singlePulseRowL'
           ),
           dbc.Col(
            dcc.Dropdown(
                    options=[
                        {'label':'YES', 'value':'YES'},
                        {'label':'NO', 'value':'NO'},
                    ], value=defaultParams['single_pulse'],
                       clearable=False, id='singlePulseRow',
                ), width=dropWidth
                           )
       ], row=True)

rratsPulp =  dbc.FormGroup([
           dbc.Label('Search for RRATS', width=labelWidth-inpWidth,
                     id='rratsRowL'
           ),
           dbc.Col(
            dcc.Dropdown(
                    options=[
                        {'label':'YES', 'value':'YES'},
                        {'label':'NO', 'value':'NO'},
                    ], value=defaultParams['rrats'],
                       clearable=False, id='rratsRow',
                ), width=dropWidth
                           )
       ], row=True)




pipeGUISetupPulp = dbc.Form([rawTo8bitPulp, digifilPulp, pdmpPulp, tAvgPulp, singlePulsePulp , rratsPulp   ])




###############################################################################
# Define the layout of the target setup
###############################################################################
targetToolTip = 'Multiple co-observing targets can be specified as ' + \
                'comma-separated values. Note that the number of targets ' + \
                '(pointings) times the number of subbands must be less than 488.'
targetName = dbc.FormGroup([
                dbc.Label('Target', width=labelWidth-inpWidth,
                          id='targetNameRowL'
                ),
                dbc.Tooltip(targetToolTip, target='targetNameRowL'),
                dbc.Tooltip(targetToolTip, target='targetNameRow'),
                dbc.Col(
                   dbc.Input(id='targetNameRow', min=0),
                   width=inpWidth
                ),
                dbc.Col(
                   dbc.Button('Resolve', id='resolve', color='dark')
                ),
             ], row=True)
targetCoord = dbc.FormGroup([
                 dbc.Label('Coordinates', width=labelWidth-inpWidth),
                 dbc.Col(dbc.Input(id='coordRow'), width=inpWidth*2)
              ], row=True)
Nrings = dbc.FormGroup([
            dbc.Label('No. of TAB rings (0 - 8)', width=labelWidth-inpWidth,
                      id='nRingsRowL'),
            dbc.Col(
                dbc.Input(type='number',
                          id='nRingsRow',
                          value=defaultParams['Nrings']
                ), width=inpWidth,
            )
         ], row=True, id='nRingsForm')
obsDate = dbc.FormGroup([
             dbc.Label('Observation date', width=labelWidth-inpWidth),
             dbc.Col(dcc.DatePickerSingle(date=date.today(),
                                          display_format='DD/MM/YYYY',
                                          id='dateRow')
             )
          ], row=True)
calListToolTip = 'Calibrators are not taken into account in the final data sizes'
calList = dbc.FormGroup([
             dbc.Label('Calibrators', width=labelWidth-inpWidth, id='calListRowL'),
             dbc.Tooltip(calListToolTip, target='calListRowL'),
             dbc.Col(dcc.Dropdown(
                        options=[
                             {'label':'3C48', 'value':'3C48'},
                             {'label':'3C147', 'value':'3C147'},
                             {'label':'3C196', 'value':'3C196'},
                             {'label':'3C295', 'value':'3C295'}
                        ], searchable=True, clearable=True,
                           id='calListRow', multi=True
                     ), width=dropWidth
             )
          ], row=True)
demixList = dbc.FormGroup([
               dbc.Label('A-team sources', width=labelWidth-inpWidth),
               dbc.Col(dcc.Dropdown(
                        options=[
                             {'label':'VirA', 'value':'VirA'},
                             {'label':'CasA', 'value':'CasA'},
                             {'label':'CygA', 'value':'CygA'},
                             {'label':'TauA', 'value':'TauA'}
                        ], searchable=True, clearable=True,
                           id='demixListRow', multi=True
                     ), width=dropWidth
             )
          ], row=True)
targetGUISetup = dbc.Form([targetName, targetCoord, Nrings, obsDate, calList, demixList])
pipeGUIFrame = html.Div(children=[
                html.H3('Target setup'),
                html.Hr(),
                targetGUISetup,
                html.H3('Pipeline setup'),
                html.Hr(),
                pipeGUISetup,
                pipeGUISetupPulp,
               ], style={'width':'95%', 'padding':'20px'})

###############################################################################
# Layout of the results tab
###############################################################################
imNoise = dbc.FormGroup([
            dbc.Label('Theoretical image sensitivity (uJy/beam)', width=labelWidth,
                      id='imNoiseRowL'),
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
warntext = \
"""
**Notes:**

The various features of this calculator are documented on the [LOFAR Imaging Cookbook](https://support.astron.nl/LOFARImagingCookbook/calculator.html).

The sensitivity calculation performed by this tool follow [SKA Memo 113](http://www.skatelescope.org/uploaded/59513_113_Memo_Nijboer.pdf) by Nijboer, Pandey-Pommier & de Bruyn. It uses theoretical SEFD values. So, please use it with caution.

LUCI (version 20200114) was written and is maintained for the LOFAR Science Operations & Support group by Sarrvesh Sridhar. The source code is publicly available on [GitHub](https://github.com/scisup/LOFAR-calculator). For comments and/or feature requests, please contact the Science Operations & Support group using the [Helpdesk](https://support.astron.nl/rohelpdesk).
"""
cautiontext = html.Div([
                  dcc.Markdown(children=warntext)
              ], style={'width':'90%'})
resultGUISetup = dbc.Form([imNoise, rawSize, pipeSize, pipeProcTime, cautiontext])
resultGUIFrame = html.Div(children=[
                    html.H3('Results'),
                    html.Hr(),
                    resultGUISetup
                 ], style={'width':'95%', 'padding':'20px'})

###############################################################################
# Layout of the graph
###############################################################################
graph = html.Div([
        dbc.Row([
           dbc.Col(
              html.Div([
                 dcc.Graph(id='elevation-plot',
                           figure={'layout':{'title':'Target visibility plot'}},
                           style={'height':600}
                 )
              ]), width=7
           ),
           dbc.Col(
              html.Div([
                 dcc.Graph(id='beam-plot',
                           figure={'layout':{'title':'Beam Layout'}},
                           style={'height':600},
                           config={
                              'modeBarButtonsToRemove':\
                                  ['toggleSpikelines', \
                                   'hoverCompareCartesian', \
                                   'hoverClosestCartesian' \
                                  ]
                           }
                 )
              ]), width=5
           )
        ]),
        dbc.Row([
           dbc.Col(
              html.Div([
                 dcc.Graph(id='distance-table')
              ]), width=7
           )
        ])
        ])

###############################################################################
# Define the layout of the calculator
###############################################################################
layout = html.Div([dbc.Row(dbc.Col(header)),
                   dbc.Row([dbc.Col(obsGUIFrame),
                            dbc.Col(pipeGUIFrame),
                            dbc.Col(resultGUIFrame)
                   ]),
                   graph,

                   msgBoxTAvg, msgBoxFAvg,
                   msgBoxResolve, msgBoxGenPdf, msgBox
         ])
