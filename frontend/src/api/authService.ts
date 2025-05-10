import { 
    createUserWithEmailAndPassword, 
    signInWithEmailAndPassword, 
    signOut, 
    sendPasswordResetEmail,
    updateProfile,
    sendEmailVerification,
    User
  } from 'firebase/auth';
  import { auth } from '../config/firebase';
  import { client } from './client';
  import { UserProfile } from '../types/user';
  
  export interface AuthResponse {
    user: User;
    token: string;
  }
  
  export const authService = {
    // Register a new user
    async register(email: string, password: string, name: string): Promise<AuthResponse> {
      try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        
        // Update the user's display name
        await updateProfile(user, { displayName: name });
        
        // Send email verification
        await sendEmailVerification(user);
        
        const token = await user.getIdToken();
        
        // Create user profile on the backend
        await client.post('/auth/profile', { name });
        
        return { user, token };
      } catch (error) {
        console.error('Registration error:', error);
        throw error;
      }
    },
    
    // Login user
    async login(email: string, password: string): Promise<AuthResponse> {
      try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        const token = await user.getIdToken();
        
        return { user, token };
      } catch (error) {
        console.error('Login error:', error);
        throw error;
      }
    },
    
    // Logout user
    async logout(): Promise<void> {
      try {
        await signOut(auth);
      } catch (error) {
        console.error('Logout error:', error);
        throw error;
      }
    },
    
    // Reset password
    async resetPassword(email: string): Promise<void> {
      try {
        await sendPasswordResetEmail(auth, email, {
          url: window.location.origin + '/login',
        });
      } catch (error) {
        console.error('Reset password error:', error);
        throw error;
      }
    },
    
    // Get current authenticated user
    getCurrentUser(): User | null {
      return auth.currentUser;
    },
    
    // Get profile
    async getProfile(): Promise<UserProfile> {
      try {
        const response = await client.get('/auth/profile');
        return response.data;
      } catch (error) {
        console.error('Get profile error:', error);
        throw error;
      }
    },
    
    // Update profile
    async updateProfile(data: Partial<UserProfile>): Promise<UserProfile> {
      try {
        const response = await client.post('/auth/profile', data);
        return response.data;
      } catch (error) {
        console.error('Update profile error:', error);
        throw error;
      }
    },
    
    // Upload profile image
    async uploadProfileImage(imageFile: File): Promise<UserProfile> {
      try {
        const formData = new FormData();
        formData.append('profile_image', imageFile);
        
        const response = await client.post('/auth/profile/image', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        
        return response.data;
      } catch (error) {
        console.error('Upload profile image error:', error);
        throw error;
      }
    }
  };