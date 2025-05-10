import React from 'react';
import './App.css';
import { AuthProvider } from './contexts/AuthContext';
import Login from './components/auth/Login';

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <header className="App-header">
          <h1>Fitness & Food App</h1>
          <Login />
        </header>
      </AuthProvider>
    </div>
  );
}

export default App;