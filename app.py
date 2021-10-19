import numpy as np
import funcs as fun
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

app = Dash(__name__)

#Layout Data
p1 = dict({'ss':'Slit Width = ', 'ds':'Slit Width = ', 'w':'Wire Diameter = ',
           '1dg':'Slit Width = ', 'c':'Radius = ', 'tg':'Side = ', 'sq':'Side = ',
           '2dg':'Slit Width = ', 'hex':'None', '2dg2':'Slit Side = ', 'lg':'Relative Angle = '})
p2 = dict({'ss':'None', 'ds':'Separation = ', 'w':'None',
           '1dg':'None', 'c':'None', 'tg':'None', 'sq':'None', '2dg':'None',
           'hex':'None', '2dg2':'None', 'lg':'None'})

#Layout
app.layout = html.Div([

    html.H1("Fraunhofer Diffraction Patterns (v0.1)", style={'text-align': 'center'}),
    html.Div(id='fixed',children='Fixed Parameters : Wavelength = 532 nm, z = 1.5 m, Beam profile - Gaussian, Beam waist = 100 microns'),
    html.Div(id='note',children='(Note : The contrast at output has been slightly exaggerated for better visibility.)'),
    html.Br(),
    dcc.Dropdown(
        id='Slit Type',
        options = [
            {'label':'Single Slit', 'value':'ss'},
            {'label':'Double Slit', 'value':'ds'},
            {'label':'Wire', 'value':'w'},
            {'label':'1-d Grating', 'value':'1dg'},
            {'label':'2-d Grating', 'value':'2dg'},
            {'label':'2-d Grating, Type 2', 'value':'2dg2'},
            {'label':'Laser Grating', 'value':'lg'},
            {'label':'Circular', 'value':'c'},
            {'label':'Triangular', 'value':'tg'},
            {'label':'Square', 'value':'sq'},
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
        marks={},
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
    #html.Br(),

    dcc.Graph(id='plots', figure={}),
    html.Img(id='image', src=[],height=262,width=315),
    html.Div(children='Actual image'),
    html.Br(), html.Br(),
    html.Div(id='contact', children='Please report any problems to harishss@iitk.ac.in. Thanks! The source code can be found '),
    html.A(id='url',children='here.', href='https://github.com/harishss3/Diffraction')

])

#Callback
@app.callback(
    [Output(component_id='plots', component_property='figure'),
     Output(component_id='Slit Width', component_property='min'),
     Output(component_id='Slit Width', component_property='max'),
     Output(component_id='Slit Width', component_property='step'),
     Output(component_id='param1', component_property='children'),
     Output(component_id='param2', component_property='children'),
     Output(component_id='Slit Width', component_property='marks'),
     Output(component_id='image', component_property='src')],
    [Input(component_id='Slit Width', component_property='value'),
     Input(component_id='Slit Separation', component_property='value'),
     Input(component_id='Slit Type', component_property='value'),]
)
def update_plots(a,d,st):
    fig,amin,amax,astep = fun.plot(st,a,d)

    if st != 'tg':
        source = None
    else:
        source = app.get_asset_url('triangle.jpg')

    if st != 'lg':
        mks = dict()
    else:
        mks = dict({36.9:'36.9', 53.1:'53.1'})

    val1 = ''
    val2 = ''

    if p1[st] != 'None':
        val1 = str(a)+' microns'
        if p1[st] == 'lg':
            val1 = str(a) + ' degrees'
    if p2[st] != 'None':
        val2 = str(d)+' microns'

    return go.Figure(data=fig),amin,amax,astep,p1[st]+val1,p2[st]+val2,mks,source
if __name__ == '__main__':
    app.run_server(debug=True)
