import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { ProfileForm } from '../../components/auth/forms/ProfileForm';

const Profile: React.FC = () => {
  const { currentUser, userProfile, loading } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    if (!loading) {
      setIsLoading(false);
    }
  }, [loading]);
  
  // Redirect to login if not authenticated
  if (!isLoading && !currentUser) {
    return <Navigate to="/login" replace />;
  }
  
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Your Profile
            </h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Update your personal information
            </p>
          </div>
          
          <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
            <ProfileForm />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;