import { initializeApp, FirebaseApp } from 'firebase/app';
import { getFirestore, Firestore } from 'firebase/firestore';
import { getStorage, FirebaseStorage } from 'firebase/storage';
import { getAuth, Auth } from 'firebase/auth';

// Firebase configuration with CORRECTED fallback values
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY || "AIzaSyB_d5xpQLQ4ZWMxsSWYqQi_iypKS7xjA78",
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN || "fitness-food-app-9d41d.firebaseapp.com",
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID || "fitness-food-app-9d41d",
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET || "fitness-food-app-9d41d.firebasestorage.app",
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID || "175044367442",
  appId: process.env.REACT_APP_FIREBASE_APP_ID || "1:175044367442:web:3b38fe992db32996b5fb8b",
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID || "G-WNSQXS16JH"
};

// Initialize Firebase
const app: FirebaseApp = initializeApp(firebaseConfig);

// Initialize Firebase services - these are guaranteed to be defined
const db: Firestore = getFirestore(app);
const storage: FirebaseStorage = getStorage(app);
const auth: Auth = getAuth(app);

// Debug logging to see which API key is being used
if (process.env.NODE_ENV === 'development') {
  console.log('Firebase initialized successfully');
  console.log('Project ID:', firebaseConfig.projectId);
  console.log('API Key being used:', firebaseConfig.apiKey.substring(0, 15) + '...');
  console.log('Environment API Key exists:', !!process.env.REACT_APP_FIREBASE_API_KEY);
}

// Export the services
export { app as firebaseApp, db, storage, auth };
export default app;