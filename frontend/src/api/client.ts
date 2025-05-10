import axios from 'axios';
import { auth } from '../config/firebase';

// Create an axios instance for the API
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';
export const client = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
client.interceptors.request.use(
  async (config) => {
    const user = auth.currentUser;
    
    if (user) {
      const token = await user.getIdToken();
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling common error cases
client.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 Unauthorized and we haven't tried refreshing the token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Get a fresh token
        const user = auth.currentUser;
        if (user) {
          const token = await user.getIdToken(true); // Force token refresh
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return client(originalRequest);
        }
      } catch (refreshError) {
        console.error('Error refreshing auth token:', refreshError);
        // Force logout if we can't refresh the token
        auth.signOut().catch(console.error);
      }
    }
    
    return Promise.reject(error);
  }
);

export default client;