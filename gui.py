import dash_html_components as html
import dash_bootstrap_components as dbc

###############################################################################
# Layout of the header
###############################################################################
header = html.Div(children=[
            html.H1('LOFAR data size and processing time calculator')
         ], style={'padding':'10px 10px'})

# Parameters common for all 3 sub-panels
labelWidth = 8
inpWidth = 3

###############################################################################
# Layout of observational setup
###############################################################################
hbaDualItems = [dbc.DropdownMenuItem("Disabled", active=True),
                dbc.DropdownMenuItem("Enabled")
               ]
obsTime = dbc.FormGroup([
            dbc.Label('Observation time (in hours)', 
                      html_for='obsTimeRow', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='obsTimeRow', style={'padding':'0px 0px'}), width=inpWidth
            )
          ], row=True)
Ncore = dbc.FormGroup([
            dbc.Label('Number of core stations', 
                      html_for='nCoreRow', width=labelWidth),
            dbc.Col(
                dbc.Input(type='number', id='nCoreRow', min=0, max=24, value=24),
                width=inpWidth
            )
        ], row=True)
Nremote = dbc.FormGroup([
            dbc.Label('Number of remote stations', 
                      html_for='nRemoteRow', width=labelWidth),
            dbc.Col(
                dbc.Input(type='number', id='nRemoteRow', min=0, max=14, value=14), 
                width=inpWidth
            )            
        ], row=True)
Nint = dbc.FormGroup([
            dbc.Label('Number of international stations', 
                      html_for='nIntRow', width=labelWidth),
            dbc.Col(
                dbc.Input(type='number', id='nIntRow', min=0, max=13, value=13), 
                width=inpWidth
            )
        ], row=True)
Nchan = dbc.FormGroup([
            dbc.Label('Number of channels per subband', 
                      html_for='nChanRow', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='nChanRow', value=64), width=inpWidth
            )
        ], row=True)
Nsb = dbc.FormGroup([
            dbc.Label('Number of subbands', 
                      html_for='nSbRow', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='nSbRow', value=488), width=inpWidth
            )
        ], row=True)
intTime = dbc.FormGroup([
            dbc.Label('Integration time (in seconds)', 
                      html_for='intTimeRow', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='intTimeRow', value=1), width=inpWidth
            )
        ], row=True)
hbaDual = dbc.FormGroup([
            dbc.Label('Observe in HBA Dual mode?', 
                      html_for='hbaDualRow', width=labelWidth),
            dbc.Col(
                dbc.DropdownMenu(bs_size='md', 
                                 children=hbaDualItems, label='Disabled'),
                width=inpWidth
            )
        ], row=True)
buttons = html.Div([
            dbc.Row([
                dbc.Col(dbc.Button('Calculate', color='dark')),
                dbc.Col(dbc.Button('Reset', color='dark'))
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
pipeList = [dbc.DropdownMenuItem("None", active=True),
            dbc.DropdownMenuItem("Preprocessing")
           ]
dyCompressList = [dbc.DropdownMenuItem("Disabled"),
                  dbc.DropdownMenuItem("Enabled", active=True)
                 ]
pipeType = dbc.FormGroup([
                dbc.Label('Pipeline', html_for='pipeTypeRow', width=labelWidth),
                dbc.Col(
                    dbc.DropdownMenu(bs_size='md',
                                     children=pipeList, label='None'),
                    width=inpWidth
                )
           ], row=True)
tAvg = dbc.FormGroup([
           dbc.Label('Time averaging factor', html_for='tAvgRow', 
                     width=labelWidth),
           dbc.Col(
            dbc.Input(type='numeric', id='tAvgRow', min=0, value=1), 
            width=inpWidth
           )
       ], row=True)
fAvg = dbc.FormGroup([
           dbc.Label('Frequency averaging factor', html_for='fAvgRow', 
                     width=labelWidth),
           dbc.Col(
            dbc.Input(type='numeric', id='fAvgRow', min=0, value=1), 
            width=inpWidth
           )
       ], row=True)
dyCompress = dbc.FormGroup([
                dbc.Label('Enable dysco compression?', html_for='fAvgRow', 
                          width=labelWidth),
                dbc.Col(
                    dbc.DropdownMenu(bs_size='md', children=dyCompressList, 
                                     label='Enabled'), 
                    width=inpWidth
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
            dbc.Label('Theoretical image noise', 
                      html_for='inNoiseRow', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='inNoiseRow', disabled=True), 
                width=inpWidth
            )
          ], row=True)
rawSize = dbc.FormGroup([
            dbc.Label('Raw data size (in GB)', 
                      html_for='rawSizeRow', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='rawSizeRow', disabled=True), 
                width=inpWidth
            )
          ], row=True)
pipeSize = dbc.FormGroup([
            dbc.Label('Processed data size (in GB)', 
                      html_for='pipeSizeeRow', width=labelWidth),
            dbc.Col(
                dbc.Input(type='text', id='pipeSizeRow', disabled=True), 
                width=inpWidth
            )
          ], row=True)
pipeProcTime = dbc.FormGroup([
                  dbc.Label('Pipeline processing time (in hours)', 
                            html_for='pipeProcTimeRow', width=labelWidth),
                  dbc.Col(
                     dbc.Input(type='text', id='pipeProcTimeRow', 
                               disabled=True), 
                     width=inpWidth
                  )
               ], row=True)
resultGUISetup = dbc.Form([imNoise, rawSize, pipeSize, pipeProcTime])
resultGUIFrame = html.Div(children=[
                    html.H3('Results'),
                    html.Hr(),
                    resultGUISetup
                 ], style={'width':'95%', 'padding':'20px'})

###############################################################################
# Layout of the footer which contains the buttons
###############################################################################
footer = html.Div([
            dbc.Row([
                dbc.Col(dbc.Button('Calculate', id='calculate', color='dark')),
                dbc.Col(dbc.Button('Reset', id='reset', color='dark'))
             ])
         ], style={'width':'20%', 'padding':'0px 20px'})
