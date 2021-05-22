import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output
import json
from app import app
from app import server
import pathlib
import plotly.express as px


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH  = PATH.joinpath("../datasets").resolve()


with open(DATA_PATH.joinpath('data2018.json')) as json_file:
    data_dict = json.load(json_file)

with open(DATA_PATH.joinpath('names2018.json')) as json_file:
    names_dict = json.load(json_file)


issuers_dict = data_dict.get('0000038777')
df = pd.DataFrame(list(issuers_dict.items()), columns=['Company', 'Total amount'])


# App Layout & Callbacks
layout = html.Div([

    html.Div([
        dcc.Dropdown(
            id='left-year-selection',
            options=[
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ],
            value='2018'
        ),

        dcc.Dropdown(
            id='left-cik-selection',
            options=[{'label': i, 'value': i} for i in data_dict.keys()],
            value='0001126328',
            placeholder='Select a CIK'
        ),

        dcc.Graph(id='left-graph'),

        html.Div(id="left-total")

    ],
        style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='right-year-selection',
            options=[
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ],
            value='2018'
        ),
        dcc.Dropdown(
            id='right-cik-selection',
            options=[{'label': i, 'value': i} for i in data_dict.keys()],
            value='0001126328',
            placeholder='Select a CIK'
        ),

        dcc.Graph(id='right-graph'),

        html.Div(id="right-total")

    ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'})

]
)


@app.callback(
    Output('left-graph', 'figure'),
    Input('left-year-selection', 'value'),
    Input('left-cik-selection', 'value'))
def update_graph(year_value, cik_value):
    directory = DATA_PATH.joinpath('data' + str(year_value) + '.json')
    directory2 = DATA_PATH.joinpath('names' + str(year_value) + '.json')

    with open(directory) as json_file:
        data_dict = json.load(json_file)

    with open(directory2) as json_file2:
        names_dict = json.load(json_file2)

    companyname = names_dict.get(cik_value)

    issuers_dict = data_dict.get(cik_value)
    df = pd.DataFrame(list(issuers_dict.items()), columns=['Company', 'Total amount'])
    df10 = df.nlargest(10, columns='Total amount')

    fig = px.pie(df10, values='Total amount', names='Company', color_discrete_sequence=px.colors.sequential.RdBu,
                 title=companyname)
    fig.update_traces(hoverinfo='label+percent', textinfo='value')
    fig.update_layout(legend_font_size=5)

    return fig


@app.callback(
    Output("left-total", "children"),
    Input('left-year-selection', 'value'),
    Input('left-cik-selection', 'value'))
def update_output(year_value, cik_value):
    directory = DATA_PATH.joinpath('data' + str(year_value) + '.json')
    with open(directory) as json_file:
        data_dict = json.load(json_file)

    issuers_dict = data_dict.get(cik_value)
    df = pd.DataFrame(list(issuers_dict.items()), columns=['Company', 'Total amount'])

    total = df['Total amount'].sum()

    return u'Total amount of stocks: {:,}'.format(total)


@app.callback(
    Output('right-graph', 'figure'),
    Input('right-year-selection', 'value'),
    Input('right-cik-selection', 'value'))
def update_graph(year_value, cik_value):
    directory = DATA_PATH.joinpath('data' + str(year_value) + '.json')
    directory2 = DATA_PATH.joinpath('names' + str(year_value) + '.json')

    with open(directory) as json_file:
        data_dict = json.load(json_file)

    with open(directory2) as json_file2:
        names_dict = json.load(json_file2)

    companyname = names_dict.get(cik_value)

    issuers_dict = data_dict.get(cik_value)
    df = pd.DataFrame(list(issuers_dict.items()), columns=['Company', 'Total amount'])
    df10 = df.nlargest(10, columns='Total amount')

    fig = px.pie(df10, values='Total amount', names='Company', color_discrete_sequence=px.colors.sequential.RdBu,
                 title=companyname)
    fig.update_traces(hoverinfo='label+percent', textinfo='value')
    fig.update_layout(legend_font_size=5)

    return fig


@app.callback(
    Output("right-total", "children"),
    Input('right-year-selection', 'value'),
    Input('right-cik-selection', 'value'))
def update_output(year_value, cik_value):
    directory = DATA_PATH.joinpath('data' + str(year_value) + '.json')

    with open(directory) as json_file:
        data_dict = json.load(json_file)

    issuers_dict = data_dict.get(cik_value)
    df = pd.DataFrame(list(issuers_dict.items()), columns=['Company', 'Total amount'])
    high = df.nlargest(1, columns='Total amount')

    total = df['Total amount'].sum()

    return u'Total amount of stocks: {:,}'.format(total)


@app.callback(
    Output('left-cik-selection', 'options'),
    Input('left-year-selection', 'value'))
def update_left_dropdown(year_value):
    directory = DATA_PATH.joinpath('data' + str(year_value) + '.json')

    with open(directory) as json_file:
        data_dict = json.load(json_file)

    return [{'label': i, 'value': i} for i in data_dict.keys()]


@app.callback(
    Output('right-cik-selection', 'options'),
    Input('right-year-selection', 'value'))
def update_left_dropdown(year_value):
    directory = DATA_PATH.joinpath('data' + str(year_value) + '.json')

    with open(directory) as json_file:
        data_dict = json.load(json_file)

    return [{'label': i, 'value': i} for i in data_dict.keys()]