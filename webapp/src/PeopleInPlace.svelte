<script>
    import { db}  from './firebase';
	export let currentStore;
	import Chart from './Chart.svelte';
	import Graph from './Graph.svelte';
    
    function peopleInPlace() {db.collection("stores").doc(currentStore).collection("dataSamples").onSnapshot(function(querySnapshot) {
        var dataPoints = [];
        querySnapshot.forEach(function(doc) {
            let foo = {id: doc.id, timeStamp: doc.get("timeStamp"), numPeople: doc.get("numPeople")}
            dataPoints.push(foo);
        });
		console.log(dataPoints)
		dataPoints = dataPoints
        return dataPoints
   })}
</script>

<div>
	<h2>The store is {currentStore}</h2>
	<Graph timeBits={peopleInPlace()}/>
</div>

<style>
	main {
		text-align: center;

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