#!/usr/bin/env python

__author__ = "Sarrvesh S. Sridhar"
__email__  = "sarrvesh@astron.nl"

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from gui import header, obsGUIFrame, pipeGUIFrame, resultGUIFrame, footer

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

#######################################
# What should the reset button do?
#######################################
#@app.callback(
#    Output('obsTimeTow', 'value'),
#    [Input('reset', 'n_clicks')]
#)
#def on_reset_click(n):
#   """Function defines what to do when the reset button is clicked"""
#   if n is none:
#      # Reset button has not been clicked yet
#      # So, do nothing
#      pass
#   else:
#      return 'x'
      

if __name__ == '__main__':
    app.run_server(debug=True)
