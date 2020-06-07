<script>
	import PeopleInPlace from './PeopleInPlace.svelte';
	export let currentStore;
	import { db }  from './firebase';
	import Chart from './Chart.svelte';
	import GraphHandler from './GraphHandler.svelte';
	import ChartHandler from './ChartHandler.svelte';

</script>
<main class="p-4">
	{#if !!currentStore}
	<h1>{currentStore}</h1>
	<GraphHandler currentStore={currentStore}/>
	<ChartHandler currentStore={currentStore}/>
	<button></button>
	{:else}
	<img id="logo" src="./open_entex_logo.png">
	<strong style="font-size:40px;">Welcome to <i>Open Entex</i>.<br>Please choose a store from the menu on the left.</strong>
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

	#logo {
    	justify-content: center;
    	display: flex;
    	text-align: center;
    	margin-left: auto;
    	margin-right: auto;
	}
</style>