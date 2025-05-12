// tests/__mocks__/nutritionService.ts
import { mockFoodItems, mockMeals, mockUSDASearchResults } from '../test-utils';

export const getFoodItems = jest.fn().mockResolvedValue({ 
  data: { items: mockFoodItems, total: mockFoodItems.length } 
});

export const getFoodItem = jest.fn().mockImplementation((id: string) => 
  Promise.resolve({ data: mockFoodItems.find(item => item.id === id) || mockFoodItems[0] })
);

export const createFoodItem = jest.fn().mockImplementation((data: any) => 
  Promise.resolve({ data: { ...data, id: 'new-food-id' } })
);

export const updateFoodItem = jest.fn().mockImplementation((id: string, data: any) => 
  Promise.resolve({ data: { ...data, id } })
);

export const deleteFoodItem = jest.fn().mockResolvedValue({ data: { success: true } });

export const toggleFavorite = jest.fn().mockImplementation((id: string) => 
  Promise.resolve({ data: { success: true, is_favorite: true } })
);

export const searchUsda = jest.fn().mockResolvedValue({ data: mockUSDASearchResults });

export const getUsdaDetails = jest.fn().mockResolvedValue({ data: mockUSDASearchResults.foods[0] });

export const importUsdaFood = jest.fn().mockResolvedValue({ data: mockFoodItems[0] });

export const getMeals = jest.fn().mockResolvedValue({ 
  data: { items: mockMeals, total: mockMeals.length } 
});

export const getMeal = jest.fn().mockImplementation((id: string) => 
  Promise.resolve({ data: mockMeals.find(meal => meal.id === id) || mockMeals[0] })
);

export const createMeal = jest.fn().mockImplementation((data: any) => 
  Promise.resolve({ data: { ...data, id: 'new-meal-id' } })
);

export const updateMeal = jest.fn().mockImplementation((id: string, data: any) => 
  Promise.resolve({ data: { ...data, id } })
);

export const deleteMeal = jest.fn().mockResolvedValue({ data: { success: true } });

export const getDailyStats = jest.fn().mockResolvedValue({
  data: {
    date: new Date().toISOString().split('T')[0],
    meals: mockMeals,
    nutrition_totals: {
      calories: 52,
      protein: 0.3,
      carbs: 14,
      fat: 0.2
    },
    meal_count: 1
  }
});

export const getWeeklyStats = jest.fn().mockResolvedValue({
  data: {
    start_date: '2025-05-05',
    end_date: '2025-05-11',
    daily_stats: [
      {
        date: '2025-05-05',
        nutrition_totals: { calories: 52, protein: 0.3, carbs: 14, fat: 0.2 },
        meal_count: 1
      }
    ],
    nutrition_averages: { calories: 52, protein: 0.3, carbs: 14, fat: 0.2 }
  }
});

export const lookupBarcode = jest.fn().mockResolvedValue({ data: mockFoodItems[0] });