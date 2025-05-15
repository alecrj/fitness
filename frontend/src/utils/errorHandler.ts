// Error handling utilities
import axios from 'axios';

/**
 * Standard error response interface
 */
export interface ApiError {
  message: string;
  code?: string;
  status?: number;
  details?: any;
}

/**
 * Handle API errors and return a standardized error object
 */
export const handleApiError = (error: any): ApiError => {
  // If it's an axios error
  if (axios.isAxiosError(error)) {
    const response = error.response;
    
    return {
      message: response?.data?.message || error.message || 'An error occurred',
      code: response?.data?.code || error.code,
      status: response?.status,
      details: response?.data
    };
  }
  
  // If it's a regular Error object
  if (error instanceof Error) {
    return {
      message: error.message,
      code: error.name,
      details: error
    };
  }
  
  // If it's just a string
  if (typeof error === 'string') {
    return {
      message: error
    };
  }
  
  // Fallback for unknown error types
  return {
    message: 'An unknown error occurred',
    details: error
  };
};

/**
 * Log errors for debugging
 */
export const logError = (error: any, context?: string): void => {
  const formattedError = handleApiError(error);
  console.error(`Error${context ? ` in ${context}` : ''}:`, formattedError);
  
  // In production, you might want to send this to a logging service
  // like Sentry, LogRocket, etc.
};

/**
 * Get user-friendly error message
 */
export const getUserFriendlyMessage = (error: any): string => {
  const apiError = handleApiError(error);
  
  // Map specific errors to user-friendly messages
  switch (apiError.code) {
    case 'NETWORK_ERROR':
      return 'Unable to connect to server. Please check your internet connection.';
    case 'UNAUTHORIZED':
      return 'You are not authorized to perform this action.';
    case 'FORBIDDEN':
      return 'You do not have permission to access this resource.';
    case 'NOT_FOUND':
      return 'The requested resource was not found.';
    case 'VALIDATION_ERROR':
      return apiError.message || 'Please check your input and try again.';
    default:
      return apiError.message || 'Something went wrong. Please try again.';
  }
};