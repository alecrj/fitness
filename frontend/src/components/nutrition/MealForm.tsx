import React, { useState, useEffect } from 'react';
import { Meal, MealRequest, MealType, FoodItem, MealFoodItem } from '../../types/nutrition';
import { useNutrition } from '../../contexts/NutritionContext';
import FoodItemCard from './FoodItemCard';

interface MealFormProps {
  initialData?: Meal;
  onSubmit: (meal: MealRequest) => void;
  onCancel: () => void;
  isSubmitting: boolean;
}

const MealForm: React.FC<MealFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
  isSubmitting
}) => {
  const { fetchFoodItems, foodItems, foodItemsLoading } = useNutrition();
  
  const [name, setName] = useState('');
  const [mealType, setMealType] = useState<MealType>(MealType.BREAKFAST);
  const [mealTime, setMealTime] = useState('');
  const [notes, setNotes] = useState('');
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState('');
  
  const [selectedFoodItems, setSelectedFoodItems] = useState<{ 
    foodItem: FoodItem; 
    servings: number;
  }[]>([]);
  
  const [searchQuery, setSearchQuery] = useState('');
  const [showFoodSelector, setShowFoodSelector] = useState(false);

  // Set default meal time to current time
  useEffect(() => {
    const now = new Date();
    const localISOTime = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
      .toISOString()
      .slice(0, 16);
    setMealTime(localISOTime);
  }, []);

  // Load initial data if editing an existing meal
  useEffect(() => {
    if (initialData) {
      setName(initialData.name);
      setMealType(initialData.meal_type);
      setMealTime(initialData.meal_time.slice(0, 16));
      setNotes(initialData.notes || '');
      setTags(initialData.tags || []);
      
      // We need to fetch the full food items based on the IDs in the meal
      const loadFoodItems = async () => {
        const items = await Promise.all(
          initialData.food_items.map(async (item) => {
            try {
              const foodItem = await useNutrition().getFoodItem(item.food_item_id);
              if (foodItem) {
                return {
                  foodItem,
                  servings: item.servings
                };
              }
              return null;
            } catch (error) {
              console.error(`Error fetching food item ${item.food_item_id}:`, error);
              return null;
            }
          })
        );
        
        setSelectedFoodItems(items.filter(Boolean) as { foodItem: FoodItem; servings: number }[]);
      };
      
      loadFoodItems();
    }
  }, [initialData]);

  // Load food items when search query changes
  useEffect(() => {
    const loadFoodItems = async () => {
      const queryParams = searchQuery ? { q: searchQuery } : undefined;
      await fetchFoodItems(queryParams);
    };
    
    loadFoodItems();
  }, [searchQuery, fetchFoodItems]);

  const handleAddTag = () => {
    if (tagInput.trim() && !tags.includes(tagInput.trim())) {
      setTags([...tags, tagInput.trim()]);
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleFoodItemSelect = (foodItem: FoodItem) => {
    const existing = selectedFoodItems.find(item => item.foodItem.id === foodItem.id);
    
    if (existing) {
      // If already selected, increase serving
      setSelectedFoodItems(
        selectedFoodItems.map(item => 
          item.foodItem.id === foodItem.id 
            ? { ...item, servings: item.servings + 1 }
            : item
        )
      );
    } else {
      // Add new food item with 1 serving
      setSelectedFoodItems([...selectedFoodItems, { foodItem, servings: 1 }]);
    }
    
    setShowFoodSelector(false);
  };

  const handleRemoveFoodItem = (foodItemId: string) => {
    setSelectedFoodItems(selectedFoodItems.filter(item => item.foodItem.id !== foodItemId));
  };

  const handleServingChange = (foodItemId: string, servings: number) => {
    setSelectedFoodItems(
      selectedFoodItems.map(item => 
        item.foodItem.id === foodItemId 
          ? { ...item, servings: servings }
          : item
      )
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const mealData: MealRequest = {
      name,
      meal_type: mealType,
      meal_time: new Date(mealTime).toISOString(),
      food_items: selectedFoodItems.map(item => ({
        food_item_id: item.foodItem.id,
        servings: item.servings
      })),
      notes: notes || undefined,
      tags: tags.length > 0 ? tags : undefined
    };
    
    onSubmit(mealData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Meal Name*
        </label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          placeholder="e.g., Breakfast, Lunch, Post-Workout Snack"
          required
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="mealType" className="block text-sm font-medium text-gray-700">
            Meal Type*
          </label>
          <select
            id="mealType"
            value={mealType}
            onChange={(e) => setMealType(e.target.value as MealType)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            required
          >
            <option value={MealType.BREAKFAST}>Breakfast</option>
            <option value={MealType.LUNCH}>Lunch</option>
            <option value={MealType.DINNER}>Dinner</option>
            <option value={MealType.SNACK}>Snack</option>
          </select>
        </div>
        <div>
          <label htmlFor="mealTime" className="block text-sm font-medium text-gray-700">
            Date & Time*
          </label>
          <input
            type="datetime-local"
            id="mealTime"
            value={mealTime}
            onChange={(e) => setMealTime(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            required
          />
        </div>
      </div>

      <div className="border-t border-gray-200 pt-4">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-lg font-medium leading-6 text-gray-900">Food Items</h3>
          <button
            type="button"
            onClick={() => setShowFoodSelector(!showFoodSelector)}
            className="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            {showFoodSelector ? 'Hide Foods' : 'Add Foods'}
          </button>
        </div>

        {selectedFoodItems.length === 0 ? (
          <p className="text-gray-500 text-sm italic">No food items added to this meal yet.</p>
        ) : (
          <div className="space-y-2 mb-4">
            {selectedFoodItems.map((item) => (
              <div key={item.foodItem.id} className="border rounded-md p-3 flex justify-between items-center">
                <div className="flex-1">
                  <p className="font-medium">{item.foodItem.name}</p>
                  <p className="text-sm text-gray-600">
                    {item.foodItem.serving_size} {item.foodItem.serving_unit} per serving
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <label htmlFor={`servings-${item.foodItem.id}`} className="sr-only">
                    Servings
                  </label>
                  <input
                    type="number"
                    id={`servings-${item.foodItem.id}`}
                    value={item.servings}
                    onChange={(e) => handleServingChange(item.foodItem.id, parseFloat(e.target.value) || 0)}
                    min="0.1"
                    step="0.1"
                    className="w-16 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                  />
                  <span className="text-sm text-gray-600">servings</span>
                  <button
                    type="button"
                    onClick={() => handleRemoveFoodItem(item.foodItem.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {showFoodSelector && (
          <div className="border rounded-md p-4 mb-4">
            <div className="mb-3">
              <label htmlFor="foodSearch" className="sr-only">
                Search Foods
              </label>
              <input
                type="text"
                id="foodSearch"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search your food items..."
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              />
            </div>

            {foodItemsLoading ? (
              <p className="text-gray-500 text-center py-4">Loading food items...</p>
            ) : foodItems.length === 0 ? (
              <p className="text-gray-500 text-center py-4">
                {searchQuery ? 'No matching food items found' : 'No food items available'}
              </p>
            ) : (
              <div className="grid gap-3 max-h-80 overflow-y-auto">
                {foodItems.map((foodItem) => (
                  <FoodItemCard
                    key={foodItem.id}
                    foodItem={foodItem}
                    selectable
                    onSelect={() => handleFoodItemSelect(foodItem)}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      <div>
        <label htmlFor="notes" className="block text-sm font-medium text-gray-700">
          Notes (Optional)
        </label>
        <textarea
          id="notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          rows={3}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          placeholder="Any additional notes about this meal..."
        />
      </div>

      <div>
        <label htmlFor="tags" className="block text-sm font-medium text-gray-700">
          Tags (Optional)
        </label>
        <div className="mt-1 flex rounded-md shadow-sm">
          <input
            type="text"
            id="tags"
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            className="flex-1 min-w-0 block w-full rounded-l-md border-gray-300 focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            placeholder="Add tags separated by comma"
            onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddTag())}
          />
          <button
            type="button"
            onClick={handleAddTag}
            className="inline-flex items-center px-3 py-2 border border-l-0 border-gray-300 rounded-r-md bg-gray-50 text-gray-500 sm:text-sm"
          >
            Add
          </button>
        </div>
        {tags.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            {tags.map((tag) => (
              <span key={tag} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {tag}
                <button
                  type="button"
                  onClick={() => handleRemoveTag(tag)}
                  className="flex-shrink-0 ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center text-blue-400 hover:bg-blue-200 hover:text-blue-500 focus:outline-none focus:bg-blue-500 focus:text-white"
                >
                  <span className="sr-only">Remove {tag} tag</span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          disabled={isSubmitting}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          disabled={isSubmitting || selectedFoodItems.length === 0}
        >
          {isSubmitting ? 'Saving...' : initialData ? 'Update Meal' : 'Log Meal'}
        </button>
      </div>
    </form>
  );
};

export default MealForm;