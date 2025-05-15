// Profile service for user profile management
import { client } from './client';
import { UserProfile } from '../types/user';

export const profileService = {
  /**
   * Get current user's profile
   */
  async getProfile(): Promise<UserProfile> {
    const response = await client.get('/auth/profile');
    return response.data;
  },

  /**
   * Update user profile
   */
  async updateProfile(data: Partial<UserProfile>): Promise<UserProfile> {
    const response = await client.post('/auth/profile', data);
    return response.data;
  },

  /**
   * Upload profile image
   */
  async uploadProfileImage(imageFile: File): Promise<UserProfile> {
    const formData = new FormData();
    formData.append('profile_image', imageFile);
    
    const response = await client.post('/auth/profile/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  }
};

export default profileService;