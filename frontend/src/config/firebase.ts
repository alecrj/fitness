import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyB_d5xpQLQ4ZWMxsSWYqQi_iypKS7xjA78",
  authDomain: "fitness-food-app-9d41d.firebaseapp.com",
  projectId: "fitness-food-app-9d41d",
  storageBucket: "fitness-food-app-9d41d.firebasestorage.app",
  messagingSenderId: "175044367442",
  appId: "1:175044367442:web:3b38fe992db32996b5fb8b",
  measurementId: "G-WNSQX5H5JH"
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);

// Get Firebase services
export const auth = getAuth(firebaseApp);
export const db = getFirestore(firebaseApp);
export const storage = getStorage(firebaseApp);

export { firebaseApp };
export default firebaseApp;