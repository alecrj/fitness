import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { RecipeProvider } from '../contexts/RecipeContext';
import RecipeList from '../components/recipes/RecipeList';
import RecipeDetail from '../components/recipes/RecipeDetail';
import RecipeForm from '../components/recipes/RecipeForm';
import RecipeImport from '../components/recipes/RecipeImport';
import ProtectedRoute from '../components/auth/ProtectedRoute';

/**
 * Recipe routes component with protected routes
 */
const RecipeRoutes: React.FC = () => {
  return (
    <RecipeProvider>
      <Routes>
        {/* List view - protected */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <RecipeList />
            </ProtectedRoute>
          }
        />
        
        {/* Create new recipe - protected */}
        <Route
          path="/create"
          element={
            <ProtectedRoute>
              <RecipeForm />
            </ProtectedRoute>
          }
        />
        
        {/* Edit recipe - protected */}
        <Route
          path="/edit/:id"
          element={
            <ProtectedRoute>
              <RecipeForm />
            </ProtectedRoute>
          }
        />
        
        {/* Import recipe - protected */}
        <Route
          path="/import"
          element={
            <ProtectedRoute>
              <RecipeImport />
            </ProtectedRoute>
          }
        />
        
        {/* View recipe detail - protected */}
        <Route
          path="/:id"
          element={
            <ProtectedRoute>
              <RecipeDetail />
            </ProtectedRoute>
          }
        />
        
        {/* Fallback for unknown paths */}
        <Route path="*" element={<Navigate to="/recipes" replace />} />
      </Routes>
    </RecipeProvider>
  );
};

export default RecipeRoutes;