<script>
  import ApexCharts from 'apexcharts'
  import { db }  from './firebase';;
  export let currentStore;
  import Graph from './Graph.svelte';
  import { onMount } from 'svelte';
  import { currentStoreData, currentStoreData2 } from './storeDataStore.js';
  let weep = false
  var unixTimestamp = 1553617238;
  var date = new Date(unixTimestamp*1000);

	onMount(async () => {
		/*await db.collection("stores").get().then((querySnapshot) => {

			querySnapshot.forEach((doc) => {
				console.log(doc.id);
				let mountStore = { id: doc.id, name: doc.get("StoreName")}
				stores.push(mountStore)
			});
		stores = stores
		});
    console.log(stores)*/
    if (!!currentStore) {
      let timePoints = []
      let capPoints = []
      await db.collection("stores").doc(currentStore).collection("dataSamples").get().then((querySnapshot) => {
      querySnapshot.forEach((doc) => {
              console.log(doc.get("timeStamp"))
              var eek = doc.get("timeStamp")*1000
              var myDate = new Date(eek - 100000000000000);
              let foo = myDate;
              timePoints.push(foo);
              let bar = doc.get("numPeople")
              capPoints.push(bar);
          });
        console.log(timePoints)
        timePoints = timePoints
        return timePoints
      })  
      console.log("foo")
      currentStoreData.set(timePoints)
      console.log(timePoints)
      console.log(capPoints)
      currentStoreData2.set(capPoints)
      weep = true
    }
  })
  
</script>

<div>
	{#if !!currentStore && weep == true}
	<Graph currentStoreTimes={$currentStoreData} currentStoreCaps={$currentStoreData2}/>
	{:else}
	<strong>Loading...</strong>
	{/if}
</div>

<!--{#if !!peopleInPlace}
	<Graph graphData={data}/>
{:else}
	<p>Loading...</p>
{/if}
-->