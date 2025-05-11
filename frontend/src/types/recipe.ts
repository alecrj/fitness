// Recipe Type Definitions
export type RecipeNutrition = {
    calories?: number;
    protein?: number;
    carbs?: number;
    fat?: number;
    fiber?: number;
    sugar?: number;
  };
  
  export type RecipeDifficulty = 'easy' | 'medium' | 'hard' | 'expert';
  
  export type RecipeSource = 'user' | 'web' | 'instagram';
  
  export interface Recipe {
    id: string;
    userId: string;
    title: string;
    description?: string;
    ingredients: string[];
    instructions: string[];
    prepTime?: number;
    cookTime?: number;
    servings?: number;
    difficulty?: RecipeDifficulty;
    cuisine?: string;
    imageUrl?: string;
    imageStoragePath?: string;
    tags?: string[];
    createdAt: Date | string | number;
    updatedAt: Date | string | number;
    isPublic: boolean;
    source: RecipeSource;
    sourceUrl?: string;
    nutrition?: RecipeNutrition;
    needsReview?: boolean;
  }
  
  // Form data interfaces for creating/updating recipes
  export interface RecipeFormData {
    title: string;
    description?: string;
    ingredients: string[];
    instructions: string[];
    prepTime?: number;
    cookTime?: number;
    servings?: number;
    difficulty?: RecipeDifficulty;
    cuisine?: string;
    image?: File;
    tags?: string[];
    isPublic?: boolean;
  }
  
  // Recipe request/response interfaces
  export interface RecipeListResponse {
    recipes: Recipe[];
    total: number;
    page: number;
    limit: number;
    totalPages: number;
  }
  
  export interface RecipeSearchParams {
    q?: string;
    tags?: string[];
    cuisine?: string;
    difficulty?: RecipeDifficulty;
    includePublic?: boolean;
    limit?: number;
    offset?: number;
  }
  
  export interface RecipeImportRequest {
    url: string;
  }
  
  export interface RecipeImportResponse {
    recipe: Recipe;
    taskId?: string;
  }
  
  export interface RecipeSupportedSite {
    name: string;
    domain: string;
    icon?: string;
  }
  
  export interface RecipeNutritionAnalysisRequest {
    ingredients: string[];
    servings?: number;
  }
  
  export interface RecipeNutritionAnalysisResponse {
    nutrition: RecipeNutrition;
    servings: number;
    ingredients: {
      original: string;
      parsed: string;
      nutrition?: RecipeNutrition;
    }[];
  }