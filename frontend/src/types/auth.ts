// Auth types for the application
import { UserProfile } from './user';

/**
 * Represents a user in the auth system
 */
export interface AuthUser {
  uid: string;
  email: string | null;
  displayName: string | null;
  photoURL: string | null;
  emailVerified: boolean;
}

/**
 * Auth context type for the application
 */
export interface AuthContextType {
  currentUser: AuthUser | null;
  userProfile: UserProfile | null;
  loading: boolean;
  error: string;
  
  // Authentication methods
  register: (email: string, password: string, name: string) => Promise<AuthUser>;
  login: (email: string, password: string) => Promise<AuthUser>;
  logout: () => Promise<void>; // This should match the method name in your AuthContext
  resetPassword: (email: string) => Promise<void>;
  
  // Profile methods
  updateUserProfile: (data: Partial<UserProfile>) => Promise<void>;
  fetchUserProfile: () => Promise<UserProfile | null>;
  
  // Onboarding methods
  hasCompletedOnboarding: () => boolean;
  completeOnboarding: () => Promise<void>;
}

/**
 * User registration data
 */
export interface RegisterFormData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

/**
 * Login form data
 */
export interface LoginFormData {
  email: string;
  password: string;
  rememberMe?: boolean;
}

/**
 * Password reset form data
 */
export interface PasswordResetFormData {
  email: string;
}