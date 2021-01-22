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
    def __init__(self, datamodel):
        super().__init__("World Map", datamodel)

        self.content = html.Div(
            [
                dbc.Row(dbc.Col(self.__create_button_groups())),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Iframe(
                                id="world_map",
                                style={
                                    "border-width" : "0",
                                    "width": "1000px",
                                    "height": "1000px"
                                }
                            )
                        ]
                    ),
                )
            ]
        )

    def refresh(self, chart_type="confirmed"):
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
        chart = self.__create_world_map_chart(data, chart_type.title())
        return chart
 
    
    
    def __create_button_groups(self):
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
        source = alt.topo_feature(dt.world_110m.url, 'countries')
        base = alt.Chart(source, title = "").mark_geoshape(
            fill='lightgray',
            stroke='white'
            ).properties(
            width=800,
            height=450
            ).project('equirectangular')
            
        points = alt.Chart(data[data['variable'] == data['variable'].unique().max()]).mark_circle().encode(
                longitude='Long:Q',
                latitude='Lat:Q',
                size=alt.Size('value:Q', 
                               title='Number of Confirmed',
                               scale=alt.Scale(range=[250, 2000]),
                               legend = None),
                color=alt.value('steelblue'),
                tooltip=['Country/Region:N','value:Q']
            )
        
        chart = base + points 
        
        return chart.to_html()
  