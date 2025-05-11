import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { MealRequest, MealType } from '../../types/nutrition';
import { useNutrition } from '../../contexts/NutritionContext';

interface LocationState {
  selectedFoodId?: string;
}

const AddEditMeal: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { getMeal, createMeal, updateMeal, getFoodItem } = useNutrition();
  
  const [meal, setMeal] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const isEditMode = !!id;
  
  // Form state
  const [name, setName] = useState('');
  const [mealType, setMealType] = useState<MealType>(MealType.BREAKFAST);
  const [mealTime, setMealTime] = useState<string>(
    new Date().toISOString().slice(0, 16)
  );
  const [notes, setNotes] = useState('');
  const [selectedFoodItems, setSelectedFoodItems] = useState<Array<{
    food_item_id: string;
    food_item_name: string;
    servings: number;
  }>>([]);
  
  // Check if we have a selected food item to add to the meal
  const locationState = location.state as LocationState | null;
  const selectedFoodId = locationState?.selectedFoodId;

  useEffect(() => {
    // Set default meal time to current time
    const now = new Date();
    const localISOTime = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
      .toISOString()
      .slice(0, 16);
    setMealTime(localISOTime);
    
    if (isEditMode) {
      loadMeal();
    } else if (selectedFoodId) {
      // If a food item was passed, load it
      loadSelectedFood(selectedFoodId);
    }
  }, [id, selectedFoodId]);

  const loadMeal = async () => {
    if (!id) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const mealData = await getMeal(id);
      if (mealData) {
        setMeal(mealData);
        setName(mealData.name);
        setMealType(mealData.meal_type as MealType);
        setMealTime(new Date(mealData.meal_time).toISOString().slice(0, 16));
        setNotes(mealData.notes || '');
        
        // Load the food items
        setSelectedFoodItems(
          mealData.food_items.map((item: any) => ({
            food_item_id: item.food_item_id,
            food_item_name: item.food_item_name,
            servings: item.servings
          }))
        );
      } else {
        setError('Meal not found');
      }
    } catch (err) {
      console.error('Error loading meal:', err);
      setError('Failed to load meal');
    } finally {
      setLoading(false);
    }
  };

  const loadSelectedFood = async (foodId: string) => {
    try {
      const foodItem = await getFoodItem(foodId);
      if (foodItem) {
        setSelectedFoodItems([
          {
            food_item_id: foodItem.id,
            food_item_name: foodItem.name,
            servings: 1
          }
        ]);
      }
    } catch (err) {
      console.error('Error loading selected food:', err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (selectedFoodItems.length === 0) {
      setError('Please add at least one food item to the meal');
      return;
    }
    
    setSubmitting(true);
    setError(null);
    
    const mealData: MealRequest = {
      name,
      meal_type: mealType,
      meal_time: new Date(mealTime).toISOString(),
      food_items: selectedFoodItems.map(item => ({
        food_item_id: item.food_item_id,
        servings: item.servings
      })),
      notes: notes || undefined
    };
    
    try {
      if (isEditMode && id) {
        await updateMeal(id, mealData);
        navigate(`/nutrition/meals/${id}`);
      } else {
        const newMeal = await createMeal(mealData);
        if (newMeal) {
          navigate(`/nutrition/meals/${newMeal.id}`);
        } else {
          setError('Failed to create meal');
        }
      }
    } catch (err) {
      console.error('Error saving meal:', err);
      setError('Failed to save meal');
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancel = () => {
    if (isEditMode && id) {
      navigate(`/nutrition/meals/${id}`);
    } else {
      navigate('/nutrition/meals');
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-3xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">
          {isEditMode ? 'Edit Meal' : 'Log Meal'}
        </h1>
        <p className="text-gray-600 mt-1">
          {isEditMode 
            ? 'Update the details of your meal' 
            : 'Track what you ate to monitor your nutrition'}
        </p>
      </div>
      
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}
      
      {loading ? (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <div className="bg-white shadow-sm rounded-lg p-6">
          <form onSubmit={handleSubmit}>
            <div className="space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  Meal Name*
                </label>
                <input
                  type="text"
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="e.g., Breakfast, Post-Workout Snack"
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
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
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
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    required
                  />
                </div>
              </div>
              
              <div>
                <h2 className="text-lg font-medium mb-2">Food Items</h2>
                {selectedFoodItems.length === 0 ? (
                  <div className="bg-gray-50 p-4 rounded-md text-center text-gray-500">
                    <p>No food items added yet. Click "Add Foods" to continue.</p>
                  </div>
                ) : (
                  <ul className="divide-y divide-gray-200 mb-4">
                    {selectedFoodItems.map((item, index) => (
                      <li key={item.food_item_id} className="py-3 flex items-center justify-between">
                        <span className="font-medium">{item.food_item_name}</span>
                        <div className="flex items-center space-x-2">
                          <label htmlFor={`servings-${index}`} className="sr-only">Servings</label>
                          <input
                            type="number"
                            id={`servings-${index}`}
                            value={item.servings}
                            onChange={(e) => {
                              const newItems = [...selectedFoodItems];
                              newItems[index].servings = parseFloat(e.target.value) || 0;
                              setSelectedFoodItems(newItems);
                            }}
                            className="w-16 px-2 py-1 border border-gray-300 rounded-md"
                            min="0.1"
                            step="0.1"
                          />
                          <span className="text-sm text-gray-600">servings</span>
                          <button
                            type="button"
                            onClick={() => {
                              setSelectedFoodItems(
                                selectedFoodItems.filter((_, i) => i !== index)
                              );
                            }}
                            className="text-red-500 hover:text-red-700"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                            </svg>
                          </button>
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
                
                <button
                  type="button"
                  onClick={() => navigate('/nutrition/foods')}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Add Foods
                </button>
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
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Any additional notes about this meal..."
                />
              </div>
              
              <div className="pt-4 flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={handleCancel}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting || selectedFoodItems.length === 0}
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400"
                >
                  {submitting ? 'Saving...' : (isEditMode ? 'Update Meal' : 'Log Meal')}
                </button>
              </div>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default AddEditMeal;