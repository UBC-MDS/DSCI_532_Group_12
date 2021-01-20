import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import locale
import altair as alt

locale.setlocale(locale.LC_ALL, "")

import data_model as dm

import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir + "/components")
from right_panel import right_panel
from left_panel import left_panel
from mid_panel import mid_panel

# region Read in global data
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
data_reader = dm.data_model(parentdir + "/data/raw")
# endregion

# region Setup app and layout/frontend
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
country_panel = right_panel(data_reader)
global_panel = left_panel(data_reader)
map_panel = mid_panel(data_reader)
alt.themes.enable("ggplot2")
app.title = "Covid-19 Data Portal"
app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Div([html.H1("Covid Data Portal")]), className="heading")),
        dbc.Row(
            [
                dbc.Col([global_panel.render()], width=3, className="panel"),
                dbc.Col([map_panel.render()], width=6, className="panel"),
                dbc.Col(
                    [country_panel.render()],
                    width=3,
                    className="panel",
                ),
            ]
        ),
    ],
    fluid=True,
)

# endregion

# region handle call backs
@app.callback(
    Output("lb_confirmed", "children"),
    Output("lb_recovered", "children"),
    Output("lb_deaths", "children"),
    Output("chart_confirmed_trend", "srcDoc"),
    Output("chart_deaths_trend", "srcDoc"),
    Input("dd_country", "value"),
)
def update_right_panel(country):
    return country_panel.refresh(country)


# endregion

if __name__ == "__main__":
    app.run_server(debug=True)  # activate hot reloading
