import React, { useState, useEffect } from 'react';
import { auth } from '../config/firebase';
import { debugFirebase } from '../config/firebase';
import { authService } from '../api/authService';

interface TestResult {
  name: string;
  success: boolean;
  details: any;
  error?: any;
}

export const FirebaseDebugPanel: React.FC = () => {
  const [results, setResults] = useState<TestResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [testEmail] = useState('test@example.com');
  const [testPassword] = useState('testpassword123');

  const addResult = (result: TestResult) => {
    setResults(prev => [...prev, result]);
  };

  const runDiagnostics = async () => {
    setIsRunning(true);
    setResults([]);

    console.log('=== Starting Firebase Diagnostics ===');

    // Test 1: Check Firebase configuration
    addResult({
      name: 'Firebase Configuration',
      success: true,
      details: debugFirebase.getConfig()
    });

    // Test 2: Check Firebase app initialization
    try {
      addResult({
        name: 'Firebase App Initialization',
        success: !!auth.app,
        details: {
          name: auth.app?.name,
          options: auth.app?.options
        }
      });
    } catch (error) {
      addResult({
        name: 'Firebase App Initialization',
        success: false,
        details: null,
        error
      });
    }

    // Test 3: Test API key validity
    try {
      const apiKeyValid = await debugFirebase.testApiKey();
      addResult({
        name: 'API Key Test',
        success: apiKeyValid,
        details: { apiKeyValid }
      });
    } catch (error) {
      addResult({
        name: 'API Key Test',
        success: false,
        details: null,
        error
      });
    }

    // Test 4: Check project status
    try {
      const projectOk = await debugFirebase.checkProjectStatus();
      addResult({
        name: 'Project Status Check',
        success: projectOk,
        details: { projectOk }
      });
    } catch (error) {
      addResult({
        name: 'Project Status Check',
        success: false,
        details: null,
        error
      });
    }

    // Test 5: Check connectivity to Firebase Auth
    try {
      const response = await fetch(`https://identitytoolkit.googleapis.com/v1/projects/${auth.app.options.projectId}`, {
        method: 'HEAD'
      });
      
      addResult({
        name: 'Firebase Auth Connectivity',
        success: response.status < 500,
        details: {
          status: response.status,
          statusText: response.statusText,
          headers: Object.fromEntries(response.headers.entries())
        }
      });
    } catch (error) {
      addResult({
        name: 'Firebase Auth Connectivity',
        success: false,
        details: null,
        error
      });
    }

    // Test 6: Test authentication attempt
    try {
      console.log('Attempting test authentication...');
      await authService.register(testEmail, testPassword, 'Test User');
      
      addResult({
        name: 'Test Authentication',
        success: true,
        details: { message: 'Successfully created test user' }
      });
    } catch (error) {
      addResult({
        name: 'Test Authentication',
        success: false,
        details: {
          code: (error as any).code,
          message: (error as any).message,
          stack: (error as any).stack?.substring(0, 200)
        },
        error
      });
    }

    // Test 7: Check browser environment
    addResult({
      name: 'Browser Environment',
      success: true,
      details: {
        userAgent: navigator.userAgent,
        online: navigator.onLine,
        protocol: window.location.protocol,
        host: window.location.host,
        cookieEnabled: navigator.cookieEnabled,
        localStorage: typeof(Storage) !== "undefined",
        webgl: !!window.WebGLRenderingContext,
        webrtc: !!(navigator.getUserMedia || navigator.mediaDevices)
      }
    });

    setIsRunning(false);
    console.log('=== Diagnostics Complete ===');
  };

  useEffect(() => {
    // Run diagnostics on mount if in development
    if (process.env.NODE_ENV === 'development') {
      runDiagnostics();
    }
  }, []);

  const clearResults = () => {
    setResults([]);
  };

  const exportResults = () => {
    const resultsJson = JSON.stringify(results, null, 2);
    const blob = new Blob([resultsJson], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `firebase-debug-${new Date().toISOString()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4">Firebase Debug Panel</h2>
      
      <div className="mb-4 space-x-4">
        <button
          onClick={runDiagnostics}
          disabled={isRunning}
          className={`px-4 py-2 rounded ${
            isRunning 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
        >
          {isRunning ? 'Running...' : 'Run Diagnostics'}
        </button>
        
        <button
          onClick={clearResults}
          disabled={isRunning}
          className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 disabled:bg-gray-400"
        >
          Clear Results
        </button>
        
        <button
          onClick={exportResults}
          disabled={results.length === 0}
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400"
        >
          Export Results
        </button>
      </div>

      <div className="space-y-4">
        {results.map((result, index) => (
          <div
            key={index}
            className={`p-4 rounded border-l-4 ${
              result.success 
                ? 'border-green-500 bg-green-50' 
                : 'border-red-500 bg-red-50'
            }`}
          >
            <div className="flex items-center justify-between">
              <h3 className="font-semibold">{result.name}</h3>
              <span className={`px-2 py-1 rounded text-sm ${
                result.success 
                  ? 'bg-green-200 text-green-800' 
                  : 'bg-red-200 text-red-800'
              }`}>
                {result.success ? '✓ Pass' : '✗ Fail'}
              </span>
            </div>
            
            {result.details && (
              <div className="mt-2">
                <p className="text-sm text-gray-600 mb-1">Details:</p>
                <pre className="text-xs bg-gray-100 p-2 rounded overflow-auto max-h-40">
                  {JSON.stringify(result.details, null, 2)}
                </pre>
              </div>
            )}
            
            {result.error && (
              <div className="mt-2">
                <p className="text-sm text-red-600 mb-1">Error:</p>
                <pre className="text-xs bg-red-100 p-2 rounded overflow-auto max-h-40 text-red-800">
                  {JSON.stringify(result.error, null, 2)}
                </pre>
              </div>
            )}
          </div>
        ))}
      </div>

      {results.length === 0 && !isRunning && (
        <div className="text-center text-gray-500 py-8">
          No diagnostics results yet. Click "Run Diagnostics" to start.
        </div>
      )}
    </div>
  );
};

export default FirebaseDebugPanel;