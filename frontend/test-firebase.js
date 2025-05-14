// Import Firebase v10 (which you have installed)
const { initializeApp } = require('firebase/app');
const { getAuth, createUserWithEmailAndPassword } = require('firebase/auth');

const config = {
    apiKey: "AIzaSyB_d8xpQLQ4ZWMxsSWYqQi_iypKS7xjA78",
    authDomain: "fitness-food-app-9d41d.firebaseapp.com",
    projectId: "fitness-food-app-9d41d",
    storageBucket: "fitness-food-app-9d41d.firebasestorage.app",
    messagingSenderId: "175044367442",
    appId: "1:175044367442:web:3b38fe992db32996b5fb8b"
};

console.log('Initializing Firebase...');
const app = initializeApp(config);
const auth = getAuth(app);

console.log('Testing auth...');
createUserWithEmailAndPassword(auth, 'test@test.com', 'password123')
    .then(() => {
        console.log('✅ SUCCESS: Firebase auth works!');
        process.exit(0);
    })
    .catch((error) => {
        console.log('❌ ERROR:', error.code, '-', error.message);
        process.exit(1);
    });
