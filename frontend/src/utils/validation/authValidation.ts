// Authentication form validation utilities
import { RegisterFormData, LoginFormData, PasswordResetFormData, ResetPasswordFormData } from '../../types/auth';

/**
 * Email validation regex
 */
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/**
 * Password strength validation
 */
export const validatePasswordStrength = (password: string): string[] => {
  const errors: string[] = [];
  
  if (password.length < 6) {
    errors.push('Password must be at least 6 characters long');
  }
  
  if (password.length < 8) {
    errors.push('For better security, use at least 8 characters');
  }
  
  if (!/(?=.*[a-z])/.test(password)) {
    errors.push('Password should contain at least one lowercase letter');
  }
  
  if (!/(?=.*[A-Z])/.test(password)) {
    errors.push('Password should contain at least one uppercase letter');
  }
  
  if (!/(?=.*\d)/.test(password)) {
    errors.push('Password should contain at least one number');
  }
  
  return errors;
};

/**
 * Validate email format
 */
export const validateEmail = (email: string): string | null => {
  if (!email) {
    return 'Email is required';
  }
  
  if (!EMAIL_REGEX.test(email)) {
    return 'Please enter a valid email address';
  }
  
  return null;
};

/**
 * Validate registration form data
 */
export const validateRegistrationForm = (data: RegisterFormData): Record<string, string> => {
  const errors: Record<string, string> = {};
  
  // Name validation
  if (!data.name.trim()) {
    errors.name = 'Name is required';
  } else if (data.name.trim().length < 2) {
    errors.name = 'Name must be at least 2 characters';
  }
  
  // Email validation
  const emailError = validateEmail(data.email);
  if (emailError) {
    errors.email = emailError;
  }
  
  // Password validation
  if (!data.password) {
    errors.password = 'Password is required';
  } else if (data.password.length < 6) {
    errors.password = 'Password must be at least 6 characters';
  }
  
  // Confirm password validation
  if (!data.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password';
  } else if (data.password !== data.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match';
  }
  
  return errors;
};

/**
 * Validate login form data
 */
export const validateLoginForm = (data: LoginFormData): Record<string, string> => {
  const errors: Record<string, string> = {};
  
  // Email validation
  const emailError = validateEmail(data.email);
  if (emailError) {
    errors.email = emailError;
  }
  
  // Password validation
  if (!data.password) {
    errors.password = 'Password is required';
  }
  
  return errors;
};

/**
 * Validate password reset form
 */
export const validatePasswordResetForm = (data: PasswordResetFormData): Record<string, string> => {
  const errors: Record<string, string> = {};
  
  // Email validation
  const emailError = validateEmail(data.email);
  if (emailError) {
    errors.email = emailError;
  }
  
  return errors;
};

/**
 * Validate reset password form (for setting new password)
 */
export const validateResetPasswordForm = (data: ResetPasswordFormData): Record<string, string> => {
  const errors: Record<string, string> = {};
  
  // Password validation
  if (!data.password) {
    errors.password = 'Password is required';
  } else if (data.password.length < 6) {
    errors.password = 'Password must be at least 6 characters';
  }
  
  // Confirm password validation
  if (!data.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password';
  } else if (data.password !== data.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match';
  }
  
  return errors;
};