Highcharts.chart("pie", {
  chart: {
    type: "pie"
  },
  title: {
    text: "UC San Diego Admissions Breakdown by Gender in 2018"
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: "pointer",
      dataLabels: {
        enabled: true,
        format: "<b>{point.name}</b>: {point.percentage:.1f} %"
      }
    }
  },
  series: [
    {
      name: "Admitted",
      colorByPoint: true,
      data: [
        {
          name: "fulltime_men_admitted",
          y: 13781
        },
        {
          name: "fulltime_women_admitted",
          y: 15821
        }
      ]
    }
  ]
});
