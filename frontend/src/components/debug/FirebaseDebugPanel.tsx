import React, { useState, useEffect } from 'react';
import { auth } from '../../config/firebase';
import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  connectAuthEmulator
} from 'firebase/auth';

interface DiagnosticResult {
  name: string;
  success: boolean;
  details?: any;
  error?: any;
}

const FixedFirebaseDebugPanel: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<DiagnosticResult[]>([]);
  const [currentUser, setCurrentUser] = useState<any>(null);

  // Listen to auth state changes
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      console.log('Auth state changed:', user);
      setCurrentUser(user);
    });
    return () => unsubscribe();
  }, []);

  const runDiagnostics = async () => {
    setIsLoading(true);
    setResults([]);
    const diagnostics: DiagnosticResult[] = [];

    console.log('=== Starting Fixed Firebase Diagnostics ===');

    // Test 1: Firebase Configuration
    try {
      const config = auth.app.options;
      diagnostics.push({
        name: 'Firebase Configuration',
        success: true,
        details: {
          projectId: config.projectId,
          authDomain: config.authDomain,
          apiKey: config.apiKey ? `${config.apiKey.substring(0, 10)}...` : 'Missing'
        }
      });
    } catch (error) {
      diagnostics.push({
        name: 'Firebase Configuration',
        success: false,
        error: error
      });
    }

    // Test 2: Firebase Auth Initialization
    try {
      const isInitialized = !!auth.app && !!auth.app.name;
      diagnostics.push({
        name: 'Firebase Auth Initialization',
        success: isInitialized,
        details: {
          name: auth.app.name,
          projectId: auth.app.options.projectId
        }
      });
    } catch (error) {
      diagnostics.push({
        name: 'Firebase Auth Initialization',
        success: false,
        error: error
      });
    }

    // Test 3: Test User Registration (using Firebase SDK)
    try {
      console.log('Testing user registration with Firebase SDK...');
      
      // Generate a unique email for testing
      const testEmail = `test-${Date.now()}@example.com`;
      const testPassword = 'TestPassword123!';
      
      // Try to create a user
      const userCredential = await createUserWithEmailAndPassword(auth, testEmail, testPassword);
      
      diagnostics.push({
        name: 'Test User Registration',
        success: true,
        details: {
          uid: userCredential.user.uid,
          email: userCredential.user.email,
          message: 'User created successfully'
        }
      });

      // Clean up - delete the test user
      await userCredential.user.delete();
      console.log('Test user cleaned up');

    } catch (error: any) {
      console.error('Registration test error:', error);
      
      let errorMessage = 'Registration failed';
      let success = false;
      
      // Check specific error codes
      if (error.code === 'auth/network-request-failed') {
        errorMessage = 'Network error - check internet connection';
      } else if (error.code === 'auth/invalid-api-key') {
        errorMessage = 'Invalid API key';
      } else if (error.code === 'auth/project-not-found') {
        errorMessage = 'Firebase project not found';
      } else if (error.code === 'auth/operation-not-allowed') {
        errorMessage = 'Email/password auth not enabled';
      } else {
        errorMessage = error.message || 'Unknown error';
        
        // If it's just a quota exceeded or similar, auth is still working
        if (error.code === 'auth/quota-exceeded' || error.code === 'auth/too-many-requests') {
          success = true;
          errorMessage = 'Auth working (rate limited)';
        }
      }
      
      diagnostics.push({
        name: 'Test User Registration',
        success: success,
        details: { 
          message: errorMessage,
          code: error.code 
        },
        error: error
      });
    }

    // Test 4: Test Existing User Login (if possible)
    try {
      console.log('Testing existing user login...');
      
      // Try to sign in with a test account (this will fail but shows auth is working)
      await signInWithEmailAndPassword(auth, 'existing@test.com', 'password123');
      
      diagnostics.push({
        name: 'Test User Login',
        success: true,
        details: { message: 'Login test successful' }
      });
      
    } catch (error: any) {
      console.log('Login test error (expected):', error);
      
      // These errors actually mean auth is working
      const workingErrors = [
        'auth/user-not-found',
        'auth/wrong-password',
        'auth/invalid-email',
        'auth/invalid-credential',
        'auth/too-many-requests'
      ];
      
      const success = workingErrors.includes(error.code);
      
      diagnostics.push({
        name: 'Test User Login',
        success: success,
        details: { 
          message: success ? 'Auth endpoint working (expected login failure)' : error.message,
          code: error.code
        },
        error: error
      });
    }

    // Test 5: Browser Environment
    try {
      const browserInfo = {
        userAgent: navigator.userAgent,
        online: navigator.onLine,
        protocol: window.location.protocol,
        host: window.location.host,
        cookieEnabled: navigator.cookieEnabled,
        localStorage: !!window.localStorage,
        firebaseSDKVersion: auth.app.options.apiKey ? 'Loaded' : 'Not loaded'
      };
      
      diagnostics.push({
        name: 'Browser Environment',
        success: true,
        details: browserInfo
      });
    } catch (error) {
      diagnostics.push({
        name: 'Browser Environment',
        success: false,
        error: error
      });
    }

    setResults(diagnostics);
    setIsLoading(false);
    
    console.log('=== Diagnostics Complete ===');
    console.log('Results:', diagnostics);
  };

  const clearResults = () => {
    setResults([]);
  };

  const exportResults = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    const exportFileDefaultName = `firebase-debug-${new Date().toISOString()}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const renderResult = (result: DiagnosticResult, index: number) => {
    const { name, success, details, error } = result;
    
    return (
      <div key={index} className="border border-gray-200 rounded-lg p-4 mb-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold">{name}</h3>
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            success 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            {success ? '✓ Pass' : '✗ Fail'}
          </span>
        </div>
        
        {details && (
          <div className="mb-2">
            <h4 className="text-sm font-medium text-gray-700 mb-1">Details:</h4>
            <pre className="text-xs bg-gray-50 p-2 rounded overflow-x-auto">
              {JSON.stringify(details, null, 2)}
            </pre>
          </div>
        )}
        
        {error && (
          <div>
            <h4 className="text-sm font-medium text-red-700 mb-1">Error:</h4>
            <pre className="text-xs bg-red-50 p-2 rounded overflow-x-auto text-red-800">
              {JSON.stringify(error, null, 2)}
            </pre>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Fixed Firebase Debug Panel</h1>
      
      {/* Current Auth Status */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <h2 className="text-lg font-semibold text-blue-800 mb-2">Current Auth Status</h2>
        <p className="text-blue-700">
          {currentUser ? (
            <>Logged in as: {currentUser.email} (UID: {currentUser.uid})</>
          ) : (
            <>Not authenticated</>
          )}
        </p>
      </div>
      
      {/* Control Buttons */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={runDiagnostics}
          disabled={isLoading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Running...' : 'Run Diagnostics'}
        </button>
        
        <button
          onClick={clearResults}
          className="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700"
        >
          Clear Results
        </button>
        
        {results.length > 0 && (
          <button
            onClick={exportResults}
            className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
          >
            Export Results
          </button>
        )}
      </div>
      
      {/* Results */}
      {results.length > 0 && (
        <div>
          <h2 className="text-2xl font-bold mb-4">Diagnostic Results</h2>
          {results.map(renderResult)}
          
          {/* Summary */}
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mt-6">
            <h3 className="text-lg font-semibold mb-2">Summary</h3>
            <p>
              {results.filter(r => r.success).length} of {results.length} tests passed
            </p>
            
            {results.some(r => r.success && r.name.includes('Registration')) && (
              <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded">
                <p className="text-green-800 font-medium">
                  ✅ Firebase Authentication is working correctly!
                </p>
                <p className="text-green-700 text-sm mt-1">
                  Your Firebase setup is properly configured for authentication.
                </p>
              </div>
            )}
          </div>
        </div>
      )}
      
      {isLoading && (
        <div className="text-center">
          <p className="text-gray-600">Running diagnostics...</p>
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mt-2"></div>
        </div>
      )}
    </div>
  );
};

export default FixedFirebaseDebugPanel;