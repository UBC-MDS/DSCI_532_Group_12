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


class left_panel(panel):
    def __init__(self, datamodel):
        super().__init__("Global", datamodel)

        self.content = html.Div(
            [
                dbc.Row(dbc.Col(self.__create_button_groups())),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Iframe(
                                id="chart_cases_ranking",
                                style={
                                    "border-width": "0",
                                    "width": "100%",
                                    "height": "800px",
                                },
                            )
                        ]
                    ),
                ),
            ]
        )

    def refresh(self, chart_type="confirmed"):
        """Aggregate the country level data

        Args:
            chart_type (string): selected chart type from buttons

        Returns:
            a ranking bar chart of confirmed cases/death cases/recovered cases
        """

        result = self.data_reader.get_aggregated_daily_report()
        confirmed_data = result[["Country_Region", "Confirmed"]]
        active_data = result[["Country_Region", "Active"]]
        recovered_data = result[["Country_Region", "Recovered"]]
        deaths_data = result[["Country_Region", "Deaths"]]

        if chart_type == "confirmed":
            data = confirmed_data
        elif chart_type == "active":
            data = active_data
        elif chart_type == "recovered":
            data = confirmed_data
        elif chart_type == "death":
            data = confirmed_data
        data.columns = ["Country_Region", "Cases"]
        chart = self.__create_ranking_bar_chart(
            data.nlargest(30, "Cases"), chart_type.title()
        )
        return chart

    def __create_button_groups(self):
        button_groups = dbc.ButtonGroup(
            [
                dbc.Button("Confirmed", active=True, id="btn_confirmed"),
                dbc.Button("Active", id="btn_active"),
                dbc.Button("Death", id="btn_death"),
                dbc.Button("Recovered", id="btn_recovered"),
            ],
            size="md",
            className="mr-1",
        )
        return button_groups

    def __create_ranking_bar_chart(self, data, type):
        chart = (
            alt.Chart(data, title="")
            .mark_bar()
            .encode(
                x=alt.X("Cases", title=" "),
                y=alt.Y("Country_Region", sort="-x", title=" "),
                color=alt.Color("Cases", scale=alt.Scale(scheme="orangered")),
                tooltip=["Cases:Q"],
            )
            .configure_axis(grid=False)
            .configure_title(anchor="start")
        )
        return chart.to_html()