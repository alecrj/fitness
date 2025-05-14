import axios from 'axios';
import { auth } from '../config/firebase';

// Create an axios instance for the API
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Request interceptor to add auth header with Firebase token
client.interceptors.request.use(
  async (config) => {
    try {
      // Get the current user from Firebase
      const user = auth.currentUser;
      
      if (user) {
        // Get Firebase ID token
        const token = await user.getIdToken();
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error in request interceptor:', error);
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling auth errors
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If we get a 401 and haven't already tried to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const user = auth.currentUser;
        
        if (user) {
          // Force refresh the token
          const token = await user.getIdToken(true);
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return client(originalRequest);
        }
      } catch (refreshError) {
        console.error('Error refreshing token:', refreshError);
        // Redirect to login page here if needed
      }
    }
    
    return Promise.reject(error);
  }
);

// Export both named and default exports to support both import styles
export { client };
export default client;