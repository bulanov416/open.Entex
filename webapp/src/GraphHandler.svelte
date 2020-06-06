<script>
  import ApexCharts from 'apexcharts'
  import { db }  from './firebase';;
  export let currentStore;
  import Graph from './Graph.svelte';
  import { onMount } from 'svelte';
  import { currentStoreData } from './storeDataStore.js';

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
      let dataPoints = []
      await db.collection("stores").doc(currentStore).collection("dataSamples").get().then((querySnapshot) => {
      querySnapshot.forEach((doc) => {
              let foo = [doc.get("timeStamp"), doc.get("numPeople")]
              dataPoints.push(foo);
          });
        console.log(dataPoints)
        dataPoints = dataPoints
        return dataPoints
      })  
      console.log("foo")
      currentStoreData.set(dataPoints)
      console.log(dataPoints)
    }
  })
  
</script>

<div>
	{#if !!currentStore && !!{$currentStoreData}}
	<Graph currentStoreData={$currentStoreData}/>
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