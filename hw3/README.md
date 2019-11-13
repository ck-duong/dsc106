# HW3 Write-Up

## Instructions to run locally (MacOS/Linux):
1. Download and unzip the DUONG_A15258153_HW3.zip file
2. Use terminal to navigate to the unzipped folder
3. Run `npm install` to make sure all node modules are installed (if you skip this step, the code will not run, and it does run I promise)
4. Run `npm start` to start running the file locally

## Running in Brower Through CodeSandbox
[Run in Brower](https://codesandbox.io/embed/testbox3-kgyk1?fontsize=14&hidenavigation=1&theme=dark)
- Open preview in new browser for best view (button is on bottom left, next to the refresh button)

## Notes
- To toggle between the pie chart and the table/bar chart of energy breakdown:
    1. Click on the three bars in the upper right corner of the pie chart
    2. Click "Switch Chart"

## Limitations
In my recreation of the given Springfield Energy dashboard, I wasn't able to completely replicate all the features present in the screencast. Some of the issues I had (that are present in my final submission) were:
- **Syncing the three charts on the SharedGrid**: When trying to sync my graphs, they always synchronized inconsistently, meaning that only two of the three graphs would synchronize or graphs would only synchronize with charts above them (ie. Generation doesn't synchronize with Temperature unless you're scrolling on Temperature)
- **Issue with showing the correct value on the area graph**: When scrolling over the power area chart, the export value is always printed rather than the actual value you're hovering over (ie. hydro, wind, etc).
- **Updating Values**: For updating values (most notably the legend), at points I had to apply non-ideal methods to update the values such as directly calling the DOM and manually updating the values.
- **Aesthetics**: I could not fully match the screencast aesthetics in my dashboard, but still aimed to create a visually pleasing dashboard that resembles the original. Though I match most of the basic functionality, aethetically they are lacking.

### Citations
- http://jsfiddle.net/BlackLabel/tyazu4ko/
- http://jsfiddle.net/BlackLabel/xdsgL6rm/
- http://jsfiddle.net/7sxnzetc/
- https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/chart/height/
- https://stackoverflow.com/questions/30064294/how-do-i-get-the-value-of-a-highcharts-graph-point-on-mouseover
- http://jsfiddle.net/frjqwy5L/
- https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/demo/bar-basic/
- Essentially every documentation page from Highcharts API