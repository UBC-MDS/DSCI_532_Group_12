from altair.vegalite.v4.schema.core import Padding
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import locale
import altair as alt
from vega_datasets import data as dt
import datetime

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
        current_date = datetime.date.today()
        start_date = current_date - datetime.timedelta(days=180)

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
                        dcc.DatePickerRange(
                            id="global_time_frame",
                            min_date_allowed=datetime.date(2020, 1, 1),
                            max_date_allowed=datetime.date.today(),
                            # initial_visible_month=datetime.date.today(),
                            start_date=start_date,
                            end_date=current_date,
                            stay_open_on_select=True,
                            updatemode="singledate",
                        )
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Iframe(
                                id="chart_global_trend_new",
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
                dbc.Row(
                    dbc.Col(
                        [
                            html.Iframe(
                                id="chart_global_trend_death",
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

    def refresh_global_map(self, chart_type="confirmed"):
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

        return world_map

    def refresh_trend_charts(
        self,
        start_date,
        end_date,
    ):

        new_trend_chart = self.__create_world_timeseries_chart(
            "confirmed", start_date=start_date, end_date=end_date
        )
        death_trend_chart = self.__create_world_timeseries_chart(
            "death", start_date=start_date, end_date=end_date
        )
        return new_trend_chart, death_trend_chart

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

    def __create_world_timeseries_chart(
        self,
        case_type,
        start_date,
        end_date,
    ):
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

        chart_title = "New " + chart_title + " Per Day"
        # data = self.data_reader.get_timeserie_data_by_country("all", case_type)
        # data.date = data.date.astype(str)

        data = self.data_reader.get_timeserie_data_by_country(
            country="all", c_type=case_type, start_date=start_date, end_date=end_date
        )
        data = data.query("type=='New'")

        chart = (
            alt.Chart(
                data,
                title=alt.TitleParams(text=chart_title),
            )
            .mark_line()
            .encode(
                x=alt.X("date:T", title=""),
                y=alt.Y("count:Q", title=""),
                tooltip=alt.Tooltip(["count:Q"], format=",.0f"),
            )
            # .properties(width="container", height="container")
        )
        rolling_mean = (
            alt.Chart(data)
            .mark_line(color="red")
            .transform_window(rolling_mean="mean(count)", frame=[-7, 7])
            .encode(x=alt.X("date:T", title=""), y=alt.Y("rolling_mean:Q", title=""))
        )
        chart = chart + rolling_mean
        chart = (
            chart.configure_axis(grid=False)
            .configure_title(anchor="start")
            .properties(width=790, height=200)
        )
        return chart.to_html()