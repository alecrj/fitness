import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { NutritionProvider } from '../contexts/NutritionContext';

// Import Nutrition Pages
import Dashboard from '../pages/nutrition/Dashboard';
import FoodItems from '../pages/nutrition/FoodItems';
import FoodItemDetail from '../pages/nutrition/FoodItemDetail';
import AddEditFoodItem from '../pages/nutrition/AddEditFoodItem';
import USDASearch from '../pages/nutrition/USDASearch';
import Meals from '../pages/nutrition/Meals';
import MealDetail from '../pages/nutrition/MealDetail';
import AddEditMeal from '../pages/nutrition/AddEditMeal';

// Import Protected Route component
import ProtectedRoute from '../components/auth/ProtectedRoute';

const NutritionRoutes: React.FC = () => {
  return (
    <NutritionProvider>
      <Routes>
        <Route path="/" element={<Navigate to="/nutrition/dashboard" replace />} />
        
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/foods" 
          element={
            <ProtectedRoute>
              <FoodItems />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/foods/new" 
          element={
            <ProtectedRoute>
              <AddEditFoodItem />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/foods/:id" 
          element={
            <ProtectedRoute>
              <FoodItemDetail />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/foods/:id/edit" 
          element={
            <ProtectedRoute>
              <AddEditFoodItem />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/usda-search" 
          element={
            <ProtectedRoute>
              <USDASearch />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/meals" 
          element={
            <ProtectedRoute>
              <Meals />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/meals/new" 
          element={
            <ProtectedRoute>
              <AddEditMeal />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/meals/:id" 
          element={
            <ProtectedRoute>
              <MealDetail />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/meals/:id/edit" 
          element={
            <ProtectedRoute>
              <AddEditMeal />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </NutritionProvider>
  );
};

export default NutritionRoutes;