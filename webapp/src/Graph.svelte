<script>
  import Chart from 'svelte-frappe-charts';
  import { db }  from './firebase';
  
  export let currentStoreCaps;
  export let currentStoreTimes;
  

  let y = currentStoreCaps;
  let x = currentStoreTimes;

 let data = {
    labels: x,
    datasets: [
      {
        values: y
      }
    ]
  };
</script>

<Chart data={data} type="line" />