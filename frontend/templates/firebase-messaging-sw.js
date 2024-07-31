// Scripts for firebase and firebase messaging
importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js");

// Initialize the Firebase app in the service worker by passing the generated config
const firebaseConfig = {
  apiKey: "AIzaSyCsEEl7bhST8VHrK3ovbEfMxCUcHZngKg0",
  authDomain: "geraipi.firebaseapp.com",
  projectId: "geraipi",
  storageBucket: "geraipi.appspot.com",
  messagingSenderId: "1071852496864",
  appId: "1:1071852496864:web:c5e8338dc67fa12d9bad85",
  measurementId: "G-SW3CZ09N71"
};

firebase.initializeApp(firebaseConfig);

// Retrieve firebase messaging
const messaging = firebase.messaging();

messaging.onBackgroundMessage(function (payload) {
  console.log("Received background message ", payload);

  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});