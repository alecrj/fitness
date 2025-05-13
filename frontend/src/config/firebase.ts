import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';
import { getAuth } from 'firebase/auth';

// Debug: Check all environment variables
console.log('All REACT_APP_FIREBASE env vars:');
console.log('REACT_APP_FIREBASE_API_KEY:', process.env.REACT_APP_FIREBASE_API_KEY);
console.log('REACT_APP_FIREBASE_AUTH_DOMAIN:', process.env.REACT_APP_FIREBASE_AUTH_DOMAIN);
console.log('REACT_APP_FIREBASE_PROJECT_ID:', process.env.REACT_APP_FIREBASE_PROJECT_ID);
console.log('REACT_APP_FIREBASE_STORAGE_BUCKET:', process.env.REACT_APP_FIREBASE_STORAGE_BUCKET);
console.log('REACT_APP_FIREBASE_MESSAGING_SENDER_ID:', process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID);
console.log('REACT_APP_FIREBASE_APP_ID:', process.env.REACT_APP_FIREBASE_APP_ID);
console.log('REACT_APP_FIREBASE_MEASUREMENT_ID:', process.env.REACT_APP_FIREBASE_MEASUREMENT_ID);

// Firebase configuration
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID
};

console.log('Final firebaseConfig:', firebaseConfig);

// Initialize Firebase
export const firebaseApp = initializeApp(firebaseConfig);
export const db = getFirestore(firebaseApp);
export const storage = getStorage(firebaseApp);
export const auth = getAuth(firebaseApp);

export default firebaseApp;