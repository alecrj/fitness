import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';

// Auth pages
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import ResetPassword from './pages/auth/ResetPassword';
import Profile from './pages/auth/Profile';

// Layout components
import MainLayout from './components/layouts/MainLayout';

// Debug components (back to original name since you overwrote the file)
import FirebaseDebugPanel from './components/debug/FirebaseDebugPanel';

// Routes
import RecipeRoutes from './routes/RecipeRoutes';
import NutritionRoutes from './routes/NutritionRoutes';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Debug route (accessible without authentication) */}
          <Route path="/debug" element={<FirebaseDebugPanel />} />
          
          {/* Auth routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          
          {/* Protected routes with MainLayout */}
          <Route path="/" element={<MainLayout />}>
            {/* Dashboard (redirect to nutrition dashboard) */}
            <Route index element={<Navigate to="/nutrition/dashboard" />} />
            
            {/* Profile */}
            <Route
              path="profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />
            
            {/* Recipe routes */}
            <Route path="recipes/*" element={<RecipeRoutes />} />
            
            {/* Nutrition routes */}
            <Route path="nutrition/*" element={<NutritionRoutes />} />
            
            {/* Future routes for Social will go here */}
            {/* <Route path="social/*" element={<SocialRoutes />} /> */}
          </Route>
          
          {/* Fallback for unknown routes */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;