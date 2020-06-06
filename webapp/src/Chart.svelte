<script>

  import ProgressBar from '@okrad/svelte-progressbar';


  export let numPeople;
  export let maxCap;
  console.log("usdiafhsdkhf: " + numPeople + " || " + maxCap);
  let ratio = numPeople / maxCap * 100;

  let bar;

  let series = [ratio];

  const updateBar = values => {
    values.forEach((v, i) => bar.updatePerc(v, i));
  };

  const resetBar = () => updateBar([0,0]);
  


</script>

<div id="chart-container">
  <h1>There are {numPeople} people in the store.</h1>
</div><br>
Capacity: <div id="bar">
 <ProgressBar id="bar" {series} bind:this={bar}/>
</div>
<style>
  #chart-container {
    justify-content: center;
    align-items: center;
    display: flex;
  }

  #bar {
    align-items:center ;
    justify-content: center;
    display: flex;
  }
</style>