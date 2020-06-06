<script>
  import FusionCharts from 'fusioncharts';
  import { db }  from './firebase';
  import Timeseries from 'fusioncharts/fusioncharts.timeseries';
  import SvelteFC, { fcRoot } from 'svelte-fusioncharts';
  import dataSource from './data2.js';
  import schemaSource from './schema.js';
  export let currentStore;

  fcRoot(FusionCharts, Timeseries);

  let dataPoints2 = []

  function peopleInPlace() {db.collection("stores").doc(currentStore).collection("dataSamples").onSnapshot(function(querySnapshot) {
        var dataPoints = [];
        querySnapshot.forEach(function(doc) {
            let foo = [doc.get("timeStamp"), doc.get("numPeople")]
            dataPoints.push(foo);
        });
		console.log(dataPoints)
		dataPoints = dataPoints
    return dataPoints
   })}

  dataPoints2 = peopleInPlace()
  

  const getChartConfig = () => {
    const fusionDataStore = new FusionCharts.DataStore(),
      fusionTable = fusionDataStore.createDataTable(dataPoints2, schemaSource);

    return {
      type: 'timeseries',
      width: '100%',
      height: 450,
      renderAt: 'chart-container',
      dataSource: {
        data: fusionTable,
        caption: {
          text: 'Sales Analysis'
        },
        subcaption: {
          text: 'Grocery'
        },
        yAxis: [
          {
            plot: {
              value: 'Grocery Sales Value',
              type: 'line'
            },
            format: {
              prefix: '$'
            },
            title: 'Sale Value'
          }
        ]
      }
    };
  };
</script>

<div id="chart-container" >
    <SvelteFC
      {...getChartConfig()}
    />
</div>