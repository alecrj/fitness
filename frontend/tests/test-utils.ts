// tests/test-utils.ts
import React from 'react';
import { render as rtlRender, RenderOptions } from '@testing-library/react';
import { ReactElement } from 'react';

// Mock Firebase objects
export const mockFirebaseUser = {
  uid: 'test-user-123',
  email: 'test@example.com',
  displayName: 'Test User'
};

// Mock food item data
export const mockFoodItems = [
  {
    id: 'food-1',
    userId: 'test-user-123',
    name: 'Apple',
    brand: '',
    serving_size: 100,
    serving_unit: 'g',
    is_custom: true,
    is_favorite: false,
    nutrition: {
      calories: 52,
      protein: 0.3,
      carbs: 14,
      fat: 0.2,
      fiber: 2.4,
      sugar: 10.3
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: 'food-2',
    userId: 'test-user-123',
    name: 'Chicken Breast',
    brand: '',
    serving_size: 85,
    serving_unit: 'g',
    is_custom: true,
    is_favorite: true,
    nutrition: {
      calories: 128,
      protein: 26.7,
      carbs: 0,
      fat: 2.8,
      fiber: 0,
      sugar: 0
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
];

// Mock meal data
export const mockMeals = [
  {
    id: 'meal-1',
    userId: 'test-user-123',
    name: 'Breakfast',
    meal_type: 'breakfast',
    meal_time: new Date().toISOString(),
    food_items: [
      {
        food_item_id: 'food-1',
        food_item_name: 'Apple',
        servings: 1,
        nutrition: {
          calories: 52,
          protein: 0.3,
          carbs: 14,
          fat: 0.2,
          fiber: 2.4,
          sugar: 10.3
        }
      }
    ],
    nutrition_totals: {
      calories: 52,
      protein: 0.3,
      carbs: 14,
      fat: 0.2,
      fiber: 2.4,
      sugar: 10.3
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
];

// Mock USDA search results
export const mockUsdaSearchResults = {
  foods: [
    {
      fdcId: 171689,
      description: 'Banana, raw',
      dataType: 'SR Legacy',
      foodNutrients: [
        { nutrientName: 'Energy', value: 89, unitName: 'KCAL' },
        { nutrientName: 'Protein', value: 1.09, unitName: 'G' },
        { nutrientName: 'Carbohydrates', value: 22.84, unitName: 'G' },
        { nutrientName: 'Total lipid (fat)', value: 0.33, unitName: 'G' }
      ],
      foodCategory: 'Fruits and Fruit Juices'
    }
  ],
  totalHits: 1
};

// Simple wrapper without router for now
const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return <div>{children}</div>;
};

// Custom render
const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => {
  return rtlRender(ui, { wrapper: TestWrapper, ...options });
};

// Re-export everything from testing-library
export * from '@testing-library/react';
export { customRender as render };