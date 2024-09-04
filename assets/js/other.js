import { initializeApp } from "firebase/app";
import { getMessaging } from "firebase/messaging/sw";
import { onBackgroundMessage } from "firebase/messaging/sw";

const firebaseConfig = {
    apiKey: "AIzaSyCsEEl7bhST8VHrK3ovbEfMxCUcHZngKg0",
    authDomain: "geraipi.firebaseapp.com",
    projectId: "geraipi",
    storageBucket: "geraipi.appspot.com",
    messagingSenderId: "1071852496864",
    appId: "1:1071852496864:web:c5e8338dc67fa12d9bad85",
    measurementId: "G-SW3CZ09N71"
};

const app = initializeApp(firebaseConfig);

const messaging = getMessaging(app);
onBackgroundMessage(messaging, (payload) => {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = 'Background Message Title';
  const notificationOptions = {
    body: 'Background Message body.',
    icon: '/firebase-logo.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});