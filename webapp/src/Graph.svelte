<script>
  import ApexCharts from 'apexcharts'
  import { db }  from './firebase';;
  export let currentStoreData;

  let data = currentStoreData
  
var options = {
  chart: {
    height: 380,
    width: "100%",
    type: "area",
    animations: {
      initialAnimation: {
        enabled: false
      }
    }
  },
  series: [
    {
      name: "Series 1",
      data: [
        {
          x: "02-10-2017 GMT",
          y: 34
        },
        {
          x: "02-11-2017 GMT",
          y: 43
        },
        {
          x: "02-12-2017 GMT",
          y: 31
        },
        {
          x: "02-13-2017 GMT",
          y: 43
        },
        {
          x: "02-14-2017 GMT",
          y: 33
        },
        {
          x: "02-15-2017 GMT",
          y: 52
        }
      ]
    }
  ],
  xaxis: {
    type: "numeric"
  }
};

var chart = new ApexCharts(document.querySelector("#chart"), options);

chart.render();
</script>

<div id="chart">
</div>
