<script>
import { db } from "./firebase";
import {currentStoreId} from './stores.js';

export function getCurrentStoreData() {
  let currSData = [];
  if (storeID != null) {
    const peopleInPlace = db
      .collection("stores")
      .doc({$currentStoreId})
      .collection("dataSamples")
      .onSnapshot(function (querySnapshot) {
        var dataPoints = [];
        querySnapshot.forEach(function (doc) {
          let foo = [doc.get("timeStamp"), doc.get("numPeople")];
          dataPoints.push(foo);
        });
        console.log(dataPoints);
        dataPoints = dataPoints;
        return dataPoints;
      });
    currSData = peopleInPlace;
  }
  return currSData;
}
</script>
