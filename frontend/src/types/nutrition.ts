/**
 * Type definitions for nutrition-related entities
 */

// Basic nutrition properties
export interface NutritionData {
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
    fiber?: number;
    sugar?: number;
    sodium?: number;
    cholesterol?: number;
  }
  
  // Food item from the database
  export interface FoodItem {
    id: string;
    userId: string;
    name: string;
    brand?: string;
    barcode?: string;
    fdcId?: string; // USDA Food Data Central ID (if imported)
    serving_size: number;
    serving_unit: string;
    nutrition: NutritionData;
    is_custom: boolean;
    is_favorite: boolean;
    created_at: string;
    updated_at: string;
  }
  
  // Food item with portion for inclusion in meals
  export interface MealFoodItem {
    food_item_id: string;
    food_item_name: string;
    servings: number;
    nutrition: NutritionData;
  }
  
  // Meal log
  export interface Meal {
    id: string;
    userId: string;
    name: string;
    meal_type: MealType;
    meal_time: string;
    food_items: MealFoodItem[];
    nutrition_totals: NutritionData;
    notes?: string;
    tags?: string[];
    created_at: string;
    updated_at: string;
  }
  
  // Meal type enum
  export enum MealType {
    BREAKFAST = 'breakfast',
    LUNCH = 'lunch',
    DINNER = 'dinner',
    SNACK = 'snack'
  }
  
  // Food item creation/update request
  export interface FoodItemRequest {
    name: string;
    brand?: string;
    barcode?: string;
    serving_size: number;
    serving_unit: string;
    nutrition: NutritionData;
    is_custom?: boolean;
    is_favorite?: boolean;
  }
  
  // Meal creation/update request
  export interface MealRequest {
    name: string;
    meal_type: MealType;
    meal_time: string;
    food_items: {
      food_item_id: string;
      servings: number;
    }[];
    notes?: string;
    tags?: string[];
  }
  
  // USDA API response types
  export interface USDAFoodSearchResult {
    fdcId: string;
    description: string;
    dataType: string;
    brandOwner?: string;
    ingredients?: string;
    foodCategory?: string;
    score?: number;
  }
  
  export interface USDASearchResponse {
    totalHits: number;
    currentPage: number;
    totalPages: number;
    foods: USDAFoodSearchResult[];
  }
  
  export interface USDAFoodDetail {
    fdcId: string;
    description: string;
    dataType: string;
    brandOwner?: string;
    ingredients?: string;
    foodCategory?: string;
    servingSize?: number;
    servingSizeUnit?: string;
    foodNutrients: {
      nutrientId: number;
      nutrientName: string;
      nutrientNumber: string;
      unitName: string;
      value: number;
    }[];
    // Other fields from USDA API
  }
  
  // USDA Food import request
  export interface USDAFoodImportRequest {
    fdcId: string;
    serving_size?: number;
    serving_unit?: string;
    is_favorite?: boolean;
  }
  
  // Nutrition statistics
  export interface NutritionStats {
    date: string;
    total: NutritionData;
    goal?: NutritionData;
    by_meal: {
      [key in MealType]?: {
        count: number;
        nutrition: NutritionData;
      };
    };
  }
  
  export interface WeeklyNutritionStats {
    start_date: string;
    end_date: string;
    daily_stats: {
      date: string;
      nutrition: NutritionData;
    }[];
    average: NutritionData;
    total: NutritionData;
  }
  
  // Pagination and query parameters
  export interface FoodItemsQueryParams {
    limit?: number;
    offset?: number;
    is_favorite?: boolean;
    is_custom?: boolean;
    q?: string;
  }
  
  export interface MealsQueryParams {
    limit?: number;
    offset?: number;
    date?: string;
    meal_type?: MealType;
  }
  
  // Pagination response
  export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    limit: number;
    offset: number;
  }