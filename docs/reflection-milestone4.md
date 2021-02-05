# Reflection
## Progress of the dashboard:
We have managed to achieve all the functionalities as we designed in our initial proposal. In this milestone, we have attempted to cover most of the high and middle priority feedback coming from the TA, Joel, and our peers. The main improvements have been listed as follow:
- As instructed by the TA from the <a href=https://github.com/UBC-MDS/DSCI_532_Group_12/issues/44>feedback</a>, we filled the middle panel with another new cases per day trendline which can be controled by the buttons in the middle panels to switch the cases type. This change filled up most of the spacing in the bottom of the dashboard, which rendered the layout more balanced.
- We also rescaled the middle panel map size and adjusted the bubble sizes, so that users can gain more information from the visualization. Especially for countries with smaller amount of cases, their bubbles can be more representative.
- We removed the scrolling bar from the left panel and resized the graph to provide the users with better a user experience. In addition, the total cases count has also been added to on the left panel to give the users more information.
- We adjusted the layout slightly for the right panel to make it less compact.
- The updated time has been added at the very bottom of the page following Joel's suggestion.

Up to this release, our panel should have the following functionalities:
The left panel contains a statistic summary and a bar chart which shows the user the ranking of case count by country with the button for user to choose if they want to see (Confirmed Cases, Active Cases, Recovered Cases or Deaths).

In the middle panel, the user could surface the distribution of the cases geographically in a map, with the options to choose confirmed cases, death cases, or recovered cases. The user can also check new cases per day for each categories from this categories. 

In the right panel, the user can check the detailed trend by country and category. Meanwhile, the right panel also shows the user how many cases in the selected category each country currently have. 
## Development Discussion
Due to the time constraint of the implementation for this milestone, we have prioritized the tasks to implement by their complexity, development efforts, benefits and demand rationality. During the implementation, it's been acknowledged by our team that customizing the CSS for some details has been tricky in python with dash library. That's why we haven't completed some of the UI enhacement tasks which couldn't bring about significant benefits from the UX perspective. We also found some potential improvements are complex due to the nature of our source data, as we have to refactor the code substantially to create a toggle button or a slide bar.

***Below we have categorized what we have left by why we didn't choose to do it:***

- Relatively low benefits added with high development efforts 
    - Allow filtering by time frame for charts to show trends. (This task will need significant amount of effort to refactor the code for the data model, which is also out of the scope of our initial proposal) 
- Technically complicated 
    - Add interaction between the left panel and middle panel. (As the left panel and middel panel were implemented seperately and they were different classes from higher level, it's technically hard to make them interactive without refactor the code extensively at this stage.) 
    - Add a toggle button to switch between cases number and cases per population density. (We had problem looking for a reliable population data that can be merged to our COVID data easily. This will also create a substantial amount of code change that can hardly be done within the given time.) 
    - Previously we thought we should have make the dashboard responsive, however this change can be relatively hard to achieve given the framework we are using and the time constraint.
- Not bring about many benefits with low priority 
    - Our peers suggested changing the color palettes for all panels, but it's really hard to tell as people all have different views on design of color. 
    - Our team also considered to cache the `.csv` file instead of load it everytime from John Hopkins Repository, but we haven't got time to refactor this code yet. This might be very minor in terms of affecting the usage of the dashboard. 