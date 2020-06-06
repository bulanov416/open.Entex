<script>
	export let name;
	import { db}  from './firebase';
	import { onMount } from 'svelte';
	import NewComp from './NewComp.svelte';

	
	/*function getStores() {
		let tempStores = [];
		
		return tempStores;
	}

	function getPeople(storeName) {
		db.collection("stores").doc(storeName).collection("dataSamples").get().then((querySnapshot) => {
			querySnapshot.forEach((doc) => {
				console.log(doc.id + " || " + doc.get("timeStamp") + " || " + doc.get("numPeople"));
			});
		});
	}*/

	let stores = [];

	onMount(async () => {
		await db.collection("stores").get().then((querySnapshot) => {

			querySnapshot.forEach((doc) => {
				console.log(doc.id);
				let mountStore = { id: doc.id, name: doc.get("StoreName")}
				stores.push(mountStore)
			});
		stores = stores
		});
		console.log(stores)
	})

</script>

<main>
	<h1>Hello {name}!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
</main>

	<div class="stores">
	{#each stores as store}
	<p>{store.id}</p>
		{:else}
		<!-- this block renders when photos.length === 0 -->
		<p>loading...</p>
	{/each}
	</div>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>