export interface UserProfile {
    id: string;
    name: string;
    email?: string;
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
  
  export interface PartialUserProfile {
    name?: string;
    profile_image_url?: string;
    metadata?: {
      onboarding_completed?: boolean;
      version?: number;
    };
  }
  
  export interface UserProfileUpdateData {
    name?: string;
    profile_image_url?: string;
    profileImage?: File;
    metadata?: {
      onboarding_completed?: boolean;
      version?: number;
    };
  }
  
  export interface ProfileFormData {
    name: string;
    profileImage?: File;
  }