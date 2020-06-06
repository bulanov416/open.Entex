<script>
	export let open = false
	export let allStores;
</script>

<aside class="absolute w-full h-full bg-gray-200 border-r-2 shadow-lg" class:open>
 <nav class="p-12 text-xl">
 	<div class="allStores">
	{#each allStores as store}
	<a class="block" href={store.id}>{store.name}</a>
	{/each}
	</div>
    <a class="block" href="#about">About</a>
  </nav>
</aside>

<style>
	aside {
		left: -100%;
		transition: left 0.3s ease-in-out
	}
	
	.open {
		left: 0
	}
</style>