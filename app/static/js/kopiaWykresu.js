var wykres;
var legend;
var selected;

var types = [{
  type: "Fossil Energy",
  percent: 70,
  color: "#"+((1<<24)*Math.random()|0).toString(16),
}, {
  type: "Green Energy",
  percent: 30,
  color: "#"+((1<<24)*Math.random()|0).toString(16),
}];

function generateChartData() {
  var chartData = [];
  for (var i = 0; i < types.length; i++) {
    if (i == selected) {
      for (var x = 0; x < types[i].subs.length; x++) {
        chartData.push({
          pulled: true
        });
      }
    } else {
      chartData.push({
        type: types[i].type,
        percent: types[i].percent,
        color: types[i].color,
        id: i
      });
    }
  }
  return chartData;
}

AmCharts.makeChart("wykres", {
  "type": "pie",
"theme": "light",

  "dataProvider": generateChartData(),
  "labelText": "[[title]]: [[value]]",
  "balloonText": "[[title]]: [[value]]",
  "titleField": "type",
  "valueField": "percent",
  "outlineColor": "#FFFFFF",
  "outlineAlpha": 0.8,
  "outlineThickness": 2,
  "colorField": "color",
  "pulledField": "pulled",
  "listeners": [{
    "event": "clickSlice",
    "method": function(event) {
      var chartdiv = event.chart;
      if (event.dataItem.dataContext.id != undefined) {
        selected = event.dataItem.dataContext.id;
      } else {
        selected = undefined;
      }
      chartdiv.dataProvider = generateChartData();
      chartdiv.validateData();
    }
  }],
  "export": {
    "enabled": true
  }
});
