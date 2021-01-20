import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import locale
import altair as alt

from panel import panel

locale.setlocale(locale.LC_ALL, "")

import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import data_model as dm


class right_panel(panel):
    def __init__(self, datamodel):
        super().__init__("Country", datamodel)

        self.content = html.Div(
            [
                dbc.Row(dbc.Col(self.__create_country_dropdown())),
                dbc.Row(
                    [
                        dbc.Col(panel.create_card("Total cases", "", "lb_confirmed")),
                        dbc.Col(panel.create_card("Recovered", "", "lb_recovered")),
                        dbc.Col(panel.create_card("Deaths", "", "lb_deaths")),
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

    def refresh(self, country):
        """update all components on the right panel when changing country selected

        Args:
            country (string): selected country from the dropdownlist

        Returns:
            a tuple (confirmed, recovered, deaths, confirmed chart, death chart)
        """
        result = self.data_reader.cumulative_filter(country)
        confirmed = f"{result.Confirmed:n}"
        recovered = f"{result.Recovered:n}"
        deaths = f"{result.Deaths:n}"

        c_chart = self.__create_timeserie_chart(
            country, number_type="total", case_type=1
        )
        d_chart = self.__create_timeserie_chart(
            country, number_type="total", case_type=2
        )
        return confirmed, recovered, deaths, c_chart, d_chart

    def __create_country_dropdown(self):
        return dcc.Dropdown(
            id="dd_country",
            options=self.data_reader.get_country_options(),
            value="Canada",
        )

    def __create_timeserie_chart(self, country, number_type="total", case_type=1):
        data = self.data_reader.get_timeserie_data_by_country(country, case_type)
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
