<script>
	import PeopleInPlace from './PeopleInPlace.svelte';
	export let currentStore;
	import { db }  from './firebase';
	import Chart from './Chart.svelte';
	import GraphHandler from './GraphHandler.svelte';
    
</script>
<main class="p-4">
	{#if !!currentStore}
	<h1>{currentStore}</h1>
	<GraphHandler currentStore={currentStore}/>
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