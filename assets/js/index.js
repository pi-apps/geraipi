import { initializeApp } from "firebase/app";
import { getMessaging, getToken } from "firebase/messaging";

// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object
const firebaseConfig = {
  apiKey: "AIzaSyCsEEl7bhST8VHrK3ovbEfMxCUcHZngKg0",
  authDomain: "geraipi.firebaseapp.com",
  projectId: "geraipi",
  storageBucket: "geraipi.appspot.com",
  messagingSenderId: "1071852496864",
  appId: "1:1071852496864:web:c5e8338dc67fa12d9bad85",
  measurementId: "G-SW3CZ09N71"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);


// Initialize Firebase Cloud Messaging and get a reference to the service
const messaging = getMessaging(app);
getToken(messaging, { vapidKey: 'BFN7KQFtuiq9l_tkSE3GcS66hqmsG7ddDjL5wrpSlegQY5_YGzp1LD5F3vn74RP4skldx5A_7k9DQuswI5zYUEs' }).then((currentToken) => {
  if (currentToken) {
    // Send the token to your server and update the UI if necessary
    // ...
    console.log("token")
  } else {
    console.log('No registration token available. Request permission to generate one.');
  }
}).catch((err) => {
  console.log('An error occurred while retrieving token. ', err);
  // ...
});
