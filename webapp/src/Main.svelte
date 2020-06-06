<script>
	export let currentStore;
</script>
<main class="p-4">
	{#if !!currentStore}
	<h2>The store is {currentStore}</h2>
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