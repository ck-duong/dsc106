/**
 * In order to synchronize tooltips and crosshairs, override the
 * built-in events with handlers defined on the parent element.
 */

["mousemove", "touchmove", "touchstart"].forEach(function(eventType) {
  document
    .getElementById("sharedGrid")
    .addEventListener(eventType, function(e) {
      var chart, point, i, event;

      for (i = 0; i < 3; i = i + 1) {
        chart = Highcharts.charts[i];
        // Find coordinates within the chart
        event = chart.pointer.normalize(e);
        // Get the hovered point
        if (chart.series.length > 1) {
          //console.log(chart.series[1].searchPoint(event, true));
          //console.log(chart.series[0].searchPoint(event, true));
        }
        point = chart.series[0].searchPoint(event, true);
        //console.log(point.x);

        //console.log(chart.series.length);
        if (point) {
          point.highlight(e);
          updatePieChart((globalPoint - 1571579700000) / 30 / 60 / 1000);
          updateLegend((globalPoint - 1571579700000) / 30 / 60 / 1000);
        }
      }
    });
});

/**
 * Override the reset function, we don't need to hide the tooltips and
 * crosshairs.
 */
Highcharts.Pointer.prototype.reset = function() {
  Highcharts.charts[3].setTitle({
    text: "Avg<br></br><b>7020 MW</b>"
  });
  document.getElementById("TotalPower").innerHTML = "1,097";
  document.getElementById("WindPower").innerHTML = "81";
  document.getElementById("HydroPower").innerHTML = "60";
  document.getElementById("GasPower").innerHTML = "65";
  document.getElementById("DistillatePower").innerHTML = "0.02";
  document.getElementById("CoalPower").innerHTML = "891";
  document.getElementById("TotalLoad").innerHTML = "-15";
  document.getElementById("ExportPower").innerHTML = "-2";
  document.getElementById("PumpPower").innerHTML = "-12";
  document.getElementById("NetTotal").innerHTML = "1,083";

  document.getElementById("WindContribution").innerHTML = "7.5%";
  document.getElementById("HydroContribution").innerHTML = "5.5%";
  document.getElementById("GasContribution").innerHTML = "6.0%";
  document.getElementById("DistillateContribution").innerHTML = "0.002%";
  document.getElementById("CoalContribution").innerHTML = "82.3%";
  document.getElementById("ExportContribution").innerHTML = "-0.2%";
  document.getElementById("PumpContribution").innerHTML = "-1.1%";
  document.getElementById("ReTotal").innerHTML = "13.0%";

  document.getElementById("AvgPrice").innerHTML = "$58.62";
  document.getElementById("WindAvg").innerHTML = "$56.43";
  document.getElementById("HydroAvg").innerHTML = "$63.96";
  document.getElementById("GasAvg").innerHTML = "$60.22";
  document.getElementById("DistillateAvg").innerHTML = "$57.42";
  document.getElementById("CoalAvg").innerHTML = "$59.01";

  return undefined;
};

var globalPoint;

/**
 * Highlight a point by showing tooltip, setting hover state and draw crosshair
 */
Highcharts.Point.prototype.highlight = function(event) {
  event = this.series.chart.pointer.normalize(event);
  this.onMouseOver(); // Show the hover marker
  this.series.chart.tooltip.refresh(this); // Show the tooltip
  this.series.chart.xAxis[0].drawCrosshair(event, this); // Show the crosshair
  globalPoint = this.x;
};

/**
 * Synchronize zooming through the setExtremes event handler.
 */
function syncExtremes(e) {
  var thisChart = this.chart;

  if (e.trigger !== "syncExtremes") {
    // Prevent feedback loop
    Highcharts.each(Highcharts.charts, function(chart) {
      if (chart !== thisChart) {
        if (chart.xAxis[0].setExtremes) {
          // It is null while updating
          chart.xAxis[0].setExtremes(e.min, e.max, undefined, false, {
            trigger: "syncExtremes"
          });
        }
      }
    });
  }
}

let sharedConfig = {
  layout: "3x1",
  graphset: [
    {
      // config for the energy stacked area graph
      chart: {
        type: "area",
        marginLeft: 40, // Keep all charts left aligned
        spacingTop: 20,
        spacingBottom: 20,
        backgroundColor: "transparent",
        height: 300
      },
      colors: [
        "#977AB1",
        "#88AFD0",
        "#121212",
        "#F35020",
        "#FDB462",
        "#4582B4",
        "#417505"
      ],
      title: {
        text: "Generation MW",
        fontSize: 18,
        align: "left"
      },
      "crosshair-x": {
        shared: true
      },
      plot: {
        tooltip: {
          visible: false
        }
      },
      plotarea: {
        margin: "dynamic"
      },
      "scale-x": {
        "min-value": 1571579700000,
        step: "30minute",
        transform: {
          type: "date",
          all: "%m/%d/%Y<br>%h:%i:%s:%q %A"
        },
        item: {
          "font-size": 9
        }
      },
      utc: true,
      plotOptions: {
        series: {
          pointStart: Date.UTC(2010, 0, 1), //default
          pointInterval: 30 * 60 * 1000, // 30 minutes
          states: {
            inactive: {
              opacity: 1
            }
          }
        },
        area: {
          stacking: "normal"
        },
        hover: {
          enabled: false
        }
      },
      xAxis: {
        type: "datetime",
        crosshair: true,
        alternateGridColor: "#DBDBDB",
        events: {
          setExtremes: syncExtremes
        }
      },
      yAxis: {
        reversedStacks: false
      },
      tooltip: {
        shared: false,
        positioner: function() {
          return {
            // right aligned
            x: this.chart.chartWidth - this.label.width,
            y: 10 // align to title
          };
        },
        formatter: function() {
          return (
            Highcharts.dateFormat("%e %b, %l:%M%p", new Date(this.x)) +
            " | " +
            this.series.name +
            " " +
            "<b>" +
            this.y +
            " MW | " +
            "</b> " +
            "Total <b>" +
            this.total.toFixed(0) +
            " MW" +
            "</b>"
          );
        },
        valueSuffix: "MW",
        borderWidth: 0,
        backgroundColor: "white",
        xDateFormat: "%Y-%m-%d",
        pointFormat: "{point.y}",
        headerFormat: "{point.x}",
        shadow: false,
        style: {
          fontSize: "18px"
        }
      },
      credits: {
        enabled: false
      },
      series: [
        {
          data: []
        }
      ]
    },
    {
      // config for the price line graph
      type: "line",
      chart: {
        backgroundColor: "transparent",
        height: 200
      },
      title: {
        text: "Price $/MWh",
        fontSize: 18,
        align: "left"
      },
      "crosshair-x": {
        shared: true
      },
      plot: {
        tooltip: {
          visible: false
        }
      },
      plotarea: {},
      "scale-x": {
        "min-value": 1571579700000,
        step: "30minute",
        transform: {
          type: "date",
          all: "%m/%d/%Y<br>%h:%i:%s:%q %A"
        },
        item: {
          "font-size": 9
        }
      },
      utc: true,
      timezone: 0,
      "scale-y": {
        values: "0:30",
        format: "%v",
        guide: {
          "line-style": "dotted"
        }
      },
      plotOptions: {
        series: {
          pointStart: Date.UTC(2010, 0, 1), //default
          pointInterval: 30 * 60 * 1000, // 30 minutes
          color: "#C74523",
          states: {
            inactive: {
              opacity: 1
            }
          }
        }
      },
      xAxis: {
        type: "datetime",
        crosshair: true,
        alternateGridColor: "#DBDBDB",
        events: {
          setExtremes: syncExtremes
        }
      },
      tooltip: {
        shared: true,
        positioner: function() {
          return {
            // right aligned
            x: this.chart.chartWidth - this.label.width,
            y: 10 // align to title
          };
        },
        formatter: function() {
          return (
            "<b>" +
            Highcharts.dateFormat("%e %b, %l:%M%p", new Date(this.x)) +
            "</b> | <b>$" +
            this.y +
            ".00" +
            "</b>"
          );
        },
        valueSuffix: "$/MWh",
        borderWidth: 0,
        backgroundColor: "white",
        pointFormat: "{point.y}",
        headerFormat: "",
        shadow: false,
        style: {
          fontSize: "18px"
        }
      },
      series: []
    },
    {
      // config for the temperature line graph
      type: "line",
      chart: {
        backgroundColor: "transparent",
        height: 200
      },
      title: {
        text: "Temperature °F",
        fontSize: 18,
        align: "left"
      },
      "crosshair-x": {
        shared: true
      },
      plot: {
        tooltip: {
          visible: false
        }
      },
      plotarea: {},
      "scale-x": {
        "min-value": 1571579700000,
        step: "30minute",
        transform: {
          type: "date",
          all: "%m/%d/%Y<br>%h:%i:%s:%q %A"
        },
        item: {
          "font-size": 9
        }
      },
      utc: true,
      timezone: 0,
      "scale-y": {
        values: "0:80:20",
        format: "%v",
        guide: {
          "line-style": "dotted"
        }
      },
      plotOptions: {
        series: {
          pointStart: Date.UTC(2010, 0, 1), //default
          pointInterval: 30 * 60 * 1000, // 30 minutes
          color: "#C74523",
          states: {
            inactive: {
              opacity: 1
            }
          }
        }
      },
      xAxis: {
        type: "datetime",
        crosshair: true,
        alternateGridColor: "#DBDBDB",
        events: {
          setExtremes: syncExtremes
        }
      },
      tooltip: {
        shared: true,
        positioner: function() {
          return {
            // right aligned
            x: this.chart.chartWidth - this.label.width,
            y: 10 // align to title
          };
        },
        formatter: function() {
          return (
            "<b>" +
            Highcharts.dateFormat("%e %b, %l:%M%p", new Date(this.x)) +
            "</b> | Avg <b>" +
            this.y +
            "°F" +
            "</b>"
          );
        },
        valueSuffix: "°F",
        borderWidth: 0,
        backgroundColor: "white",
        pointFormat: "{point.y}",
        headerFormat: "",
        shadow: false,
        style: {
          fontSize: "18px"
        }
      },
      series: []
    }
  ]
};

let pieConfig = {
  exporting: {
    menuItemDefinitions: {
      // Custom definition
      switchChart: {
        onclick: function() {
          var chartType = this.options.chart.type;

          if (chartType === "bar") {
          }
          this.update({
            chart: {
              type: chartType === "bar" ? "pie" : "bar"
            },
            title: {
              text: "boop"
            }
          });
        },
        text: "Switch chart"
      }
    },
    buttons: {
      contextButton: {
        menuItems: [
          "switchChart",
          "separator",
          "printChart",
          "separator",
          "downloadPNG",
          "downloadJPEG",
          "downloadPDF",
          "downloadSVG"
        ]
      }
    }
  },
  chart: {
    type: "pie",
    backgroundColor: "transparent",
    marginLeft: 40, // Keep all charts left aligned
    spacingTop: 20,
    spacingBottom: 20
  },
  colors: ["#121212", "#F35020", "#FDB462", "#88AFD0", "#417505"],
  title: {
    align: "center",
    verticalAlign: "middle",
    text: "<b>7020 MW</b>",
    style: {
      fontSize: "13px"
    }
  },
  plotOptions: {
    pie: {
      allowPointSelect: false,
      cursor: "pointer",
      dataLabels: {
        enabled: false
      },
      center: ["50%", "50%"],
      series: {
        states: {
          inactive: {
            opacity: 1
          }
        }
      }
    }
  },
  series: [
    {
      name: "Energy",
      colorByPoint: true,
      data: []
    }
  ]
};

// global data-structure to hold the energy breakup
var globalEnergyData = {
  keys: [],
  values: []
};

// function to do deep-copy on the global data structure
function updateGlobalEnergyData(data) {
  globalEnergyData["values"] = [];
  for (var idx = 0; idx < data[0]["data"].length; idx++) {
    var energyBreakup = data.map(elm => {
      return elm["data"][idx];
    });
    globalEnergyData["values"].push(energyBreakup);
  }
  globalEnergyData["keys"] = data.map(elm => elm["name"]);
}

function updateLegend(nodeId) {
  var dataset = globalEnergyData["keys"].map(function(elm, idx) {
    return {
      name: elm,
      y: [globalEnergyData["values"][nodeId][idx]][0]
    };
  });
  var total = 0;
  for (var i = 0; i < dataset.length; i = i + 1) {
    total = total + dataset[i].y;
  }
  document.getElementById("TotalPower").innerHTML = total.toFixed(0);
  var load = Number(dataset[4].y.toFixed(0)) + Number(dataset[6].y.toFixed(0));

  var coal = Number(dataset[0].y.toFixed(0));
  var distillate = Number(dataset[1].y.toFixed(3));
  var gas = Number(dataset[2].y.toFixed(0));
  var hydro = Number(dataset[3].y.toFixed(0));
  var pump = Number(dataset[4].y.toFixed(0));
  var wind = Number(dataset[5].y.toFixed(0));
  var exportVal = Number(dataset[6].y.toFixed(0));

  //coal, distillate, gas, hydro, pumps, wind, exports
  document.getElementById("CoalPower").innerHTML = coal;
  document.getElementById("DistillatePower").innerHTML = distillate;
  document.getElementById("GasPower").innerHTML = gas;
  document.getElementById("HydroPower").innerHTML = hydro;
  document.getElementById("PumpPower").innerHTML = pump;
  document.getElementById("WindPower").innerHTML = wind;
  document.getElementById("ExportPower").innerHTML = exportVal;
  document.getElementById("TotalLoad").innerHTML = load;
  document.getElementById("NetTotal").innerHTML = (total + load).toFixed(0);

  document.getElementById("CoalContribution").innerHTML =
    ((coal / total) * 100).toFixed(1) + "%";
  document.getElementById("DistillateContribution").innerHTML =
    ((distillate / total) * 100).toFixed(3) + "%";
  document.getElementById("GasContribution").innerHTML =
    ((gas / total) * 100).toFixed(1) + "%";
  document.getElementById("HydroContribution").innerHTML =
    ((hydro / total) * 100).toFixed(1) + "%";
  document.getElementById("PumpContribution").innerHTML =
    ((pump / total) * 100).toFixed(1) + "%";
  document.getElementById("WindContribution").innerHTML =
    ((wind / total) * 100).toFixed(1) + "%";
  document.getElementById("ExportContribution").innerHTML =
    ((exportVal / total) * 100).toFixed(1) + "%";

  document.getElementById("ReTotal").innerHTML =
    (
      Number(((wind / total) * 100).toFixed(1)) +
      Number(((hydro / total) * 100).toFixed(1))
    ).toFixed(1) + "%";

  var price = sharedConfig.graphset[1].series[0].data[nodeId]
    .toFixed(2)
    .toString();
  document.getElementById("AvgPrice").innerHTML = "$" + price;

  document.getElementById("CoalAvg").innerHTML = "-";
  document.getElementById("DistillateAvg").innerHTML = "-";
  document.getElementById("GasAvg").innerHTML = "-";
  document.getElementById("HydroAvg").innerHTML = "-";
  document.getElementById("WindAvg").innerHTML = "-";
  document.getElementById("PumpAvg").innerHTML = "-";
}

// the nodeId is basically the x-axis value
// the actual breakup is retrieved from the global data-structure
function renderPieChart(nodeId) {
  var pieDataSet = globalEnergyData["keys"].map(function(elm, idx) {
    if (elm !== "exports" && elm !== "pumps") {
      return {
        name: elm,
        y: [globalEnergyData["values"][nodeId][idx]][0]
      };
    }
  });
  pieDataSet.push(pieDataSet.splice(4, 1)[0]);
  pieConfig.series = [
    {
      name: "Energy Generated",
      colorByPoint: true,
      data: pieDataSet,
      innerSize: "50%",
      size: "90%"
    }
  ];

  var pieChart = document.createElement("div");
  pieChart.className = "chart";
  document.getElementById("pieGrid").appendChild(pieChart);
  Highcharts.chart(pieChart, pieConfig);
}

function updatePieChart(nodeId) {
  var totalPie = 0;
  var pieDataSet = globalEnergyData["keys"].map(function(elm, idx) {
    if (elm !== "exports" && elm !== "pumps") {
      totalPie += [globalEnergyData["values"][nodeId][idx]][0];
      return {
        name: elm,
        y: [globalEnergyData["values"][nodeId][idx]][0]
      };
    }
  });
  pieDataSet.push(pieDataSet.splice(4, 1)[0]);
  pieConfig.series = [
    {
      name: "Energy Generated (MW)",
      colorByPoint: true,
      data: pieDataSet,
      innerSize: "40%",
      size: "90%"
    }
  ];

  document.getElementById("pieGrid");
  Highcharts.charts[3].series[0].setData(
    pieDataSet,
    true,
    { duration: 10 },
    true
  );

  document.getElementById("pieGrid");
  Highcharts.charts[3].setTitle({
    text: "<b>" + totalPie.toFixed(2) + " MW"
  });
}

// this function is responsible for plotting the energy on
// successfully loading the JSON data
// It also plots the pie chart for nodeId=0
function onSuccessCb(jsonData) {
  var energyData = jsonData
    .filter(function(elm) {
      return elm["type"] === "power";
    })
    .map(function(elm) {
      if (elm.fuel_tech === "exports" || elm.fuel_tech === "pumps") {
        return {
          data: elm["history"]["data"].map(function(x) {
            return x * -1;
          }),
          name: elm["id"].split(".")[elm["id"].split(".").length - 2],

          showInLegend: false
        };
      }
      return {
        data: elm["history"]["data"],
        name: elm["id"].split(".")[elm["id"].split(".").length - 2],
        visible: true,
        showInLegend: false
      };
    });
  updateGlobalEnergyData(energyData);
  var priceData = jsonData
    .filter(function(elm) {
      return elm["type"] === "price";
    })
    .map(function(elm) {
      return {
        data: elm["history"]["data"],
        name: elm["id"].split(".")[1],
        showInLegend: false
      };
    });
  var tempData = jsonData
    .filter(function(elm) {
      return elm["type"] === "temperature";
    })
    .map(function(elm) {
      return {
        data: elm["history"]["data"],
        name: elm["id"].split(".")[1],
        showInLegend: false
      };
    });
  var start = jsonData.map(function(elm) {
    if (elm["history"]["start"]) {
      return elm["history"]["start"] * 1000;
    }
  });

  //set start time, all data is from same time range so just pick one
  sharedConfig.graphset[0].plotOptions.series.pointStart = start[0];
  sharedConfig.graphset[1].plotOptions.series.pointStart = start[0];
  sharedConfig.graphset[2].plotOptions.series.pointStart = start[0];

  energyData.unshift(energyData.splice(4, 1)[0]);
  energyData.unshift(energyData.splice(6, 1)[0]);

  sharedConfig.graphset[0].series = energyData;
  sharedConfig.graphset[1].series = priceData;
  sharedConfig.graphset[2].series = tempData;

  //don't show pumps (4) and exports (6) in graph like in example
  //keep in graph though

  //sharedConfig.graphset[0].series[6]["visible"] = false;

  var energyChart = document.createElement("div");
  energyChart.className = "chart-energy";
  document.getElementById("sharedGrid").appendChild(energyChart);
  Highcharts.chart(energyChart, sharedConfig["graphset"][0]);

  var priceChart = document.createElement("div");
  priceChart.className = "chart-price";
  document.getElementById("sharedGrid").appendChild(priceChart);
  Highcharts.chart(priceChart, sharedConfig["graphset"][1]);

  var tempChart = document.createElement("div");
  tempChart.className = "chart-temp";
  document.getElementById("sharedGrid").appendChild(tempChart);
  Highcharts.chart(tempChart, sharedConfig["graphset"][2]);

  renderPieChart(0);
}

// Utility function to fetch any file from the server
function fetchJSONFile(filePath, callbackFunc) {
  console.debug("Fetching file:", filePath);
  var httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = function() {
    if (httpRequest.readyState === 4) {
      if (httpRequest.status === 200 || httpRequest.status === 0) {
        console.info("Loaded file:", filePath);
        var data = JSON.parse(httpRequest.responseText);

        //drop Springfield.fuel_tech.rooftop_solar.power bc of irregularities
        delete data[7];

        data.forEach(undersample);
        let us_data;
        function undersample(item) {
          if (item.history.interval === "5m") {
            us_data = [];
            for (let i = 0; i < item.history.data.length; i += 6) {
              us_data[i / 6] = item.history.data[i];
            }
            item.history.interval = "30m";
            item.history.data = us_data;
          }
        }

        console.debug("Data parsed into valid JSON!");
        console.debug(data);
        if (callbackFunc) callbackFunc(data);
      } else {
        console.error(
          "Error while fetching file",
          filePath,
          "with error:",
          httpRequest.statusText
        );
      }
    }
  };
  httpRequest.open("GET", filePath);
  httpRequest.send();
}

// The entrypoint of the script execution
function doMain() {
  fetchJSONFile(
    "https://raw.githubusercontent.com/ck-duong/dsc106/master/hw3/assets/springfield.json",
    onSuccessCb
  );
}

document.onload = doMain();
