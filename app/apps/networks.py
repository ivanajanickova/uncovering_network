import dash
import dash_html_components as html
import dash_core_components as dcc
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output
import json
import dash_cytoscape as cyto
import pathlib
from app import app
from app import server

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


with open(DATA_PATH.joinpath('data2021.json')) as json_file:
    data2021 = json.load(json_file)

with open(DATA_PATH.joinpath('names2021.json')) as json_file:
    names2021 = json.load(json_file)

def generate_elements(data_dict, names_dict):
    elements = []
    for cik1 in data_dict.keys():
        issuers_dict1 = data_dict.get(cik1)
        issuers_set1 = set(issuers_dict1.keys())

        for cik2 in data_dict.keys():
            issuers_dict2 = data_dict.get(cik2)
            issuers_set2 = set(issuers_dict2.keys())
            common = issuers_set1.intersection(issuers_set2)

            if (bool(common) and cik1 != cik2):
                e1 = {'data' : {'id': cik1, 'label' : names_dict.get(cik1)}}
                e2 = {'data' : {'id': cik2, 'label' : names_dict.get(cik2)}}
                e3 = {'data': {'source': cik1, 'target': cik2}}
                elements.append(e1)
                elements.append(e2)
                elements.append(e3)
    return elements




# App Layout & Callbacks
layout = html.Div([

    html.Div(className='two columns', children=[
        dcc.Dropdown(
            id='year-selection',
            options=[
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
                {'label': '2021', 'value': '2021'}
            ],
            value='2021'
        ),
    ]),

    html.Div(className='ten columns', children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=generate_elements(data2021, names2021),
            layout={'name': 'random'},
            style={'width': '1000px', 'height': '1000px'}
        )
    ])
])


@app.callback(
    Output('cytoscape', 'elements'),
    Input('year-selection', 'value'),
)
def update_nodes(year_value):
    with open(DATA_PATH.joinpath('data' + str(year_value) + '.json')) as json_file:
        data = json.load(json_file)
    with open(DATA_PATH.joinpath('names' + str(year_value) + '.json')) as json_file:
        names = json.load(json_file)

    elements = generate_elements(data, names)

    return elements