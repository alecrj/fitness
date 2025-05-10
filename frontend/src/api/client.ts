import axios from 'axios';
import { auth } from '../config/firebase';

// Create axios instance
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use(
  async (config) => {
    try {
      const currentUser = auth.currentUser;
      if (currentUser) {
        const token = await currentUser.getIdToken();
        // Fix for AxiosRequestHeaders type error
        config.headers = config.headers || {};
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error getting auth token:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle responses
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      const status = error.response.status;
      
      if (status === 401) {
        console.log('Session expired. Please sign in again.');
      } else if (status === 403) {
        console.log('You do not have permission to access this resource.');
      } else if (status === 500) {
        console.log('A server error occurred. Please try again later.');
      }
    } else if (error.request) {
      console.log('Network error. Please check your connection.');
    } else {
      console.log('An error occurred. Please try again.');
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;