importScripts('https://www.gstatic.com/firebasejs/8.1.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.1.1/firebase-messaging.js');
self.addEventListener('notificationclick', event => {
    console.log(event)
});
const firebaseConfig = {
    apiKey: "AIzaSyC0lUXHwQdTFXz8KkC5D7zy-t47RrkIvsY",
    authDomain: "geraipi-indonesia.firebaseapp.com",
    projectId: "geraipi-indonesia",
    storageBucket: "geraipi-indonesia.appspot.com",
    messagingSenderId: "981139646267",
    appId: "1:981139646267:web:53cc230affb50210a5391e",
    measurementId: "G-F368X3MB4J"
};
firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();
messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
    };
    return self.registration.showNotification(notificationTitle,
        notificationOptions);
});


