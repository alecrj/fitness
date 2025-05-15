import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Meal } from '../../types/nutrition';
import { useNutrition } from '../../contexts/NutritionContext';
import NutritionSummary from '../../components/nutrition/NutritionSummary';

const MealDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { getMeal, deleteMeal } = useNutrition();
  
  const [meal, setMeal] = useState<Meal | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    if (id) {
      loadMeal();
    }
  }, [id]);

  const loadMeal = async () => {
    if (!id) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const mealData = await getMeal(id);
      if (mealData) {
        setMeal(mealData);
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

  const handleEdit = () => {
    if (id) {
      navigate(`/nutrition/meals/${id}/edit`);
    }
  };

  const handleDelete = async () => {
    if (!id) return;
    
    if (window.confirm('Are you sure you want to delete this meal?')) {
      try {
        await deleteMeal(id);
        navigate('/nutrition/meals');
      } catch (err) {
        console.error('Error deleting meal:', err);
        setError('Failed to delete meal');
      }
    }
  };

  const handleBack = () => {
    navigate('/nutrition/meals');
  };

  // Format date for display
  const formatDateTime = (dateTimeString: string): string => {
    const date = new Date(dateTimeString);
    return new Intl.DateTimeFormat('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      hour12: true
    }).format(date);
  };

  if (loading) {
    return (
      <div className="container mx-auto p-4 flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !meal) {
    return (
      <div className="container mx-auto p-4">
        <div className="bg-red-50 border-l-4 border-red-500 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error || 'Meal not found'}</p>
              <div className="mt-2">
                <button
                  onClick={handleBack}
                  className="bg-white text-red-700 hover:bg-red-100 px-3 py-1 rounded-md text-sm font-medium"
                >
                  Go back to meals
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <button
        onClick={handleBack}
        className="flex items-center text-blue-600 hover:text-blue-800 mb-4"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
        </svg>
        Back to Meals
      </button>

      <div className="bg-white shadow-sm rounded-lg overflow-hidden mb-6">
        <div className="bg-gray-50 p-4 flex justify-between items-center border-b">
          <div>
            <h1 className="text-2xl font-bold">{meal.name}</h1>
            <p className="text-gray-600">{formatDateTime(meal.meal_time)}</p>
          </div>
          <div className="flex space-x-2">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              meal.meal_type === 'breakfast' ? 'bg-yellow-100 text-yellow-800' :
              meal.meal_type === 'lunch' ? 'bg-green-100 text-green-800' :
              meal.meal_type === 'dinner' ? 'bg-blue-100 text-blue-800' : 
              'bg-purple-100 text-purple-800'
            }`}>
              {meal.meal_type.charAt(0).toUpperCase() + meal.meal_type.slice(1)}
            </span>
            <button
              onClick={handleEdit}
              className="p-2 rounded-full text-blue-500 hover:text-blue-600 bg-blue-100"
              title="Edit meal"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              onClick={handleDelete}
              className="p-2 rounded-full text-red-500 hover:text-red-600 bg-red-100"
              title="Delete meal"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>

        <div className="p-6">
          <div className="mb-6">
            <h2 className="text-lg font-medium mb-2">Nutrition Summary</h2>
            <NutritionSummary 
              nutrition={meal.nutrition_totals} 
              showDetails={true}
            />
          </div>

          <div className="mb-6">
            <h2 className="text-lg font-medium mb-2">Food Items</h2>
            <div className="bg-gray-50 rounded-lg p-4">
              <ul className="divide-y divide-gray-200">
                {meal.food_items.map((item) => (
                  <li key={item.food_item_id} className="py-3 flex justify-between">
                    <div>
                      <p className="font-medium">{item.food_item_name}</p>
                      <p className="text-sm text-gray-600">
                        {item.nutrition.calories} cal, {item.nutrition.protein}g protein, 
                        {item.nutrition.carbs}g carbs, {item.nutrition.fat}g fat
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium">{item.servings} servings</p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {meal.notes && (
            <div className="mb-6">
              <h2 className="text-lg font-medium mb-2">Notes</h2>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-gray-700">{meal.notes}</p>
              </div>
            </div>
          )}

          {meal.tags && meal.tags.length > 0 && (
            <div>
              <h2 className="text-lg font-medium mb-2">Tags</h2>
              <div className="flex flex-wrap gap-2">
                {meal.tags.map(tag => (
                  <span 
                    key={tag} 
                    className="inline-block bg-gray-100 text-gray-800 px-2 py-1 rounded"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MealDetail;