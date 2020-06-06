import firebase from 'firebase/app';// rollup bundle issue with ESM import
import 'firebase/auth';
import 'firebase/firestore';
var firebaseConfig = {
  apiKey: "AIzaSyAQaqXyzLZSufQ_kHkrNnQ4at3q_MBb2B4",
  authDomain: "hacknortheast.firebaseapp.com",
  databaseURL: "https://hacknortheast.firebaseio.com",
  projectId: "hacknortheast",
  storageBucket: "hacknortheast.appspot.com",
  messagingSenderId: "700688984971",
  appId: "1:700688984971:web:922dade65aa0692d555d8e",
  measurementId: "G-1DL5HFVN5K"
};

console.log(firebase)

firebase.initializeApp(firebaseConfig);

export const auth = firebase.auth();
export const googleProvider = new firebase.auth.GoogleAuthProvider();

export const db = firebase.firestore();