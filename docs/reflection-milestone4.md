# Reflection

## Progress of the dashboard

We have managed to achieve most of the functionalities designed in our initial proposal. In this milestone, we have attempted to cover most of the high and medium priority feedback coming from the TA, Joel, and our peers.

The main improvements are listed as follow:

-   As recommended by our TA's [feedback](https://github.com/UBC-MDS/DSCI_532_Group_12/issues/44), a line graph showing new cases trend is added to the middle panel. This change fills up most of the space under the world map, which makes the layout more balanced

-   We adjusted the scale of the bubbles showing number of cases on the world map to highlight better the difference of Covid-19's impact among countries

-   We removed the scroll-bar from the bar chart ranking Top 30 countries and added global statistics to the left panel

-   We added some spacing among rows of component on the right panel per Joel's feedback

-   A time-stamp showing the last updated date of the data is added

Up to this release, our panel should have the following functionalities:

-   The left panel (Global) contains global statistics and a ranking bar chart which shows Top 30 countries most affected by the pandemic

-   The middle panel (World Map) illustrates the case distribution geographically across the world and a line graph showing new cases trend

-   The right panel shows a country's summary statistics and trends per user selection

## Development Discussion 

There are some improvement opportunities acknowledged but delayed to future development due to the time constraint of this milestone, those can be found below.

-   **New features with substantial development effort**

    -   Allow user to select a time frame for viewing data: it requires changes both to our data access and UI layers

    -   Allow user to switch between total case and case per population: this requires using another data set to get world population, changes to our data access and UI layers

    -   Allow interaction between panels: selecting a country in the world map/selecting a country from the world ranking will display its statistics on the right panel

-   **Persistent layout issues without a technical proper solution**

    -   Horizontal scroll-bar is still displayed when displaying the dashboard on 1920x1080 screen: we tried applying `overflow:hidden` but it will always disable using scroll-bar for all components

-   **Small UI improvements suggested by our peer but not implemented**

    -   Change color palette for different types of case (confirmed, death, recovered): we find our current color scheme (creme, red, white, black, gray) reflect well the situation of the pandemic

    -   Highlight selected buttons: the buttons are currently wrapped by boxes around them, changing css style of those buttons will make the code more complicated to maintain as there is no easy way to do it but addressing that within callback methods (which are already quite complex)
