import { initializeApp } from 'firebase/app';
import { getAuth, connectAuthEmulator } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

// Log all environment variables for debugging
console.log('🔍 Environment variables check:');
console.log('NODE_ENV:', process.env.NODE_ENV);
console.log('API_KEY exists:', !!process.env.REACT_APP_FIREBASE_API_KEY);
console.log('PROJECT_ID:', process.env.REACT_APP_FIREBASE_PROJECT_ID);
console.log('AUTH_DOMAIN:', process.env.REACT_APP_FIREBASE_AUTH_DOMAIN);

// TEMPORARY: Log the actual API key for debugging (REMOVE IN PRODUCTION)
console.log('🔑 FULL API KEY:', process.env.REACT_APP_FIREBASE_API_KEY);

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

console.log('🔥 Firebase config object:', firebaseConfig);

// Verify all required fields are present
const required = ['apiKey', 'authDomain', 'projectId', 'storageBucket', 'messagingSenderId', 'appId'];
const missing = required.filter(field => !firebaseConfig[field as keyof typeof firebaseConfig]);

if (missing.length > 0) {
  console.error('❌ Missing Firebase config fields:', missing);
  throw new Error(`Missing Firebase configuration: ${missing.join(', ')}`);
}

// Initialize Firebase
console.log('🚀 Initializing Firebase...');
const app = initializeApp(firebaseConfig);
console.log('✅ Firebase app initialized:', app.name);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);

// Export for compatibility
export const firebaseApp = app;

console.log('🔐 Auth service initialized:', auth.app.name);

export default app;