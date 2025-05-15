import React, { useState } from 'react';
import { 
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  sendPasswordResetEmail,
  sendEmailVerification,
  updateProfile,
  onAuthStateChanged
} from 'firebase/auth';
import { doc, setDoc } from 'firebase/firestore';
import { auth, db } from '../../config/firebase';
import Button from '../ui/Button';
import Input from '../ui/Input';
import Alert from '../ui/Alert';

const FirebaseDebugPanel: React.FC = () => {
  const [email, setEmail] = useState('test@example.com');
  const [password, setPassword] = useState('password123');
  const [name, setName] = useState('Test User');
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testFirebaseConnection = async (): Promise<string> => {
    let testResult = 'Testing Firebase connection...\n';
    
    try {
      // Test 1: Check Firebase auth initialization
      if (auth) {
        testResult += '✅ Firebase Auth initialized\n';
      } else {
        testResult += '❌ Firebase Auth not initialized\n';
        return testResult;
      }
      
      // Test 2: Check Firestore connection
      if (db) {
        testResult += '✅ Firestore initialized\n';
      } else {
        testResult += '❌ Firestore not initialized\n';
      }
      
      // Test 3: Check environment variables
      const apiKey = process.env.REACT_APP_FIREBASE_API_KEY;
      const projectId = process.env.REACT_APP_FIREBASE_PROJECT_ID;
      const authDomain = process.env.REACT_APP_FIREBASE_AUTH_DOMAIN;
      
      testResult += `API Key: ${apiKey ? '✅ Set' : '❌ Missing'}\n`;
      testResult += `Project ID: ${projectId ? '✅ Set' : '❌ Missing'}\n`;
      testResult += `Auth Domain: ${authDomain ? '✅ Set' : '❌ Missing'}\n`;
      
      // Test 4: Test auth state listener
      try {
        const currentUser = auth.currentUser;
        testResult += `Current User: ${currentUser ? '✅ Found' : 'ℹ️ None (not logged in)'}\n`;
      } catch (error: any) {
        testResult += `❌ Auth state error: ${error.message}\n`;
      }
      
    } catch (error: any) {
      testResult += `❌ Error: ${error.message}\n`;
    }
    
    return testResult;
  };

  const testRegistration = async (): Promise<string> => {
    let testResult = 'Testing user registration...\n';
    
    try {
      // Create user with Firebase
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      
      testResult += `✅ Registration successful\n`;
      testResult += `User ID: ${user.uid}\n`;
      testResult += `Email: ${user.email}\n`;
      testResult += `Email verified: ${user.emailVerified ? 'Yes' : 'No'}\n`;
      
      // Update display name
      await updateProfile(user, { displayName: name });
      testResult += `✅ Display name updated to: ${name}\n`;
      
      // Create Firestore profile
      await setDoc(doc(db, "users", user.uid), {
        id: user.uid,
        name: name,
        email: email,
        created_at: new Date(),
        updated_at: new Date(),
        following_count: 0,
        follower_count: 0,
        metadata: {
          onboarding_completed: false,
          version: 1
        }
      });
      testResult += `✅ Firestore profile created\n`;
      
      // Send email verification
      await sendEmailVerification(user);
      testResult += `✅ Email verification sent\n`;
      
    } catch (error: any) {
      if (error.code === 'auth/email-already-in-use') {
        testResult += `ℹ️ User already exists (${email})\n`;
      } else {
        testResult += `❌ Registration error: ${error.message}\n`;
      }
    }
    
    return testResult;
  };

  const testLogin = async (): Promise<string> => {
    let testResult = 'Testing user login...\n';
    
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      
      testResult += `✅ Login successful\n`;
      testResult += `User ID: ${user.uid}\n`;
      testResult += `Email: ${user.email}\n`;
      testResult += `Display Name: ${user.displayName || 'Not set'}\n`;
      testResult += `Email verified: ${user.emailVerified ? 'Yes' : 'No'}\n`;
      testResult += `Last sign in: ${user.metadata.lastSignInTime || 'N/A'}\n`;
      
      // Get Firebase ID token
      try {
        const token = await user.getIdToken();
        testResult += `✅ ID Token obtained (${token.length} chars)\n`;
      } catch (tokenError: any) {
        testResult += `❌ Token error: ${tokenError.message}\n`;
      }
      
    } catch (error: any) {
      if (error.code === 'auth/user-not-found') {
        testResult += `❌ User not found. Try registering first.\n`;
      } else if (error.code === 'auth/wrong-password') {
        testResult += `❌ Incorrect password\n`;
      } else {
        testResult += `❌ Login error: ${error.message}\n`;
      }
    }
    
    return testResult;
  };

  const getCurrentUser = async (): Promise<string> => {
    let testResult = 'Getting current user...\n';
    
    try {
      const user = auth.currentUser;
      
      if (user) {
        testResult += `✅ Current user found\n`;
        testResult += `User ID: ${user.uid}\n`;
        testResult += `Email: ${user.email}\n`;
        testResult += `Display Name: ${user.displayName || 'Not set'}\n`;
        testResult += `Email verified: ${user.emailVerified ? 'Yes' : 'No'}\n`;
        testResult += `Provider: ${user.providerId}\n`;
        testResult += `Created: ${user.metadata.creationTime}\n`;
        testResult += `Last sign in: ${user.metadata.lastSignInTime}\n`;
        
        // Test getting fresh token
        try {
          const token = await user.getIdToken(true); // Force refresh
          testResult += `✅ Fresh token obtained\n`;
        } catch (tokenError: any) {
          testResult += `❌ Token refresh error: ${tokenError.message}\n`;
        }
      } else {
        testResult += 'ℹ️ No current user (not logged in)\n';
      }
    } catch (error: any) {
      testResult += `❌ Error: ${error.message}\n`;
    }
    
    return testResult;
  };

  const testLogout = async (): Promise<string> => {
    let testResult = 'Testing logout...\n';
    
    try {
      const currentUser = auth.currentUser;
      if (!currentUser) {
        testResult += 'ℹ️ No user logged in to logout\n';
        return testResult;
      }
      
      await signOut(auth);
      testResult += `✅ Logout successful\n`;
      
      // Verify logout
      const userAfterLogout = auth.currentUser;
      if (!userAfterLogout) {
        testResult += `✅ User completely signed out\n`;
      } else {
        testResult += `⚠️ User still appears to be signed in\n`;
      }
      
    } catch (error: any) {
      testResult += `❌ Logout error: ${error.message}\n`;
    }
    
    return testResult;
  };

  const testPasswordReset = async (): Promise<string> => {
    let testResult = 'Testing password reset...\n';
    
    try {
      await sendPasswordResetEmail(auth, email);
      testResult += `✅ Password reset email sent to ${email}\n`;
      testResult += `ℹ️ Check your email for reset instructions\n`;
    } catch (error: any) {
      if (error.code === 'auth/user-not-found') {
        testResult += `❌ No user found with email: ${email}\n`;
      } else {
        testResult += `❌ Password reset error: ${error.message}\n`;
      }
    }
    
    return testResult;
  };

  // Run all tests at once
  const runAllTests = async () => {
    setLoading(true);
    setResult('Running all Firebase authentication tests...\n\n');
    
    try {
      let allResults = 'FIREBASE AUTHENTICATION TEST SUITE\n';
      allResults += '='.repeat(40) + '\n\n';
      
      // Test 1: Connection
      allResults += '1. CONNECTION TEST\n';
      allResults += '-'.repeat(20) + '\n';
      const connectionResult = await testFirebaseConnection();
      allResults += connectionResult + '\n';
      
      // Test 2: Registration
      allResults += '2. REGISTRATION TEST\n';
      allResults += '-'.repeat(20) + '\n';
      const registrationResult = await testRegistration();
      allResults += registrationResult + '\n';
      
      // Test 3: Login
      allResults += '3. LOGIN TEST\n';
      allResults += '-'.repeat(20) + '\n';
      const loginResult = await testLogin();
      allResults += loginResult + '\n';
      
      // Test 4: Current User
      allResults += '4. CURRENT USER TEST\n';
      allResults += '-'.repeat(20) + '\n';
      const currentUserResult = await getCurrentUser();
      allResults += currentUserResult + '\n';
      
      // Test 5: Password Reset
      allResults += '5. PASSWORD RESET TEST\n';
      allResults += '-'.repeat(20) + '\n';
      const passwordResetResult = await testPasswordReset();
      allResults += passwordResetResult + '\n';
      
      // Test 6: Logout
      allResults += '6. LOGOUT TEST\n';
      allResults += '-'.repeat(20) + '\n';
      const logoutResult = await testLogout();
      allResults += logoutResult + '\n';
      
      // Summary
      allResults += 'TEST SUMMARY\n';
      allResults += '='.repeat(40) + '\n';
      allResults += `Timestamp: ${new Date().toISOString()}\n`;
      allResults += `Test Email: ${email}\n`;
      allResults += `Firebase Project: ${process.env.REACT_APP_FIREBASE_PROJECT_ID}\n`;
      allResults += `Auth Domain: ${process.env.REACT_APP_FIREBASE_AUTH_DOMAIN}\n`;
      
      setResult(allResults);
    } catch (error: any) {
      setResult(prev => prev + `\n❌ Test suite error: ${error.message}\n`);
    } finally {
      setLoading(false);
    }
  };

  // Export results to file
  const exportResults = () => {
    if (!result) {
      alert('No test results to export. Run tests first.');
      return;
    }
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `firebase-debug-results-${timestamp}.txt`;
    
    const blob = new Blob([result], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
        Firebase Authentication Debug Panel
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Test Form */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">Test Credentials</h2>
          
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="test@example.com"
            />
          </div>
          
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="password123"
            />
          </div>
          
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
              Full Name
            </label>
            <Input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Test User"
            />
          </div>
        </div>
        
        {/* Test Buttons */}
        <div className="space-y-3">
          <h2 className="text-xl font-semibold mb-4">Authentication Tests</h2>
          
          {/* Run All Tests Button */}
          <Button
            onClick={runAllTests}
            disabled={loading}
            variant="primary"
            size="lg"
            fullWidth
            loading={loading}
          >
            {loading ? 'Running All Tests...' : 'Run All Tests'}
          </Button>
          
          <div className="border-t pt-3">
            <p className="text-sm text-gray-600 mb-3">Or run individual tests:</p>
            
            <Button
              onClick={async () => {
                setLoading(true);
                const result = await testFirebaseConnection();
                setResult(result);
                setLoading(false);
              }}
              disabled={loading}
              variant="secondary"
              size="md"
              fullWidth
            >
              Test Connection
            </Button>
            
            <Button
              onClick={async () => {
                setLoading(true);
                const result = await testRegistration();
                setResult(result);
                setLoading(false);
              }}
              disabled={loading}
              variant="secondary"
              size="md"
              fullWidth
            >
              Test Registration
            </Button>
            
            <Button
              onClick={async () => {
                setLoading(true);
                const result = await testLogin();
                setResult(result);
                setLoading(false);
              }}
              disabled={loading}
              variant="secondary"
              size="md"
              fullWidth
            >
              Test Login
            </Button>
            
            <Button
              onClick={async () => {
                setLoading(true);
                const result = await getCurrentUser();
                setResult(result);
                setLoading(false);
              }}
              disabled={loading}
              variant="secondary"
              size="md"
              fullWidth
            >
              Get Current User
            </Button>
            
            <Button
              onClick={async () => {
                setLoading(true);
                const result = await testPasswordReset();
                setResult(result);
                setLoading(false);
              }}
              disabled={loading}
              variant="secondary"
              size="md"
              fullWidth
            >
              Test Password Reset
            </Button>
            
            <Button
              onClick={async () => {
                setLoading(true);
                const result = await testLogout();
                setResult(result);
                setLoading(false);
              }}
              disabled={loading}
              variant="danger"
              size="md"
              fullWidth
            >
              Test Logout
            </Button>
          </div>
        </div>
      </div>
      
      {/* Results Section */}
      <div className="mt-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Test Results</h2>
          <Button
            onClick={exportResults}
            disabled={!result}
            variant="secondary"
            size="md"
          >
            Export Results
          </Button>
        </div>
        <div className="bg-gray-100 p-4 rounded-lg">
          <pre className="whitespace-pre-wrap text-sm font-mono text-gray-800 max-h-96 overflow-y-auto">
            {result || 'No tests run yet. Click "Run All Tests" or individual test buttons above.'}
          </pre>
        </div>
      </div>
      
      {/* Info Section */}
      <div className="mt-6">
        <Alert variant="info">
          <div>
            <h3 className="font-semibold">Firebase Debug Information:</h3>
            <p className="mt-1">This panel tests Firebase authentication functionality.</p>
            <ul className="mt-2 list-disc list-inside text-sm">
              <li><strong>Connection Test:</strong> Verifies Firebase initialization and environment variables</li>
              <li><strong>Registration:</strong> Creates new user, sets display name, creates Firestore profile</li>
              <li><strong>Login:</strong> Tests sign-in and token generation</li>
              <li><strong>Current User:</strong> Checks auth state and token refresh</li>
              <li><strong>Password Reset:</strong> Tests email sending functionality</li>
              <li><strong>Logout:</strong> Verifies complete sign-out</li>
              <li>Export results for sharing with development team</li>
            </ul>
          </div>
        </Alert>
      </div>
    </div>
  );
};

export default FirebaseDebugPanel;