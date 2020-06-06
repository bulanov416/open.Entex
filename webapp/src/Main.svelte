<script>
	import { currentStoreId } from './stores.js';
	import Chart from './Chart.svelte';
	import Graph from './Graph.svelte';
</script>
<main class="p-4 text-gray-300">

	<h1>The store is {$currentStoreId}</h1>

	<Chart/>
	<Graph/>

</main>

<style>
</style>