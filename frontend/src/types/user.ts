/**
 * User profile data
 */
export interface UserProfile {
  id: string;
  name: string;
  email: string;
  profile_image_url?: string;
  created_at: Date | string;
  updated_at: Date | string;
  following_count: number;
  follower_count: number;
  metadata: {
    onboarding_completed: boolean;
    version: number;
  };
}

/**
 * Partial user profile for updates
 */
export type PartialUserProfile = Partial<UserProfile>;