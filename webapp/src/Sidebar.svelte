<script>
	import { db } from './firebase';
	import { currentStoreId } from './stores.js';
	export let open = false
	export let allStores;
	export let numPeopleArray = [];

	

	function populateData(storeName) {
		/*await db.collection("stores").doc(storeName).collection("dataSamples").get().then((querySnapshot) => {
			querySnapshot.forEach((doc) => {
				console.log(doc.id);
				let data = {numPeople: doc.get("numPeople"), timeStamp: doc.get("timeStamp")}
				console.log(data);
				numPeopleArray.push(data);
			});
			numPeopleArray = numPeopleArray;
		});
		console.log(numPeopleArray);
		return numPeopleArray;*/
		console.log(storeName)
		currentStoreId.set(storeName)
		open = false;
	}


</script>

<aside class="absolute w-full h-full bg-gray-200 border-r-2 shadow-lg" class:open>
 <nav class="p-12 text-xl">
 	<div class="allStores">
	{#each allStores as store}
	<a class="block" on:click|capture={populateData(store.id)}>{store.name}</a>
	{/each}
	</div>
  </nav>
</aside>

<style>
	aside {
		left: -100%;
		transition: left 0.3s ease-in-out
	}
	
	.open {
		left: 0;
	}
</style>