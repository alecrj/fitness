import { initializeApp, FirebaseApp } from 'firebase/app';
import { getFirestore, connectFirestoreEmulator, Firestore } from 'firebase/firestore';
import { getStorage, connectStorageEmulator, FirebaseStorage } from 'firebase/storage';
import { getAuth, connectAuthEmulator, Auth } from 'firebase/auth';

// Enhanced Firebase configuration with extensive debugging
console.log('=== Firebase Configuration Debug ===');
console.log('Environment:', process.env.NODE_ENV);
console.log('Current URL:', window.location.href);

// Firebase configuration type
interface FirebaseConfig {
  apiKey: string;
  authDomain: string;
  projectId: string;
  storageBucket?: string;
  messagingSenderId?: string;
  appId?: string;
  measurementId?: string;
}

// Check all environment variables
const envVars: FirebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY || '',
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN || '',
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID || '',
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET || '',
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID || '',
  appId: process.env.REACT_APP_FIREBASE_APP_ID || '',
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID || ''
};

console.log('Environment Variables:', envVars);

// Check if environment variables are properly loaded
const useEnvVars = Object.values(envVars).every(value => value && value.trim() !== '');
console.log('Using environment variables:', useEnvVars);

// Hard-coded configuration as fallback with your actual Firebase project values
const hardCodedConfig: FirebaseConfig = {
  apiKey: "AIzaSyB_d8xpQL94ZWMxx5WyqOi_JypKS7xjA78",
  authDomain: "fitness-food-app-9d41d.firebaseapp.com",
  projectId: "fitness-food-app-9d41d",
  storageBucket: "fitness-food-app-9d41d.firebasestorage.app",
  messagingSenderId: "175044367442",
  appId: "1:175044367442:web:3b38fe992db32996b5fb8b",
  measurementId: "G-WNSQXS16JH"
};

// Use environment variables if available, otherwise use hard-coded values
const firebaseConfig: FirebaseConfig = useEnvVars ? envVars : hardCodedConfig;

console.log('Final Firebase Config:', {
  ...firebaseConfig,
  apiKey: firebaseConfig.apiKey ? `${firebaseConfig.apiKey.substring(0, 10)}...` : 'MISSING'
});

// Validate required fields
const requiredFields: (keyof FirebaseConfig)[] = ['apiKey', 'authDomain', 'projectId'];
const missingFields = requiredFields.filter(field => !firebaseConfig[field]);

if (missingFields.length > 0) {
  console.error('Missing required Firebase config fields:', missingFields);
  throw new Error(`Missing Firebase configuration: ${missingFields.join(', ')}`);
}

console.log('=== Initializing Firebase ===');

// Initialize Firebase with error handling
const firebaseApp: FirebaseApp = initializeApp(firebaseConfig);
console.log('Firebase app initialized successfully');

// Initialize services with error handling
console.log('=== Initializing Firebase Services ===');

const db: Firestore = getFirestore(firebaseApp);
console.log('Firestore initialized successfully');

const storage: FirebaseStorage = getStorage(firebaseApp);
console.log('Storage initialized successfully');

const auth: Auth = getAuth(firebaseApp);
console.log('Auth initialized successfully');

// Add auth state change listener for debugging
auth.onAuthStateChanged((user) => {
  console.log('=== Auth State Changed ===');
  if (user) {
    console.log('User logged in:', {
      uid: user.uid,
      email: user.email,
      displayName: user.displayName,
      emailVerified: user.emailVerified
    });
  } else {
    console.log('User logged out');
  }
});

// Add token refresh listener
auth.onIdTokenChanged(async (user) => {
  console.log('=== Token Changed ===');
  if (user) {
    try {
      const token = await user.getIdToken();
      console.log('New token obtained:', token.substring(0, 20) + '...');
    } catch (error) {
      console.error('Error getting token:', error);
    }
  }
});

// Add global error handler for Firebase operations
window.addEventListener('unhandledrejection', (event) => {
  if (event.reason && event.reason.message && event.reason.message.includes('firebase')) {
    console.error('=== Unhandled Firebase Error ===');
    console.error('Error:', event.reason);
    console.error('Stack:', event.reason.stack);
  }
});

// Export with debug logging
console.log('=== Exporting Firebase Instances ===');
console.log('App:', !!firebaseApp);
console.log('DB:', !!db);
console.log('Storage:', !!storage);
console.log('Auth:', !!auth);

// Export all Firebase instances (no longer optional)
export { firebaseApp, db, storage, auth };
export default firebaseApp;

// Debug helpers
export const debugFirebase = {
  // Test API key validity
  async testApiKey(): Promise<boolean> {
    console.log('=== Testing API Key ===');
    try {
      const response = await fetch(`https://identitytoolkit.googleapis.com/v1/projects/${firebaseConfig.projectId}`, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      console.log('API Key test response:', {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok
      });
      
      return response.ok;
    } catch (error) {
      console.error('API Key test error:', error);
      return false;
    }
  },
  
  // Check Firebase project status
  async checkProjectStatus(): Promise<boolean> {
    console.log('=== Checking Project Status ===');
    try {
      const response = await fetch(`https://firebase.googleapis.com/v1beta1/projects/${firebaseConfig.projectId}`, {
        headers: {
          'Authorization': `Bearer ${firebaseConfig.apiKey}`,
          'Content-Type': 'application/json',
        }
      });
      
      console.log('Project status check:', {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Project data:', data);
      }
      
      return response.ok;
    } catch (error) {
      console.error('Project status check error:', error);
      return false;
    }
  },
  
  // Get current configuration
  getConfig(): Partial<FirebaseConfig> {
    return {
      ...firebaseConfig,
      apiKey: firebaseConfig.apiKey ? `${firebaseConfig.apiKey.substring(0, 10)}...` : 'MISSING'
    };
  }
};