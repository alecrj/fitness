import api from './client';
import {
  FoodItem,
  FoodItemRequest,
  Meal,
  MealRequest,
  FoodItemsQueryParams,
  MealsQueryParams,
  PaginatedResponse,
  USDASearchResponse,
  USDAFoodDetail,
  USDAFoodImportRequest,
  NutritionStats,
  WeeklyNutritionStats,
} from '../types/nutrition';

const BASE_URL = '/api/nutrition';

/**
 * Service for interacting with nutrition-related API endpoints
 */
const nutritionService = {
  // Food item endpoints
  getFoodItems: async (params?: FoodItemsQueryParams): Promise<PaginatedResponse<FoodItem>> => {
    const response = await api.get(`${BASE_URL}/foods`, { params });
    return response.data;
  },

  getFoodItem: async (id: string): Promise<FoodItem> => {
    const response = await api.get(`${BASE_URL}/foods/${id}`);
    return response.data;
  },

  createFoodItem: async (foodItem: FoodItemRequest): Promise<FoodItem> => {
    const response = await api.post(`${BASE_URL}/foods`, foodItem);
    return response.data;
  },

  updateFoodItem: async (id: string, foodItem: Partial<FoodItemRequest>): Promise<FoodItem> => {
    const response = await api.put(`${BASE_URL}/foods/${id}`, foodItem);
    return response.data;
  },

  deleteFoodItem: async (id: string): Promise<void> => {
    await api.delete(`${BASE_URL}/foods/${id}`);
  },

  toggleFavorite: async (id: string): Promise<{ is_favorite: boolean }> => {
    const response = await api.post(`${BASE_URL}/foods/${id}/favorite`);
    return response.data;
  },

  // USDA food search and import
  searchUSDAFoods: async (query: string): Promise<USDASearchResponse> => {
    const response = await api.get(`${BASE_URL}/foods/search`, { params: { q: query } });
    return response.data;
  },

  getUSDAFoodDetails: async (fdcId: string): Promise<USDAFoodDetail> => {
    const response = await api.get(`${BASE_URL}/foods/details/${fdcId}`);
    return response.data;
  },

  importUSDAFood: async (importRequest: USDAFoodImportRequest): Promise<FoodItem> => {
    const response = await api.post(`${BASE_URL}/foods/import`, importRequest);
    return response.data;
  },

  // Meal logging endpoints
  getMeals: async (params?: MealsQueryParams): Promise<PaginatedResponse<Meal>> => {
    const response = await api.get(`${BASE_URL}/meals`, { params });
    return response.data;
  },

  getMeal: async (id: string): Promise<Meal> => {
    const response = await api.get(`${BASE_URL}/meals/${id}`);
    return response.data;
  },

  createMeal: async (meal: MealRequest): Promise<Meal> => {
    const response = await api.post(`${BASE_URL}/meals`, meal);
    return response.data;
  },

  updateMeal: async (id: string, meal: Partial<MealRequest>): Promise<Meal> => {
    const response = await api.put(`${BASE_URL}/meals/${id}`, meal);
    return response.data;
  },

  deleteMeal: async (id: string): Promise<void> => {
    await api.delete(`${BASE_URL}/meals/${id}`);
  },

  // Nutrition statistics endpoints
  getDailyStats: async (date?: string): Promise<NutritionStats> => {
    const response = await api.get(`${BASE_URL}/stats/daily`, { 
      params: date ? { date } : undefined 
    });
    return response.data;
  },

  getWeeklyStats: async (startDate: string, endDate: string): Promise<WeeklyNutritionStats> => {
    const response = await api.get(`${BASE_URL}/stats/weekly`, { 
      params: { start_date: startDate, end_date: endDate } 
    });
    return response.data;
  },

  // Barcode lookup
  lookupBarcode: async (code: string): Promise<FoodItem> => {
    const response = await api.get(`${BASE_URL}/barcode/lookup`, { params: { code } });
    return response.data;
  }
};

export default nutritionService;