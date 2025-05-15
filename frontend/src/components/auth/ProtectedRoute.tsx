import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

interface ProtectedRouteProps {
  redirectPath?: string;
  children?: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  redirectPath = '/login',
  children
}) => {
  const { currentUser, loading } = useAuth();
  
  if (loading) {
    // Show loading spinner while checking authentication
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }
  
  if (!currentUser) {
    // Redirect to login if not authenticated
    return <Navigate to={redirectPath} replace />;
  }
  
  // Render children if available, otherwise render the Outlet (nested routes)
  return <>{children ? children : <Outlet />}</>;
};

export default ProtectedRoute;