import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
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
  
  // Auth service functions
  export const register = async (email: string, password: string, name: string) => {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    
    if (userCredential.user) {
      await updateProfile(userCredential.user, {
        displayName: name,
      });
      
      await createUserProfile({
        name,
        email,
      });
    }
    
    return userCredential;
  };
  
  export const login = async (email: string, password: string) => {
    return signInWithEmailAndPassword(auth, email, password);
  };
  
  export const logout = async () => {
    return signOut(auth);
  };
  
  export const createUserProfile = async (profile: UserProfile) => {
    const response = await apiClient.post('/auth/profile', profile);
    return response.data;
  };
  
  export const getCurrentUserProfile = async () => {
    const response = await apiClient.get('/auth/profile');
    return response.data;
  };
  
  // Export all functions as a service object as well
  const authService = {
    register,
    login,
    logout,
    createUserProfile,
    getCurrentUserProfile
  };
  
  export default authService;