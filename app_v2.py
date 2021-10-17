import numpy as np
import funcs as fun
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash import Dash,dcc,html,Output,Input
#import dash_core_components as dcc
#import dash_html_components as html
#from dash.dependencies import Output, Input

app = Dash(__name__)

#Layout Data
p1 = dict({'ss':'Slit Width = ', 'ds':'Slit Width = ', 'w':'Wire Diameter = ',
           '1dg':'Slit Width = ', 'c':'Radius = ', 'tg':'Side = ', 'sq':'Side = ', '2dg':'Slit Width = ', 'hex':'None'})
p2 = dict({'ss':'None', 'ds':'Separation = ', 'w':'None',
           '1dg':'None', 'c':'None', 'tg':'None', 'sq':'None', '2dg':'None', 'hex':'None'})

#Layout
app.layout = html.Div([

    html.H1("Fraunhofer Diffraction Patterns (v0.1)", style={'text-align': 'center'}),
    html.Div(id='fixed',children='Fixed Parameters : Wavelength = 532 nm, z = 1.5 m, Beam profile - Gaussian, Beam waist = 100 microns'),
    html.Br()
    dcc.Dropdown(
        id='Slit Type',
        options = [
            {'label':'Single Slit', 'value':'ss'},
            {'label':'Double Slit', 'value':'ds'},
            {'label':'Wire', 'value':'w'},
            {'label':'1-d Grating', 'value':'1dg'},
            {'label':'Circular', 'value':'c'},
            {'label':'Triangular', 'value':'tg'},
            {'label':'Square', 'value':'sq'},
            {'label':'2-d Grating', 'value':'2dg'},
            {'label':'Hexagon', 'value':'hex'}
        ],
        value = 'ss'
    ),
    html.Br(),
    html.Div(id='param1', children=[]),
    dcc.Slider(
        id='Slit Width',
        min=8,
        max=256,
        step=8,
        value=32,
    ),
    html.Div(id='param2', children=[]),
    dcc.Slider(
        id='Slit Separation',
        min=8,
        max=256,
        step=8,
        value=64,
    ),

    #html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='plots', figure={}),
    

])

#Callback
@app.callback(
    [Output(component_id='plots', component_property='figure'),
     Output(component_id='Slit Width', component_property='min'),
     Output(component_id='Slit Width', component_property='max'),
     Output(component_id='Slit Width', component_property='step'),
     Output(component_id='param1', component_property='children'),
     Output(component_id='param2', component_property='children')],
    [Input(component_id='Slit Width', component_property='value'),
     Input(component_id='Slit Separation', component_property='value'),
     Input(component_id='Slit Type', component_property='value'),]
)
def update_plots(a,d,st):
    fig,amin,amax,astep = fun.plot(st,a,d)
    val1 = ''
    val2 = ''

    if p1[st] != 'None':
        val1 = str(a)+' microns'
    if p2[st] != 'None':
        val2 = str(d)+' microns'

    return go.Figure(data=fig),amin,amax,astep,p1[st]+val1,p2[st]+val2
if __name__ == '__main__':
    app.run_server(debug=True)

