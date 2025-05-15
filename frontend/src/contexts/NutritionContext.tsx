import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { 
  FoodItem, 
  Meal, 
  FoodItemRequest, 
  MealRequest,
  FoodItemsQueryParams,
  MealsQueryParams,
  PaginatedResponse,
  NutritionStats,
  WeeklyNutritionStats,
  MealType,
  USDASearchResponse,
  USDAFoodDetail
} from '../types/nutrition';
import nutritionService from '../api/nutritionService';
import { useAuth } from './AuthContext';

interface NutritionContextType {
  // Food items
  foodItems: FoodItem[];
  totalFoodItems: number;
  foodItemsLoading: boolean;
  foodItemsError: string | null;
  fetchFoodItems: (params?: FoodItemsQueryParams) => Promise<void>;
  getFoodItem: (id: string) => Promise<FoodItem | undefined>;
  createFoodItem: (foodItem: FoodItemRequest) => Promise<FoodItem | undefined>;
  updateFoodItem: (id: string, foodItem: Partial<FoodItemRequest>) => Promise<FoodItem | undefined>;
  deleteFoodItem: (id: string) => Promise<boolean>;
  toggleFavorite: (id: string) => Promise<boolean>;
  
  // USDA search
  usdaSearchResults: USDASearchResponse | null;
  usdaSearchLoading: boolean;
  usdaSearchError: string | null;
  searchUSDAFoods: (query: string) => Promise<void>;
  getUSDAFoodDetails: (fdcId: string) => Promise<USDAFoodDetail | undefined>;
  importUSDAFood: (fdcId: string, servingSize?: number, servingUnit?: string) => Promise<FoodItem | undefined>;
  
  // Meals
  meals: Meal[];
  totalMeals: number;
  mealsLoading: boolean;
  mealsError: string | null;
  fetchMeals: (params?: MealsQueryParams) => Promise<void>;
  getMeal: (id: string) => Promise<Meal | undefined>;
  createMeal: (meal: MealRequest) => Promise<Meal | undefined>;
  updateMeal: (id: string, meal: Partial<MealRequest>) => Promise<Meal | undefined>;
  deleteMeal: (id: string) => Promise<boolean>;
  
  // Nutrition stats
  dailyStats: NutritionStats | null;
  weeklyStats: WeeklyNutritionStats | null;
  statsLoading: boolean;
  statsError: string | null;
  fetchDailyStats: (date?: string) => Promise<void>;
  fetchWeeklyStats: (startDate: string, endDate: string) => Promise<void>;
  
  // Barcode
  lookupBarcode: (code: string) => Promise<FoodItem | undefined>;
}

const NutritionContext = createContext<NutritionContextType | undefined>(undefined);

export const useNutrition = (): NutritionContextType => {
  const context = useContext(NutritionContext);
  if (!context) {
    throw new Error('useNutrition must be used within a NutritionProvider');
  }
  return context;
};

interface NutritionProviderProps {
  children: ReactNode;
}

export const NutritionProvider: React.FC<NutritionProviderProps> = ({ children }) => {
  const { currentUser } = useAuth();

  // Food items state
  const [foodItems, setFoodItems] = useState<FoodItem[]>([]);
  const [totalFoodItems, setTotalFoodItems] = useState<number>(0);
  const [foodItemsLoading, setFoodItemsLoading] = useState<boolean>(false);
  const [foodItemsError, setFoodItemsError] = useState<string | null>(null);

  // USDA search state
  const [usdaSearchResults, setUsdaSearchResults] = useState<USDASearchResponse | null>(null);
  const [usdaSearchLoading, setUsdaSearchLoading] = useState<boolean>(false);
  const [usdaSearchError, setUsdaSearchError] = useState<string | null>(null);

  // Meals state
  const [meals, setMeals] = useState<Meal[]>([]);
  const [totalMeals, setTotalMeals] = useState<number>(0);
  const [mealsLoading, setMealsLoading] = useState<boolean>(false);
  const [mealsError, setMealsError] = useState<string | null>(null);

  // Nutrition stats state
  const [dailyStats, setDailyStats] = useState<NutritionStats | null>(null);
  const [weeklyStats, setWeeklyStats] = useState<WeeklyNutritionStats | null>(null);
  const [statsLoading, setStatsLoading] = useState<boolean>(false);
  const [statsError, setStatsError] = useState<string | null>(null);

  // Food items methods
  const fetchFoodItems = async (params?: FoodItemsQueryParams) => {
    if (!currentUser) return;
    
    setFoodItemsLoading(true);
    setFoodItemsError(null);
    
    try {
      const response = await nutritionService.getFoodItems(params);
      setFoodItems(response.items);
      setTotalFoodItems(response.total);
    } catch (error) {
      console.error('Error fetching food items:', error);
      setFoodItemsError('Failed to fetch food items. Please try again later.');
    } finally {
      setFoodItemsLoading(false);
    }
  };

  const getFoodItem = async (id: string): Promise<FoodItem | undefined> => {
    if (!currentUser) return undefined;
    
    try {
      return await nutritionService.getFoodItem(id);
    } catch (error) {
      console.error(`Error fetching food item ${id}:`, error);
      return undefined;
    }
  };

  const createFoodItem = async (foodItem: FoodItemRequest): Promise<FoodItem | undefined> => {
    if (!currentUser) return undefined;
    
    try {
      const newFoodItem = await nutritionService.createFoodItem(foodItem);
      setFoodItems(prev => [newFoodItem, ...prev]);
      setTotalFoodItems(prev => prev + 1);
      return newFoodItem;
    } catch (error) {
      console.error('Error creating food item:', error);
      return undefined;
    }
  };

  const updateFoodItem = async (id: string, foodItem: Partial<FoodItemRequest>): Promise<FoodItem | undefined> => {
    if (!currentUser) return undefined;
    
    try {
      const updatedFoodItem = await nutritionService.updateFoodItem(id, foodItem);
      setFoodItems(prev => prev.map(item => item.id === id ? updatedFoodItem : item));
      return updatedFoodItem;
    } catch (error) {
      console.error(`Error updating food item ${id}:`, error);
      return undefined;
    }
  };

  const deleteFoodItem = async (id: string): Promise<boolean> => {
    if (!currentUser) return false;
    
    try {
      await nutritionService.deleteFoodItem(id);
      setFoodItems(prev => prev.filter(item => item.id !== id));
      setTotalFoodItems(prev => prev - 1);
      return true;
    } catch (error) {
      console.error(`Error deleting food item ${id}:`, error);
      return false;
    }
  };

  const toggleFavorite = async (id: string): Promise<boolean> => {
    if (!currentUser) return false;
    
    try {
      const result = await nutritionService.toggleFavorite(id);
      setFoodItems(prev => prev.map(item => {
        if (item.id === id) {
          return { ...item, is_favorite: result.is_favorite };
        }
        return item;
      }));
      return true;
    } catch (error) {
      console.error(`Error toggling favorite status for food item ${id}:`, error);
      return false;
    }
  };

  // USDA search methods
  const searchUSDAFoods = async (query: string): Promise<void> => {
    if (!currentUser || !query.trim()) return;
    
    setUsdaSearchLoading(true);
    setUsdaSearchError(null);
    
    try {
      const results = await nutritionService.searchUSDAFoods(query);
      setUsdaSearchResults(results);
    } catch (error) {
      console.error('Error searching USDA foods:', error);
      setUsdaSearchError('Failed to search USDA database. Please try again later.');
    } finally {
      setUsdaSearchLoading(false);
    }
  };

  const getUSDAFoodDetails = async (fdcId: string): Promise<USDAFoodDetail | undefined> => {
    if (!currentUser) return undefined;
    
    try {
      return await nutritionService.getUSDAFoodDetails(fdcId);
    } catch (error) {
      console.error(`Error fetching USDA food details for ${fdcId}:`, error);
      return undefined;
    }
  };

  const importUSDAFood = async (
    fdcId: string, 
    servingSize?: number, 
    servingUnit?: string
  ): Promise<FoodItem | undefined> => {
    if (!currentUser) return undefined;
    
    try {
      const importRequest = {
        fdcId,
        ...(servingSize ? { serving_size: servingSize } : {}),
        ...(servingUnit ? { serving_unit: servingUnit } : {})
      };
      
      const importedFood = await nutritionService.importUSDAFood(importRequest);
      setFoodItems(prev => [importedFood, ...prev]);
      setTotalFoodItems(prev => prev + 1);
      return importedFood;
    } catch (error) {
      console.error(`Error importing USDA food ${fdcId}:`, error);
      return undefined;
    }
  };

  // Meals methods
  const fetchMeals = async (params?: MealsQueryParams): Promise<void> => {
    if (!currentUser) return;
    
    setMealsLoading(true);
    setMealsError(null);
    
    try {
      const response = await nutritionService.getMeals(params);
      setMeals(response.items);
      setTotalMeals(response.total);
    } catch (error) {
      console.error('Error fetching meals:', error);
      setMealsError('Failed to fetch meals. Please try again later.');
    } finally {
      setMealsLoading(false);
    }
  };

  const getMeal = async (id: string): Promise<Meal | undefined> => {
    if (!currentUser) return undefined;
    
    try {
      return await nutritionService.getMeal(id);
    } catch (error) {
      console.error(`Error fetching meal ${id}:`, error);
      return undefined;
    }
  };

  const createMeal = async (meal: MealRequest): Promise<Meal | undefined> => {
    if (!currentUser) return undefined;
    
    try {
      const newMeal = await nutritionService.createMeal(meal);
      setMeals(prev => [newMeal, ...prev]);
      setTotalMeals(prev => prev + 1);
      return newMeal;
    } catch (error) {
      console.error('Error creating meal:', error);
      return undefined;
    }
  };

  const updateMeal = async (id: string, meal: Partial<MealRequest>): Promise<Meal | undefined> => {
    if (!currentUser) return undefined;
    
    try {
      const updatedMeal = await nutritionService.updateMeal(id, meal);
      setMeals(prev => prev.map(item => item.id === id ? updatedMeal : item));
      return updatedMeal;
    } catch (error) {
      console.error(`Error updating meal ${id}:`, error);
      return undefined;
    }
  };

  const deleteMeal = async (id: string): Promise<boolean> => {
    if (!currentUser) return false;
    
    try {
      await nutritionService.deleteMeal(id);
      setMeals(prev => prev.filter(meal => meal.id !== id));
      setTotalMeals(prev => prev - 1);
      return true;
    } catch (error) {
      console.error(`Error deleting meal ${id}:`, error);
      return false;
    }
  };

  // Nutrition stats methods
  const fetchDailyStats = async (date?: string): Promise<void> => {
    if (!currentUser) return;
    
    setStatsLoading(true);
    setStatsError(null);
    
    try {
      const stats = await nutritionService.getDailyStats(date);
      setDailyStats(stats);
    } catch (error) {
      console.error('Error fetching daily nutrition stats:', error);
      setStatsError('Failed to fetch daily nutrition statistics. Please try again later.');
    } finally {
      setStatsLoading(false);
    }
  };

  const fetchWeeklyStats = async (startDate: string, endDate: string): Promise<void> => {
    if (!currentUser) return;
    
    setStatsLoading(true);
    setStatsError(null);
    
    try {
      const stats = await nutritionService.getWeeklyStats(startDate, endDate);
      setWeeklyStats(stats);
    } catch (error) {
      console.error('Error fetching weekly nutrition stats:', error);
      setStatsError('Failed to fetch weekly nutrition statistics. Please try again later.');
    } finally {
      setStatsLoading(false);
    }
  };

  // Barcode lookup method
  const lookupBarcode = async (code: string): Promise<FoodItem | undefined> => {
    if (!currentUser) return undefined;
    
    try {
      return await nutritionService.lookupBarcode(code);
    } catch (error) {
      console.error(`Error looking up barcode ${code}:`, error);
      return undefined;
    }
  };

  useEffect(() => {
    // Clear state when user logs out
    if (!currentUser) {
      setFoodItems([]);
      setTotalFoodItems(0);
      setMeals([]);
      setTotalMeals(0);
      setDailyStats(null);
      setWeeklyStats(null);
      setUsdaSearchResults(null);
    }
  }, [currentUser]);

  const value = {
    // Food items
    foodItems,
    totalFoodItems,
    foodItemsLoading,
    foodItemsError,
    fetchFoodItems,
    getFoodItem,
    createFoodItem,
    updateFoodItem,
    deleteFoodItem,
    toggleFavorite,
    
    // USDA search
    usdaSearchResults,
    usdaSearchLoading,
    usdaSearchError,
    searchUSDAFoods,
    getUSDAFoodDetails,
    importUSDAFood,
    
    // Meals
    meals,
    totalMeals,
    mealsLoading,
    mealsError,
    fetchMeals,
    getMeal,
    createMeal,
    updateMeal,
    deleteMeal,
    
    // Nutrition stats
    dailyStats,
    weeklyStats,
    statsLoading,
    statsError,
    fetchDailyStats,
    fetchWeeklyStats,
    
    // Barcode
    lookupBarcode,
  };

  return (
    <NutritionContext.Provider value={value}>
      {children}
    </NutritionContext.Provider>
  );
};