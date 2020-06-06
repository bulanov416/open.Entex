<script>
	export let name;
	import { db}  from './firebase';
	import { onMount } from 'svelte';


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

	import Navbar from './Navbar.svelte'
	import Sidebar from './Sidebar.svelte'
	import Main from './Main.svelte';

	let open = false

</script>

<Sidebar bind:open allStores={stores}/>
<Navbar bind:sidebar={open}/>
<Main/>

<svelte:head>
	<link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet"/>
</svelte:head>



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