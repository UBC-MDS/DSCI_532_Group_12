import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import locale
import altair as alt

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
        Output("chart_confirmed_trend", "srcDoc"),
        Output("chart_deaths_trend", "srcDoc"),
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

        c_chart = rp_plot_trend(country, number_type="total", case_type=1)
        d_chart = rp_plot_trend(country, number_type="total", case_type=2)
        return confirmed, recovered, deaths, c_chart, d_chart

    def rp_plot_trend(country, number_type="total", case_type=1):
        data = data_reader.get_timeserie_data_by_country(country, case_type)
        if case_type == 1:
            chart_title = "Cases over time"
        elif case_type == 2:
            chart_title = "Deaths over time"

        chart = (
            alt.Chart(
                data,
                title=alt.TitleParams(text=chart_title, subtitle=country),
                height=200,
            )
            .mark_line()
            .encode(x=alt.X("date:T", title=""), y=alt.Y(number_type + ":Q", title=""))
            .configure_axis(grid=False)
            .configure_title(anchor="start")
        )
        return chart.to_html()

    def rp_create_card(card_title, card_content, content_id):
        """create a dbc.Card object with title and content

        Args:
            card_title (string): title
            card_content (string): short content

        Returns:
            dbc.Card: card object
        """
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H5(card_title, className="card-title"),
                    html.P(card_content, className="card-text", id=content_id),
                ]
            )
        )
        return card

    panel = html.Div(
        [
            dbc.Row(dbc.Col(html.H1("Country"))),
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
                        id="dd_country",
                        options=data_reader.get_country_options(),
                        value="Canada",
                    )
                )
            ),
            dbc.Row(
                [
                    dbc.Col(rp_create_card("Total cases", "", "lb_confirmed")),
                    dbc.Col(rp_create_card("Recovered", "", "lb_recovered")),
                    dbc.Col(rp_create_card("Deaths", "", "lb_deaths")),
                ]
            ),
            dbc.Row(
                dbc.Col(
                    [
                        html.Iframe(
                            id="chart_confirmed_trend",
                            style={
                                "border-width": "0",
                                "width": "100%",
                                "height": "300px",
                            },
                        )
                    ]
                ),
            ),
            dbc.Row(
                dbc.Col(
                    html.Iframe(
                        id="chart_deaths_trend",
                        style={
                            "border-width": "0",
                            "width": "100%",
                            "height": "200",
                        },
                    )
                )
            ),
        ]
    )
    return panel


# endregion

# region Setup app and layout/frontend
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
alt.themes.enable("ggplot2")
app.title = "Covid-19 Data Portal"
app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Div([html.H1("Covid Data Portal")]), className="heading")),
        dbc.Row(
            [
                dbc.Col([left_panel()], width=3, className="panel"),
                dbc.Col([mid_panel()], width=6, className="panel"),
                dbc.Col([right_panel()], width=3, className="panel"),
            ]
        ),
    ],
    fluid=True,
)

# endregion

if __name__ == "__main__":
    app.run_server(debug=True)  # activate hot reloading
