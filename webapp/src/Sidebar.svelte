<script>
	import { db } from './firebase';
	export let open = false
	export let allStores;

	function foo(storeName2){
		console.log(storeName2 + " | ");
	}
	


	async function populateData(storeName) {
		
		await db.collection("stores").doc(storeName).collection("dataSample").get().then((querySnapshot) => {
			//let numPeopleArray = []
			querySnapshot.forEach((doc) => {
				console.log(doc.id);
				let data = {numPeople: doc.get("numPeople"), timeStamp: doc.get("timeStamp")}
				console.log("helloworld");
			});
		//numPeopleArray = numPeopleArray;
		});
		//console.log(numPeopleArray);
		//return numPeopleArray;
	}


</script>

<aside class="absolute w-full h-full bg-gray-200 border-r-2 shadow-lg" class:open>
 <nav class="p-12 text-xl">
 	<div class="allStores">
	{#each allStores as store}
	<a class="block" id={store.id} href={foo(store.id)}>{store.name}</a>
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