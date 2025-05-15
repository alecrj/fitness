import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { 
  getAuth, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut, 
  sendPasswordResetEmail,
  onAuthStateChanged,
  updateProfile,
  sendEmailVerification,
  User as FirebaseUser
} from 'firebase/auth';
import { doc, setDoc, getDoc, updateDoc } from 'firebase/firestore';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { auth, db, storage } from '../config/firebase';
import { AuthContextType, AuthUser } from '../types/auth';
import { UserProfile } from '../types/user';

// Create the auth context with a default undefined value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Props for the AuthProvider component
interface AuthProviderProps {
  children: ReactNode;
}

// Convert Firebase User to our AuthUser type
const mapFirebaseUserToAuthUser = (user: FirebaseUser): AuthUser => {
  return {
    uid: user.uid,
    email: user.email,
    displayName: user.displayName,
    photoURL: user.photoURL,
    emailVerified: user.emailVerified
  };
};

// Auth provider component
export function AuthProvider({ children }: AuthProviderProps) {
  const [currentUser, setCurrentUser] = useState<AuthUser | null>(null);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Register a new user
  async function register(email: string, password: string, name: string): Promise<AuthUser> {
    try {
      setError("");
      // Create the user in Firebase Auth
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      
      // Update the user's display name
      await updateProfile(user, { displayName: name });
      
      // Send email verification
      await sendEmailVerification(user);
      
      // Create a user profile document in Firestore
      await setDoc(doc(db, "users", user.uid), {
        id: user.uid,
        name: name,
        email: email,
        created_at: new Date(),
        updated_at: new Date(),
        following_count: 0,
        follower_count: 0,
        metadata: {
          onboarding_completed: false,
          version: 1
        }
      });
      
      return mapFirebaseUserToAuthUser(user);
    } catch (error: any) {
      setError(error.message);
      throw error;
    }
  }

  // Login with email and password
  async function login(email: string, password: string): Promise<AuthUser> {
    try {
      setError("");
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      return mapFirebaseUserToAuthUser(userCredential.user);
    } catch (error: any) {
      setError(error.message);
      throw error;
    }
  }

  // Logout the current user
  async function logout(): Promise<void> {
    try {
      setError("");
      await signOut(auth);
      setUserProfile(null);
    } catch (error: any) {
      setError(error.message);
      throw error;
    }
  }

  // Reset password
  async function resetPassword(email: string): Promise<void> {
    try {
      setError("");
      await sendPasswordResetEmail(auth, email);
    } catch (error: any) {
      setError(error.message);
      throw error;
    }
  }

  // Update profile information
  async function updateUserProfile(data: Partial<UserProfile>): Promise<void> {
    try {
      setError("");
      const user = auth.currentUser;
      
      if (!user) {
        throw new Error("No authenticated user found");
      }
      
      const userDocRef = doc(db, "users", user.uid);
      
      // If there's a profile image to upload
      const profileImage = (data as any).profileImage as File | undefined;
      if (profileImage) {
        const storageRef = ref(storage, `profile_images/${user.uid}`);
        await uploadBytes(storageRef, profileImage);
        const downloadURL = await getDownloadURL(storageRef);
        
        // Update auth profile with photo URL
        await updateProfile(user, { photoURL: downloadURL });
        
        // Add the URL to the data to be saved
        data.profile_image_url = downloadURL;
        delete (data as any).profileImage; // Remove the file object
      }
      
      // Update the Firestore document
      await updateDoc(userDocRef, {
        ...data,
        updated_at: new Date()
      });
      
      // Refresh the user profile
      await fetchUserProfile();
    } catch (error: any) {
      setError(error.message);
      throw error;
    }
  }

  // Fetch the current user's profile from Firestore
  async function fetchUserProfile(): Promise<UserProfile | null> {
    try {
      const user = auth.currentUser;
      
      if (!user) {
        setUserProfile(null);
        return null;
      }
      
      const userDocRef = doc(db, "users", user.uid);
      const userDoc = await getDoc(userDocRef);
      
      if (userDoc.exists()) {
        const profileData = userDoc.data() as UserProfile;
        setUserProfile(profileData);
        return profileData;
      } else {
        // If the profile doesn't exist yet (edge case), create it
        const newProfile: UserProfile = {
          id: user.uid,
          name: user.displayName || '',
          email: user.email || '',
          profile_image_url: user.photoURL || '',
          created_at: new Date(),
          updated_at: new Date(),
          following_count: 0,
          follower_count: 0,
          metadata: {
            onboarding_completed: false,
            version: 1
          }
        };
        
        await setDoc(userDocRef, newProfile);
        setUserProfile(newProfile);
        return newProfile;
      }
    } catch (error: any) {
      setError(error.message);
      console.error("Error fetching user profile:", error);
      return null;
    }
  }

  // Check if the user has completed onboarding
  function hasCompletedOnboarding(): boolean {
    return userProfile?.metadata?.onboarding_completed || false;
  }

  // Update onboarding status
  async function completeOnboarding(): Promise<void> {
    try {
      const user = auth.currentUser;
      
      if (!user) {
        throw new Error("No authenticated user found");
      }
      
      const userDocRef = doc(db, "users", user.uid);
      
      await updateDoc(userDocRef, {
        "metadata.onboarding_completed": true,
        updated_at: new Date()
      });
      
      // Update local state
      if (userProfile) {
        setUserProfile({
          ...userProfile,
          metadata: {
            ...userProfile.metadata,
            onboarding_completed: true
          },
          updated_at: new Date() as any // TypeScript fix
        });
      }
    } catch (error: any) {
      setError(error.message);
      throw error;
    }
  }

  // Effect for handling auth state changes
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        setCurrentUser(mapFirebaseUserToAuthUser(user));
        await fetchUserProfile();
      } else {
        setCurrentUser(null);
        setUserProfile(null);
      }
      
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  // Context value
  const value: AuthContextType = {
    currentUser,
    userProfile,
    loading,
    error,
    register,
    login,
    logout,
    resetPassword,
    updateUserProfile,
    fetchUserProfile,
    hasCompletedOnboarding,
    completeOnboarding
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

// Custom hook to use the auth context
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}