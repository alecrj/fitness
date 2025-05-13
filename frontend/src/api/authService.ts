import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut, 
  sendPasswordResetEmail,
  updateProfile,
  sendEmailVerification,
  User,
  AuthError,
  UserCredential
} from 'firebase/auth';
import { auth } from '../config/firebase';
import { client } from './client';
import { UserProfile } from '../types/user';

export interface AuthResponse {
  user: User;
  token: string;
}

// Enhanced error logging function with proper typing
const logAuthError = (operation: string, error: unknown): void => {
  console.log('=== Authentication Error Debug ===');
  console.log(`Operation: ${operation}`);
  
  if (error instanceof Error) {
    console.log('Error Code:', (error as any).code);
    console.log('Error Message:', error.message);
    console.log('Full Error:', error);
    
    // Log request details if available
    if ((error as any).customData) {
      console.log('Custom Data:', (error as any).customData);
    }
    
    // Log network details if this is a network error
    if (error.name === 'NetworkError' || error.message.includes('network')) {
      console.log('Network Error Details:', {
        online: navigator.onLine,
        connection: (navigator as any).connection ? {
          effectiveType: (navigator as any).connection.effectiveType,
          downlink: (navigator as any).connection.downlink,
          rtt: (navigator as any).connection.rtt
        } : 'Not available'
      });
    }
  }
  
  // Log current auth state
  console.log('Current Auth User:', auth.currentUser);
  console.log('Auth App:', auth.app);
  console.log('Auth Config:', (auth as any).config);
};

// Test Firebase connectivity before operations
const testConnectivity = async (): Promise<boolean> => {
  try {
    console.log('=== Testing Firebase Connectivity ===');
    
    // Test if we can reach Firebase servers
    const testUrl = `https://identitytoolkit.googleapis.com/v1/projects/${auth.app.options.projectId}`;
    const response = await fetch(testUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    console.log('Connectivity test result:', {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      headers: Object.fromEntries(response.headers.entries())
    });
    
    return response.status < 500; // Consider 400s as connectivity OK but auth issue
  } catch (error) {
    console.error('Connectivity test failed:', error);
    return false;
  }
};

export const authService = {
  // Register a new user with enhanced error handling
  async register(email: string, password: string, name: string): Promise<AuthResponse> {
    console.log('=== Starting Registration ===');
    console.log('Email:', email);
    console.log('Name:', name);
    
    // Test connectivity first
    const isConnected = await testConnectivity();
    if (!isConnected) {
      throw new Error('Unable to connect to Firebase servers. Please check your internet connection.');
    }
    
    try {
      console.log('Calling createUserWithEmailAndPassword...');
      const userCredential: UserCredential = await createUserWithEmailAndPassword(auth, email, password);
      console.log('User created successfully:', userCredential.user.uid);
      
      const user = userCredential.user;
      
      // Update the user's display name
      console.log('Updating display name...');
      await updateProfile(user, { displayName: name });
      console.log('Display name updated successfully');
      
      // Send email verification
      console.log('Sending email verification...');
      await sendEmailVerification(user);
      console.log('Email verification sent successfully');
      
      // Get ID token
      console.log('Getting ID token...');
      const token = await user.getIdToken();
      console.log('ID token obtained:', token.substring(0, 20) + '...');
      
      // Create user profile on the backend
      console.log('Creating backend profile...');
      try {
        await client.post('/auth/profile', { name });
        console.log('Backend profile created successfully');
      } catch (backendError) {
        console.error('Backend profile creation error:', backendError);
        // Don't throw here as the user was successfully created in Firebase
      }
      
      console.log('=== Registration Complete ===');
      return { user, token };
    } catch (error) {
      logAuthError('register', error);
      throw error;
    }
  },
  
  // Login user with enhanced error handling
  async login(email: string, password: string): Promise<AuthResponse> {
    console.log('=== Starting Login ===');
    console.log('Email:', email);
    
    // Test connectivity first
    const isConnected = await testConnectivity();
    if (!isConnected) {
      throw new Error('Unable to connect to Firebase servers. Please check your internet connection.');
    }
    
    try {
      console.log('Calling signInWithEmailAndPassword...');
      const userCredential: UserCredential = await signInWithEmailAndPassword(auth, email, password);
      console.log('User signed in successfully:', userCredential.user.uid);
      
      const user = userCredential.user;
      
      // Get ID token
      console.log('Getting ID token...');
      const token = await user.getIdToken();
      console.log('ID token obtained:', token.substring(0, 20) + '...');
      
      console.log('=== Login Complete ===');
      return { user, token };
    } catch (error) {
      logAuthError('login', error);
      throw error;
    }
  },
  
  // Logout user
  async logout(): Promise<void> {
    console.log('=== Starting Logout ===');
    try {
      await signOut(auth);
      console.log('User signed out successfully');
    } catch (error) {
      logAuthError('logout', error);
      throw error;
    }
  },
  
  // Reset password with enhanced error handling
  async resetPassword(email: string): Promise<void> {
    console.log('=== Starting Password Reset ===');
    console.log('Email:', email);
    
    // Test connectivity first
    const isConnected = await testConnectivity();
    if (!isConnected) {
      throw new Error('Unable to connect to Firebase servers. Please check your internet connection.');
    }
    
    try {
      console.log('Sending password reset email...');
      await sendPasswordResetEmail(auth, email, {
        url: window.location.origin + '/login',
      });
      console.log('Password reset email sent successfully');
    } catch (error) {
      logAuthError('resetPassword', error);
      throw error;
    }
  },
  
  // Get current authenticated user
  getCurrentUser(): User | null {
    const user = auth.currentUser;
    console.log('Current user:', user ? user.uid : 'none');
    return user;
  },
  
  // Get profile with enhanced error handling
  async getProfile(): Promise<UserProfile> {
    console.log('=== Getting Profile ===');
    try {
      const response = await client.get('/auth/profile');
      console.log('Profile retrieved successfully');
      return response.data;
    } catch (error) {
      console.error('Get profile error:', error);
      throw error;
    }
  },
  
  // Update profile with enhanced error handling
  async updateProfile(data: Partial<UserProfile>): Promise<UserProfile> {
    console.log('=== Updating Profile ===');
    console.log('Update data:', data);
    try {
      const response = await client.post('/auth/profile', data);
      console.log('Profile updated successfully');
      return response.data;
    } catch (error) {
      console.error('Update profile error:', error);
      throw error;
    }
  },
  
  // Upload profile image with enhanced error handling
  async uploadProfileImage(imageFile: File): Promise<UserProfile> {
    console.log('=== Uploading Profile Image ===');
    console.log('File:', imageFile.name, imageFile.size, 'bytes');
    try {
      const formData = new FormData();
      formData.append('profile_image', imageFile);
      
      const response = await client.post('/auth/profile/image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      console.log('Profile image uploaded successfully');
      return response.data;
    } catch (error) {
      console.error('Upload profile image error:', error);
      throw error;
    }
  },
  
  // Debug helper to check auth state
  async debugAuthState(): Promise<void> {
    console.log('=== Auth State Debug ===');
    console.log('Current user:', auth.currentUser);
    console.log('App options:', auth.app.options);
    
    if (auth.currentUser) {
      try {
        const token = await auth.currentUser.getIdToken();
        console.log('ID token available:', !!token);
        console.log('Token length:', token.length);
      } catch (error) {
        console.error('Error getting token:', error);
      }
    }
  }
};