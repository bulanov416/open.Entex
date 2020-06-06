<script>
	import PeopleInPlace from './PeopleInPlace.svelte';
	export let currentStore;
	import { db }  from './firebase';
	import Chart from './Chart.svelte';
	import GraphHandler from './GraphHandler.svelte';
	import ChartHandler from './ChartHandler.svelte';
    
	async function getNumPeople(store) {
	    var docRef = db.collection("stores").doc(store);

	    docRef.get().then(function(doc) {
	        if (doc.exists) {
	            console.log("Document data:", doc.get('NumPeople'));
	            return doc.get('NumPeople');
	        } else {
	            // doc.data() will be undefined in this case
	            console.log("No such document!");
	        }
	    }).catch(function(error) {
	        console.log("Error getting document:", error);
	    });
  	}


</script>
<main class="p-4">
	{#if !!currentStore}
	<h1>{currentStore}</h1>
	<GraphHandler currentStore={currentStore}/>
	<ChartHandler currentStore={currentStore}/>
	{:else}
	<strong>Welcome to ____ Please choose a store from the menue on the left</strong>
	{/if}
</main>

<style>
	main {
		text-align: center;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}
</style>