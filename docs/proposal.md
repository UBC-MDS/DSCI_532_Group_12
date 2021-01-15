# Covid-19 Data Portal

## Motivation and purpose

## Description of the data

We will be visualizing the COVID-19 data from John Hopkins University's CSSE GIS and Data github repository. The data mainly consists of two primary portions, which are the daily cases summary and the time series data for confirmed cases, death, recovered cases. Our dashboard data summary such as confirmed cases by countries, death by countries and recovered by countries will come from the <a href=https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports>CSSE COVID-19 Daily Reports</a>, and the trend of confirmed cases, recovered cases and death will be coming from <a href=https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series>CSSE COVID-19 Time Series</a>.

The daily report data is updated on daily basis, which contains `FIPS, Admin2,Province_State, Country_Region, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered,Active, Combined_Key, Incident_Rate, Case_Fatality_Ratio` columns. We will be using this data to generate our geographical summary map and case statistics on the dashboard.

The time series data are collected from the daily report data. Three time series tables are for the global confirmed cases, recovered cases and deaths. Australia, Canada and China are reported at the province/state level. Dependencies of the Netherlands, the UK, France and Denmark are listed under the province/state level. The US and other countries are at the country level. The time series data will be used for generating the trend of cases. 
## Research questions and usage scenarios

The dashboard lets its users explore the trends of Covid-19's cases around the world, it helps to answer some descriptive questions related to this pandemic:

-   How many cases confirmed globally since the beginning of the pandemic?

-   Which countries have the highest cumulative confirmed cases?

-   Which countries have the highest death rate?

-   What does the trend of globally confirmed cases look like?

-   What does the trend of confirmed cases look like for a certain country?

-   How is the trend of Covid-19 related deaths at globaly scale and local scale?

Some typical usage scenarios can be described as below.

Alex is a pilot in the Philippine who lost his job in early 2020 due to all the travel bans, he has been doing surviving jobs since but his heart always longs for the sky. Alex wants to be able to keep track of the pandemic's statistics not only in his home country but also around the world, so that he will be able to plan for his career better once things get better or worse.

When Alex logs onto the Covid-19 Data Portal, he will see the overall number of confirmed cases, deaths and recovered cases globally, there is also a world map illustrating where the pandemic hits the most (high number of confirmed case). Alex will be able to see the recovery rate, death in a million for different countries in order to know if some countries are doing better than others related to treatment. Alex can filter new confirmed cases, new deaths and new recovered cases by his country as well as other neighbor countries to see if there is a new trend or if they are hitting a new wave of infection. Given countries apply different prevention strategies at different times, some already started their vaccination program, Alex will be able to compare the trend before and after a certain date for a certain country.

\

