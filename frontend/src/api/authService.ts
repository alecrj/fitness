import { 
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  sendPasswordResetEmail,
  updatePassword as firebaseUpdatePassword,
  User as FirebaseUser
} from 'firebase/auth';
import { auth } from '../config/firebase';
import { client } from './client';
import { UserProfile } from '../types/user';

// Auth service that works with Firebase auth and the Flask backend
export const authService = {
  // Get current user from Firebase
  async getCurrentUser(): Promise<FirebaseUser | null> {
    return auth.currentUser;
  },

  // Get user session (Firebase doesn't have sessions like Supabase, but we can check currentUser)
  async getSession() {
    const user = auth.currentUser;
    if (user) {
      const token = await user.getIdToken();
      return { user, token };
    }
    return null;
  },

  // Sign in with email and password
  async signIn(email: string, password: string) {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    return { user: userCredential.user };
  },

  // Sign up with email and password
  async signUp(email: string, password: string, name: string) {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    
    // Update the user's display name
    await import('firebase/auth').then(({ updateProfile }) => 
      updateProfile(userCredential.user, { displayName: name })
    );
    
    return { user: userCredential.user };
  },

  // Sign out
  async signOut() {
    await signOut(auth);
  },

  // Reset password
  async resetPassword(email: string) {
    await sendPasswordResetEmail(auth, email);
  },

  // Update password
  async updatePassword(password: string) {
    const user = auth.currentUser;
    if (!user) throw new Error('No authenticated user');
    await firebaseUpdatePassword(user, password);
  },

  // Flask API methods (these use the backend API with Firebase token)
  
  // Get user profile from Flask backend
  async getProfile(): Promise<UserProfile> {
    const response = await client.get('/api/auth/profile');
    return response.data;
  },

  // Update user profile via Flask backend
  async updateProfile(profileData: Partial<UserProfile>): Promise<UserProfile> {
    const response = await client.post('/api/auth/profile', profileData);
    return response.data;
  },

  // Upload profile image via Flask backend
  async uploadProfileImage(file: File): Promise<string> {
    const formData = new FormData();
    formData.append('image', file);
    
    const response = await client.post('/api/auth/profile/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data.image_url;
  },

  // Send email verification
  async sendEmailVerification() {
    const user = auth.currentUser;
    if (!user) throw new Error('No authenticated user');
    
    const { sendEmailVerification } = await import('firebase/auth');
    await sendEmailVerification(user);
  },

  // Get user's ID token for backend authentication
  async getIdToken(): Promise<string | null> {
    const user = auth.currentUser;
    if (!user) return null;
    
    try {
      return await user.getIdToken();
    } catch (error) {
      console.error('Error getting ID token:', error);
      return null;
    }
  },

  // Force refresh the ID token
  async refreshIdToken(): Promise<string | null> {
    const user = auth.currentUser;
    if (!user) return null;
    
    try {
      return await user.getIdToken(true); // true forces refresh
    } catch (error) {
      console.error('Error refreshing ID token:', error);
      return null;
    }
  }
};

export default authService;