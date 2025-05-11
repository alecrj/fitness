// Recipe API Service
import client from './client';
import { 
  Recipe, 
  RecipeListResponse, 
  RecipeSearchParams, 
  RecipeFormData, 
  RecipeImportRequest,
  RecipeImportResponse,
  RecipeNutritionAnalysisRequest,
  RecipeNutritionAnalysisResponse,
  RecipeSupportedSite
} from '../types/recipe';

const RECIPES_ENDPOINT = '/recipes';

/**
 * Recipe API Service
 * Provides methods to interact with the recipe endpoints
 */
export const recipeService = {
  /**
   * Get a list of recipes with pagination
   */
  getRecipes: async (limit = 10, offset = 0): Promise<RecipeListResponse> => {
    const response = await client.get(`${RECIPES_ENDPOINT}`, {
      params: { limit, offset }
    });
    return response.data;
  },

  /**
   * Get a specific recipe by ID
   */
  getRecipe: async (id: string): Promise<Recipe> => {
    const response = await client.get(`${RECIPES_ENDPOINT}/${id}`);
    return response.data;
  },

  /**
   * Create a new recipe
   */
  createRecipe: async (recipeData: RecipeFormData): Promise<Recipe> => {
    // Handle image upload if present
    const formData = new FormData();
    
    // Add recipe data as JSON
    const recipeJson = { ...recipeData };
    
    // Remove image from JSON if it exists
    if (recipeData.image) {
      delete recipeJson.image;
      formData.append('image', recipeData.image);
    }
    
    // Add recipe data as JSON string
    formData.append('recipe', JSON.stringify(recipeJson));
    
    const response = await client.post(RECIPES_ENDPOINT, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  },

  /**
   * Update an existing recipe
   */
  updateRecipe: async (id: string, recipeData: Partial<RecipeFormData>): Promise<Recipe> => {
    // Handle image upload if present
    const formData = new FormData();
    
    // Add recipe data as JSON
    const recipeJson = { ...recipeData };
    
    // Remove image from JSON if it exists
    if (recipeData.image) {
      delete recipeJson.image;
      formData.append('image', recipeData.image);
    }
    
    // Add recipe data as JSON string
    formData.append('recipe', JSON.stringify(recipeJson));
    
    const response = await client.put(`${RECIPES_ENDPOINT}/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  },

  /**
   * Delete a recipe
   */
  deleteRecipe: async (id: string): Promise<void> => {
    await client.delete(`${RECIPES_ENDPOINT}/${id}`);
  },

  /**
   * Search recipes with various filters
   */
  searchRecipes: async (params: RecipeSearchParams): Promise<RecipeListResponse> => {
    const response = await client.get(`${RECIPES_ENDPOINT}/search`, { params });
    return response.data;
  },

  /**
   * Import a recipe from a URL
   */
  importRecipe: async (importData: RecipeImportRequest): Promise<RecipeImportResponse> => {
    const response = await client.post(`${RECIPES_ENDPOINT}/import`, importData);
    return response.data;
  },

  /**
   * Share a recipe publicly
   */
  shareRecipe: async (id: string): Promise<{ isPublic: boolean }> => {
    const response = await client.post(`${RECIPES_ENDPOINT}/share/${id}`);
    return response.data;
  },

  /**
   * Make a recipe private
   */
  unshareRecipe: async (id: string): Promise<{ isPublic: boolean }> => {
    const response = await client.post(`${RECIPES_ENDPOINT}/unshare/${id}`);
    return response.data;
  },

  /**
   * Get list of supported recipe import sites
   */
  getSupportedSites: async (): Promise<RecipeSupportedSite[]> => {
    const response = await client.get(`${RECIPES_ENDPOINT}/supported-sites`);
    return response.data.sites;
  },

  /**
   * Analyze nutrition for a recipe
   */
  analyzeRecipeNutrition: async (
    data: RecipeNutritionAnalysisRequest
  ): Promise<RecipeNutritionAnalysisResponse> => {
    const response = await client.post(`${RECIPES_ENDPOINT}/nutritional-analysis`, data);
    return response.data;
  }
};

export default recipeService;