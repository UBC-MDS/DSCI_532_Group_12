# Reflection

## Progress of the dashboard:
Following our initial design and proposal, our team has implemented a dashboard with three panels(left, middle, and right), which is pretty close to our intial design and has covered most of the functionalities we proposed to offer to our user. As instructed by the TA from the <a href=https://github.com/UBC-MDS/DSCI_532_Group_12/issues/35>feedback</a>, we choosed to implement a simpler version of the dashboard. 

The left panel contains a bar chart which shows the user the ranking of case count with the button for user to choose if they want to see (Confirmed Cases, Active Cases, Recovered Cases or Deaths).

In the middle panel, the user could surface the cases distribution geographically in a map, with the options to choose confirmed cases, death cases, or recovered cases. 

In the right panel, the user can check the detailed trend by country and category. Meanwhile, the right panel also shows the user how many cases in the selected category each country currently have. 
## Areas of Improvement/Enhancement for the dashboard:
There are still a couple of points our teams thrive to cover in the next milestone/impelentation.

- Add cumulative statistics at global scale on the left panel
- Allow viewing a country's statistics upon being selected from the map
- Allow filtering by time frame for charts showing trend
- Add some ***iteraction between the ranking of ranking on the left panel to the diagram on in the midele panel***, which allows the user to highlight the specific countries distribution in the map when clicking on the bar chart. 
- Improve the user experience of the dashboard, and use more meaningful color to represent the data in the visualization.
- Add data last updated timestamp to the dashboard, so the user have a better sense about how updated our data is
- The app works best with screen resolution 1920x1080, when it is shown on smaller screen, some charts will not be scaled responsively yet
