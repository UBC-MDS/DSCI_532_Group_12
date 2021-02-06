from altair.vegalite.v4.schema.core import Padding
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import locale
import altair as alt
from vega_datasets import data as dt

from panel import panel

locale.setlocale(locale.LC_ALL, "")

import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import data_model as dm


class mid_panel(panel):
    """handle all activities related to world map panel"""

    def __init__(self, datamodel):
        super().__init__("World Map", datamodel)

        self.content = dbc.Col(
            [
                dbc.Row(dbc.Col(self.__create_button_groups())),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Iframe(
                                id="world_map",
                                style={
                                    "border-width": "0",
                                    "width": "100%",
                                    "height": "570px",
                                    "padding-left": "3px",
                                },
                            )
                        ],
                        width=12,
                    ),
                ),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Iframe(
                                id="chart_global_trend",
                                style={
                                    "border-width": "0",
                                    "width": "100%",
                                    "height": "300px",
                                    "padding-left": "3px",
                                },
                            )
                        ],
                        width=12,
                    ),
                ),
            ],
            width=12,
        )

    def refresh(self, chart_type="confirmed", ntype="Total"):
        """Aggregate the country level data

        Args:
            chart_type (string): selected chart type from buttons

        Returns:
            a ranking bar chart of confirmed cases/death cases/recovered cases
        """

        # result = self.data_reader.get_aggregated_daily_report()
        confirmed_data = self.data_reader.times_series_confirmed_tidy
        # active_data = result[['Country_Region', 'Active']]
        recovered_data = self.data_reader.times_series_recovered_tidy
        deaths_data = self.data_reader.times_series_death_tidy

        if chart_type == "confirmed":
            data = confirmed_data
        elif chart_type == "recovered":
            data = recovered_data
        elif chart_type == "death":
            data = deaths_data
        # data.columns =['Country_Region', 'Cases']
        world_map = self.__create_world_map_chart(data, chart_type.title())

        trend_chart = self.__create_world_timeseries_chart(chart_type)
        return world_map, trend_chart

    def __create_button_groups(self):
        """Create button

        Returns:
            buttons for three cases
        """
        button_groups = dbc.ButtonGroup(
            [
                dbc.Button("Confirmed", active=True, id="wm_confirmed"),
                dbc.Button("Death", id="wm_death"),
                dbc.Button("Recovered", id="wm_recovered"),
            ],
            size="md",
            className="mr-1",
        )
        return button_groups

    def __create_world_map_chart(self, data, type):
        """Create world map chart

        Args:
            data (data frame): data frame for each cases

            type (string): selected chart type from buttons

        Returns:
            a world map bubble chart of confirmed cases/death cases/recovered cases
        """
        # alt.renderers.set_embed_options(padding = {"left": 0, "right": 0, "bottom": 1, "top":1})

        source = alt.topo_feature(dt.world_110m.url, "countries")
        base = (
            alt.Chart(source, title="")
            .mark_geoshape(fill="lightgray", stroke="white")
            .properties(width=860, height=450)
            .project("equirectangular")
            # .padding({"left": 0, "right": 0, "bottom": 1, "top":1})
        )

        points = (
            alt.Chart(data[data["variable"] == data["variable"].unique().max()])
            .mark_circle()
            .encode(
                longitude="Long:Q",
                latitude="Lat:Q",
                size=alt.Size(
                    "value:Q",
                    title="Number of Cases",
                    scale=alt.Scale(range=[5, 3000]),
                    # legend=None,
                ),
                color=alt.Color("value", scale=alt.Scale(scheme="orangered")),
                tooltip=[
                    alt.Tooltip("Country/Region:N"),
                    alt.Tooltip("value:Q", format=",.0f"),
                ],
            )
        )

        chart = base + points
        chart = chart.configure_legend(orient="bottom").configure_view(
            strokeWidth=0,
        )

        return chart.to_html()

    def __create_world_timeseries_chart(self, case_type, ntype="New"):
        """create trend chart for global numbers

        Args:
            case_type (string): "confirmed", "recovered", "death"
            ntype (string): "Total" or "New"

        Returns:
            a time series chart of confirmed cases/death cases/recovered cases
        """

        if case_type == "confirmed":
            chart_title = "Global Confirmed Cases"
            case_type = 1
        elif case_type == "death":
            chart_title = "Global Deaths"
            case_type = 2
        elif case_type == "recovered":
            chart_title = "Global Recovered Cases"
            case_type = 3
        if ntype == "Total":
            chart_title = chart_title + " Over Time"
        else:
            chart_title = "New " + chart_title + " Per Day"
        data = self.data_reader.get_timeserie_data_by_country("all", case_type)

        chart = (
            alt.Chart(
                data,
                title=alt.TitleParams(text=chart_title),
                height=200,
            )
            .mark_line()
            .transform_filter(alt.FieldEqualPredicate(field="type", equal=ntype))
            .encode(
                x=alt.X("date:T", title="", axis=alt.Axis(format=("%b %Y"))),
                y=alt.Y("count:Q", title=""),
            )
            .configure_axis(grid=False)
            .configure_title(anchor="start")
            .properties(width=790)
        )
        return chart.to_html()