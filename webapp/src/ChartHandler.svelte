<script>
	import { db }  from './firebase';;
	export let currentStore;
	import Chart from './Chart.svelte';
	import { onMount } from 'svelte';
	import { numPeopleStore, maxCapStore } from './storeDataStore2.js';
	let weep = false;

	onMount(async () => {
		if (!!currentStore) {
			var docRef = db.collection("stores").doc(currentStore);

		    await docRef.get().then(function(doc) {
		        if (doc.exists) {
		            console.log("Document data:" + doc.get('NumPeople') + " || " + doc.get('MaxCap'));
		            numPeopleStore.set(doc.get('NumPeople'));
		            maxCapStore.set(doc.get('MaxCap'));
		        } else {
		            // doc.data() will be undefined in this case
		            console.log("No such document!");

		        }
		    }).catch(function(error) {
		        console.log("Error getting document:", error);
		    });
		}
        weep = true;
	})

</script>

<div>
	{#if !!currentStore && weep == true}
	<Chart numPeople={$numPeopleStore} maxCap={$maxCapStore}/>
	{:else}
	<strong>Loading...</strong>
	{/if}
</div>