import React from 'react';
import { render as rtlRender, RenderOptions } from '@testing-library/react';

// Firebase Auth User Interface
interface MockUser {
  uid: string;
  email: string;
  displayName: string;
  emailVerified: boolean;
}

// Firebase Auth Interface
interface MockFirebaseAuth {
  currentUser: MockUser | null;
  signInWithEmailAndPassword: jest.Mock;
  createUserWithEmailAndPassword: jest.Mock;
  signOut: jest.Mock;
  sendPasswordResetEmail: jest.Mock;
  onAuthStateChanged: jest.Mock;
}

// Mock Firebase Auth with proper types
export const mockFirebaseAuth: MockFirebaseAuth = {
  currentUser: {
    uid: 'test-user-id',
    email: 'test@example.com',
    displayName: 'Test User',
    emailVerified: true,
  },
  signInWithEmailAndPassword: jest.fn(() => Promise.resolve({ user: mockFirebaseAuth.currentUser })),
  createUserWithEmailAndPassword: jest.fn(() => Promise.resolve({ user: mockFirebaseAuth.currentUser })),
  signOut: jest.fn(() => Promise.resolve()),
  sendPasswordResetEmail: jest.fn(() => Promise.resolve()),
  onAuthStateChanged: jest.fn((callback: (user: MockUser | null) => void) => {
    callback(mockFirebaseAuth.currentUser);
    return () => {};
  }),
};

// Mock Firebase Firestore with proper types
export const mockFirestore = {
  collection: jest.fn(() => ({
    doc: jest.fn(() => ({
      get: jest.fn(() => Promise.resolve({
        exists: true,
        data: () => ({}),
      })),
      set: jest.fn(() => Promise.resolve()),
      update: jest.fn(() => Promise.resolve()),
      delete: jest.fn(() => Promise.resolve()),
    })),
    add: jest.fn(() => Promise.resolve({ id: 'mock-doc-id' })),
    where: jest.fn(() => ({
      get: jest.fn(() => Promise.resolve({
        docs: [],
        forEach: jest.fn(),
      })),
    })),
    orderBy: jest.fn(() => ({
      limit: jest.fn(() => ({
        get: jest.fn(() => Promise.resolve({
          docs: [],
          forEach: jest.fn(),
        })),
      })),
    })),
  })),
};

// Mock Firebase Storage
export const mockStorage = {
  ref: jest.fn(() => ({
    child: jest.fn(() => ({
      put: jest.fn(() => Promise.resolve({
        ref: {
          getDownloadURL: jest.fn(() => Promise.resolve('https://example.com/image.jpg')),
        },
      })),
    })),
  })),
};

// Auth Context Type
interface MockAuthContext {
  user: MockUser | null;
  loading: boolean;
  error: string | null;
  login: jest.Mock;
  register: jest.Mock;
  logout: jest.Mock;
  updateProfile: jest.Mock;
  resetPassword: jest.Mock;
}

// Mock Context Providers with proper types
export const mockAuthContext: MockAuthContext = {
  user: mockFirebaseAuth.currentUser,
  loading: false,
  error: null,
  login: jest.fn(),
  register: jest.fn(),
  logout: jest.fn(),
  updateProfile: jest.fn(),
  resetPassword: jest.fn(),
};

// Nutrition types - FIXED to use string dates
interface MockNutrition {
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fiber?: number;
  sugar?: number;
  sodium?: number;
  cholesterol?: number;
}

interface MockFoodItem {
  id: string;
  userId: string;
  name: string;
  brand: string | undefined;
  barcode: string | undefined;
  fdcId: string | undefined;
  serving_size: number;
  serving_unit: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  nutrition: MockNutrition;
  is_custom: boolean;
  is_favorite: boolean;
  created_at: string; // ACTUALLY CHANGED: Now string instead of Date
  updated_at: string; // ACTUALLY CHANGED: Now string instead of Date
}

interface MockMeal {
  id: string;
  userId: string;
  name: string;
  meal_type: string;
  meal_time: Date;
  food_items: Array<{
    food_item_id: string;
    food_item_name: string;
    servings: number;
    nutrition: MockNutrition;
  }>;
  nutrition_totals: MockNutrition;
  notes?: string;
  tags?: string[];
  created_at: string; // ACTUALLY CHANGED: Now string instead of Date
  updated_at: string; // ACTUALLY CHANGED: Now string instead of Date
}

export const mockNutritionContext = {
  foods: [] as MockFoodItem[],
  meals: [] as MockMeal[],
  loading: false,
  error: null,
  addFood: jest.fn(),
  updateFood: jest.fn(),
  deleteFood: jest.fn(),
  getFoods: jest.fn(),
  searchUSDAFoods: jest.fn(),
  importUSDAFood: jest.fn(),
  addMeal: jest.fn(),
  updateMeal: jest.fn(),
  deleteMeal: jest.fn(),
  getMeals: jest.fn(),
  getDailyStats: jest.fn(),
  getWeeklyStats: jest.fn(),
};

export const mockRecipeContext = {
  recipes: [],
  loading: false,
  error: null,
  addRecipe: jest.fn(),
  updateRecipe: jest.fn(),
  deleteRecipe: jest.fn(),
  getRecipes: jest.fn(),
  getRecipe: jest.fn(),
  searchRecipes: jest.fn(),
  importRecipe: jest.fn(),
  shareRecipe: jest.fn(),
  unshareRecipe: jest.fn(),
};

// Mock Food Items with proper types - ACTUALLY CHANGED: Use string dates
export const mockFoodItems: MockFoodItem[] = [
  {
    id: 'food-1',
    userId: 'test-user-id',
    name: 'Apple',
    brand: undefined,
    barcode: undefined,
    fdcId: '123456',
    serving_size: 100,
    serving_unit: 'g',
    calories: 52,
    protein: 0.3,
    carbs: 14,
    fat: 0.2,
    nutrition: {
      calories: 52,
      protein: 0.3,
      carbs: 14,
      fat: 0.2,
      fiber: 2.4,
      sugar: 10.4,
      sodium: 1,
      cholesterol: 0,
    },
    is_custom: false,
    is_favorite: false,
    created_at: '2024-05-12T10:30:00Z', // ACTUALLY CHANGED: String instead of new Date()
    updated_at: '2024-05-12T10:30:00Z', // ACTUALLY CHANGED: String instead of new Date()
  },
  {
    id: 'food-2',
    userId: 'test-user-id',
    name: 'Banana',
    brand: undefined,
    barcode: undefined,
    fdcId: '123457',
    serving_size: 100,
    serving_unit: 'g',
    calories: 89,
    protein: 1.1,
    carbs: 23,
    fat: 0.3,
    nutrition: {
      calories: 89,
      protein: 1.1,
      carbs: 23,
      fat: 0.3,
      fiber: 2.6,
      sugar: 12.2,
      sodium: 1,
      cholesterol: 0,
    },
    is_custom: false,
    is_favorite: true,
    created_at: '2024-05-12T10:30:00Z', // ACTUALLY CHANGED: String instead of new Date()
    updated_at: '2024-05-12T10:30:00Z', // ACTUALLY CHANGED: String instead of new Date()
  },
];

// Mock Meals with proper types - ACTUALLY CHANGED: Use string dates
export const mockMeals: MockMeal[] = [
  {
    id: 'meal-1',
    userId: 'test-user-id',
    name: 'Breakfast',
    meal_type: 'breakfast',
    meal_time: new Date(),
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
          sugar: 10.4,
          sodium: 1,
          cholesterol: 0,
        },
      },
    ],
    nutrition_totals: {
      calories: 52,
      protein: 0.3,
      carbs: 14,
      fat: 0.2,
      fiber: 2.4,
      sugar: 10.4,
      sodium: 1,
      cholesterol: 0,
    },
    notes: 'Morning snack',
    tags: ['healthy', 'fruit'],
    created_at: '2024-05-12T10:30:00Z', // ACTUALLY CHANGED: String instead of new Date()
    updated_at: '2024-05-12T10:30:00Z', // ACTUALLY CHANGED: String instead of new Date()
  },
  {
    id: 'meal-2',
    userId: 'test-user-id',
    name: 'Lunch',
    meal_type: 'lunch',
    meal_time: new Date(),
    food_items: [
      {
        food_item_id: 'food-2',
        food_item_name: 'Banana',
        servings: 1,
        nutrition: {
          calories: 89,
          protein: 1.1,
          carbs: 23,
          fat: 0.3,
          fiber: 2.6,
          sugar: 12.2,
          sodium: 1,
          cholesterol: 0,
        },
      },
    ],
    nutrition_totals: {
      calories: 89,
      protein: 1.1,
      carbs: 23,
      fat: 0.3,
      fiber: 2.6,
      sugar: 12.2,
      sodium: 1,
      cholesterol: 0,
    },
    notes: 'Quick lunch',
    tags: ['quick'],
    created_at: '2024-05-12T10:30:00Z', // ACTUALLY CHANGED: String instead of new Date()
    updated_at: '2024-05-12T10:30:00Z', // ACTUALLY CHANGED: String instead of new Date()
  },
];

// USDA Search Results interface
interface USDAFood {
  fdcId: number;
  description: string;
  foodCategory: string;
}

interface MockUSDASearchResults {
  foods: USDAFood[];
  totalHits: number;
}

// Mock USDA Search Results
export const mockUSDASearchResults: MockUSDASearchResults = {
  foods: [
    {
      fdcId: 123456,
      description: 'Apple, raw',
      foodCategory: 'Fruits and Fruit Juices',
    },
    {
      fdcId: 123457,
      description: 'Banana, raw',
      foodCategory: 'Fruits and Fruit Juices',
    },
  ],
  totalHits: 2,
};

// Split mock USDA data for test functions
export const splitMockUsda3 = (): MockUSDASearchResults => ({
  foods: mockUSDASearchResults.foods.slice(0, 1),
  totalHits: 1,
});

// No wrapper approach - render directly
export const customRender = (ui: React.ReactElement, options?: RenderOptions) => {
  return rtlRender(ui, options);
};

// Export everything from RTL
export * from '@testing-library/react';

// Override render method
export { customRender as render };
// At the very bottom of your test-utils.ts file, add this line:

// Export with alternative name to fix import issues
export const mockUsDASearchResults = mockUSDASearchResults;