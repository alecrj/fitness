import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    UserCredential,
    updateProfile,
    sendPasswordResetEmail,
  } from 'firebase/auth';
  import { auth } from '../config/firebase';
  import apiClient from './client';
  
  // User profile interface
  export interface UserProfile {
    id?: string;
    name: string;
    email: string;
    profile_image_url?: string;
  }
  
  // Auth service
  export const authService = {
    // Register user
    async register(email: string, password: string, name: string): Promise<UserCredential> {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      
      if (userCredential.user) {
        await updateProfile(userCredential.user, {
          displayName: name,
        });
        
        await this.createUserProfile({
          name,
          email,
        });
      }
      
      return userCredential;
    },
    
    // Login user
    async login(email: string, password: string): Promise<UserCredential> {
      return signInWithEmailAndPassword(auth, email, password);
    },
    
    // Logout user
    async logout(): Promise<void> {
      return signOut(auth);
    },
    
    // Create profile in backend
    async createUserProfile(profile: UserProfile): Promise<UserProfile> {
      const response = await apiClient.post('/auth/profile', profile);
      return response.data;
    },
    
    // Get current user profile
    async getCurrentUserProfile(): Promise<UserProfile> {
      const response = await apiClient.get('/auth/profile');
      return response.data;
    },
  };
  
  export default authService;