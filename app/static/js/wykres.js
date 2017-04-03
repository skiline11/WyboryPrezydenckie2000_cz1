var wykres;
var legend;
var selected;

var types = [
    
        {
            type: "Dariusz Maciej GRABOWSKI",
            percent: 0.51,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Piotr IKONOWICZ",
            percent: 0.22,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Jarosław KALINOWSKI",
            percent: 5.95,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Janusz KORWIN-MIKKE",
            percent: 1.43,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Marian KRZAKLEWSKI",
            percent: 15.57,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Aleksander KWAŚNIEWSKI",
            percent: 53.90,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Andrzej LEPPER",
            percent: 3.05,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Jan ŁOPUSZAŃSKI",
            percent: 0.79,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Andrzej Marian OLECHOWSKI",
            percent: 17.30,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Bogdan PAWŁOWSKI",
            percent: 0.10,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Lech WAŁĘSA",
            percent: 1.01,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
        {
            type: "Tadeusz Adam WILECKI",
            percent: 0.16,
            color: "#"+((1<<24)*Math.random()|0).toString(16)
        },
    
];

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