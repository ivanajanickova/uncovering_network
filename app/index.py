import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import networks, piecharts


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Top Investment Managers|', href='/apps/piecharts'),
        dcc.Link('Networks', href='/apps/networks'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/networks':
        return networks.layout
    if pathname == '/apps/piecharts':
        return piecharts.layout
    else:
        return piecharts.layout


if __name__ == '__main__':
    app.run_server(debug=False)