Highcharts.chart("line", {
  chart: {
    type: "line"
  },
  data: {
    csvURL:
      "https://gist.githubusercontent.com/dingmei/d1ab5dd8ff9597d71b3fba3dc26347fe/raw/31229a7b96e75fd53281c9ec4a3eb6671b42a179/ucsd_cds_admission_data_2005_to_2018"
  },
  marker: false,
  title: {
    text: "UC San Diego Admissions Breakdown by Gender and Year"
  },
  xAxis: {
    title: {
      text: "Year"
    },
    step: 1,
    visible: true
  },
  yAxis: {
    title: {
      text: "Count in Thousands"
    }
  },
  plotOptions: {
    line: {
      dataLabels: {
        enabled: false
      },
      enableMouseTracking: false
    }
  }
});
