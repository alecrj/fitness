import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const ResetPassword: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Extract oobCode from URL query parameters
  const queryParams = new URLSearchParams(location.search);
  const oobCode = queryParams.get('oobCode');
  
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  
  // Validate the reset code on mount
  useEffect(() => {
    if (!oobCode) {
      setError('Invalid password reset link. Please try again.');
    }
  }, [oobCode]);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }
    
    if (!oobCode) {
      setError('Invalid password reset link');
      return;
    }
    
    try {
      setError('');
      setLoading(true);
      
      // In a real implementation, we would call Firebase's confirmPasswordReset method here
      // For this placeholder, we'll just show a success message
      setMessage('Your password has been reset successfully. You can now log in with your new password.');
      
      // Clear form
      setPassword('');
      setConfirmPassword('');
    } catch (err: any) {
      setError(err.message || 'Failed to reset password');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Set new password
          </h2>
        </div>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}
        
        {message && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
            <span className="block sm:inline">{message}</span>
            <div className="mt-4">
              <Link to="/login" className="font-medium text-green-700 underline">
                Go to login
              </Link>
            </div>
          </div>
        )}
        
        {!message && (
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="password" className="sr-only">New Password</label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="new-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                  placeholder="New Password"
                  disabled={loading || !oobCode}
                />
              </div>
              <div>
                <label htmlFor="confirmPassword" className="sr-only">Confirm New Password</label>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  autoComplete="new-password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                  placeholder="Confirm New Password"
                  disabled={loading || !oobCode}
                />
              </div>
            </div>
            
            <div>
              <button
                type="submit"
                disabled={loading || !oobCode}
                className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white ${
                  loading || !oobCode ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
              >
                {loading ? 'Setting new password...' : 'Reset Password'}
              </button>
            </div>
            
            <div className="text-center">
              <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500">
                Back to login
              </Link>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default ResetPassword;