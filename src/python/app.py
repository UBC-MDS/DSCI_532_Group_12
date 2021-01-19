import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import locale

locale.setlocale(locale.LC_ALL, "")

import data_model as dm

# region Read in global data
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
data_reader = dm.data_model(parentdir + "/data/raw")
# endregion

# region Create components
def left_panel():
    """create the left panel (global statistics)

    Returns:
       dash component
    """
    panel = html.Div([html.H1("Global")])
    return panel


def mid_panel():
    """create the middle panel (world map)

    Returns:
        dash component
    """
    panel = html.Div([html.H1("World Map")])
    return panel


def right_panel():
    """create the right panel (country statistics)

    Returns:
        dash component
    """

    @app.callback(
        Output("lb_confirmed", "children"),
        Output("lb_recovered", "children"),
        Output("lb_deaths", "children"),
        Input("dd_country", "value"),
    )
    def update_right_panel(country):
        """update all components on the right panel when changing country selected

        Args:
            country (string): selected country from the dropdownlist

        Returns:
            a tuple (confirmed, recovered, deaths)
        """
        result = data_reader.cumulative_filter(country)
        confirmed = f"{result.Confirmed:n}"
        recovered = f"{result.Recovered:n}"
        deaths = f"{result.Deaths:n}"
        return confirmed, recovered, deaths

    panel = html.Div(
        [
            html.H1("Country"),
            dcc.Dropdown(
                id="dd_country",
                options=data_reader.get_country_options(),
                value="Canada",
            ),
            html.H3("Total cases"),
            html.Label(id="lb_confirmed"),
            html.H3("Recovered"),
            html.Label(id="lb_recovered"),
            html.H3("Deaths"),
            html.Label(id="lb_deaths"),
        ]
    )
    return panel


# endregion

# region Setup app and layout/frontend
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [
        dbc.Row([html.H1("Covid Data Portal")]),
        dbc.Row(
            [
                dbc.Col([left_panel()], width=3),
                dbc.Col([mid_panel()], width=6),
                dbc.Col([right_panel()], width=3),
            ]
        ),
    ],
    fluid=True,
)

# endregion

if __name__ == "__main__":
    app.run_server(debug=True)  # activate hot reloading
