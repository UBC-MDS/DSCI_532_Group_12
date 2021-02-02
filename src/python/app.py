import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import locale
import altair as alt

locale.setlocale(locale.LC_ALL, "")

import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)
sys.path.insert(0, currentdir + "/components")

import data_model as dm

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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
# CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA, MINTY, PULSE, SANDSTONE, SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB, SUPERHERO, UNITED, YETI
server = app.server
country_panel = right_panel(data_reader)
global_panel = left_panel(data_reader)
map_panel = mid_panel(data_reader)
alt.themes.enable("ggplot2")
app.title = "Covid-19 Data Portal"
dashboard_heading = (
    "Covid-19 Data Portal (Last Updated: "
    + data_reader.last_updated.strftime("%m/%d/%Y")
    + ")"
)
app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Div([html.H1(dashboard_heading)]), className="heading")),
        dbc.Row(
            [
                dbc.Col([global_panel.render()], width=3, className="left_panel"),
                dbc.Col([map_panel.render()], width=6, className="panel"),
                dbc.Col(
                    [country_panel.render()],
                    width=3,
                    className="right_panel",
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
    Input("rp_btn_total", "n_clicks"),
    Input("rp_btn_new", "n_clicks"),
)
def update_right_panel(country, total_click, new_click):
    ctx = dash.callback_context
    if not ctx.triggered:
        ntype = "Total"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "rp_btn_total":
            ntype = "Total"
        elif button_id == "rp_btn_new":
            ntype = "New"
        else:
            ntype = "Total"

    return country_panel.refresh(country, ntype=ntype)


@app.callback(
    Output("chart_cases_ranking", "srcDoc"),
    Input("btn_active", "n_clicks"),
    Input("btn_confirmed", "n_clicks"),
    Input("btn_death", "n_clicks"),
    Input("btn_recovered", "n_clicks"),
)
def update_left_panel(active, confirmed, death, recovered):
    ctx = dash.callback_context
    if not ctx.triggered:
        ctype = "confirmed"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "btn_confirmed":
            ctype = "confirmed"
        elif button_id == "btn_death":
            ctype = "death"
        elif button_id == "btn_active":
            ctype = "active"
        else:
            ctype = "recovered"
    return global_panel.refresh(chart_type=ctype)


@app.callback(
    Output("world_map", "srcDoc"),
    Output("chart_global_trend", "srcDoc"),
    # Input("btn_active", "n_clicks"),
    Input("wm_confirmed", "n_clicks"),
    Input("wm_death", "n_clicks"),
    Input("wm_recovered", "n_clicks"),
)
def update_mid_panel(confirmed, death, recovered):
    ctx = dash.callback_context
    if not ctx.triggered:
        ctype = "confirmed"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "wm_confirmed":
            ctype = "confirmed"
        elif button_id == "wm_death":
            ctype = "death"
        # elif button_id == "btn_active":
        #     ctype = "active"
        else:
            ctype = "recovered"
    return map_panel.refresh(chart_type=ctype)


# endregion

if __name__ == "__main__":
    app.run_server(debug=True)  # activate hot reloading
