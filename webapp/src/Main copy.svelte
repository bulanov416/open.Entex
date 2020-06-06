<script>
	import PeopleInPlace from './PeopleInPlace.svelte';
	export let currentStore;
	import { db }  from './firebase';
	import Chart from './Chart.svelte';
	import Graph from './Graph.svelte';
	import {currentStoreData } from './storeDataStore.js';

	if (!!currentStore) {
		console.log("foo")
		currentStoreData.set(storeName)
	}
	
    
</script>
<main class="p-4">
	{#if !!currentStore && !!currentStoreData}
	<h1>welcome to {currentStore}</h1>
	{:else}
	<strong>Welcome to ____ Please choose a store from the menue on the left</strong>
	{/if}
</main>

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
</style>