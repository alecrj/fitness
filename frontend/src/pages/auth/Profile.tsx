import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { UserProfile } from '../../types/user';

const Profile: React.FC = () => {
  const { currentUser, userProfile, updateUserProfile, logout } = useAuth();
  const navigate = useNavigate();
  
  const [name, setName] = useState('');
  const [profileImage, setProfileImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Load user data
  useEffect(() => {
    if (userProfile) {
      setName(userProfile.name || '');
    } else if (currentUser) {
      setName(currentUser.displayName || '');
    }
    
    if (currentUser?.photoURL) {
      setPreviewUrl(currentUser.photoURL);
    }
  }, [currentUser, userProfile]);
  
  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      
      // Validate file type and size
      if (!file.type.match('image.*')) {
        setError('Please select an image file');
        return;
      }
      
      if (file.size > 5 * 1024 * 1024) { // 5MB
        setError('Image must be less than 5MB');
        return;
      }
      
      setProfileImage(file);
      
      // Create preview URL
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      setError('');
      setSuccess('');
      setLoading(true);
      
      const updatedProfile: Partial<UserProfile> = {
        name
      };
      
      if (profileImage) {
        // We need to cast this because the TypeScript definition doesn't include the file
        (updatedProfile as any).profileImage = profileImage;
      }
      
      await updateUserProfile(updatedProfile);
      setSuccess('Profile updated successfully');
    } catch (err: any) {
      setError(err.message || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };
  
  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (err: any) {
      setError(err.message || 'Failed to log out');
    }
  };
  
  return (
    <div className="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Profile</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}
      
      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-6" role="alert">
          <span className="block sm:inline">{success}</span>
        </div>
      )}
      
      <div className="bg-white shadow-md rounded-lg p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Profile image */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Profile Image
            </label>
            <div className="flex items-center space-x-6">
              <div className="w-24 h-24 rounded-full overflow-hidden bg-gray-100 flex items-center justify-center">
                {previewUrl ? (
                  <img
                    src={previewUrl}
                    alt="Profile preview"
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <span className="text-gray-400 text-4xl">
                    {name ? name[0].toUpperCase() : '?'}
                  </span>
                )}
              </div>
              <div>
                <input
                  type="file"
                  id="profileImage"
                  onChange={handleImageChange}
                  className="hidden"
                  accept="image/*"
                />
                <label
                  htmlFor="profileImage"
                  className="cursor-pointer bg-gray-200 hover:bg-gray-300 py-2 px-4 rounded-md text-sm font-medium text-gray-700"
                >
                  Change Image
                </label>
              </div>
            </div>
          </div>
          
          {/* Name */}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700">
              Name
            </label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="Your name"
            />
          </div>
          
          {/* Email (read-only) */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={currentUser?.email || ''}
              readOnly
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-gray-50 text-gray-500 sm:text-sm"
            />
          </div>
          
          {/* Submit button */}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className={`py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                loading ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'
              } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
            >
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
        
        {/* Account Actions */}
        <div className="mt-8 pt-8 border-t border-gray-200">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Account</h2>
          
          <div className="space-y-4">
            <div>
              <button
                onClick={handleLogout}
                className="text-red-600 hover:text-red-800 font-medium"
              >
                Log Out
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;