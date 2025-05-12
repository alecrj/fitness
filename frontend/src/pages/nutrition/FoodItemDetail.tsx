import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FoodItem } from '../../types/nutrition';
import { useNutrition } from '../../contexts/NutritionContext';
import NutritionSummary from '../../components/nutrition/NutritionSummary';

const FoodItemDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { getFoodItem, deleteFoodItem, toggleFavorite } = useNutrition();
  
  const [foodItem, setFoodItem] = useState<FoodItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    if (id) {
      loadFoodItem();
    }
  }, [id]);

  const loadFoodItem = async () => {
    if (!id) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await getFoodItem(id);
      if (data) {
        setFoodItem(data);
      } else {
        setError('Food item not found');
      }
    } catch (err) {
      console.error('Error loading food item:', err);
      setError('Failed to load food item');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    if (id) {
      navigate(`/nutrition/foods/${id}/edit`);
    }
  };

  const handleDelete = async () => {
    if (!id) return;
    
    if (window.confirm('Are you sure you want to delete this food item?')) {
      try {
        await deleteFoodItem(id);
        navigate('/nutrition/foods');
      } catch (err) {
        console.error('Error deleting food item:', err);
        setError('Failed to delete food item');
      }
    }
  };

  const handleToggleFavorite = async () => {
    if (!id) return;
    
    try {
      await toggleFavorite(id);
      loadFoodItem(); // Reload to get updated data
    } catch (err) {
      console.error('Error toggling favorite status:', err);
      setError('Failed to update favorite status');
    }
  };

  const handleBack = () => {
    navigate('/nutrition/foods');
  };

  if (loading) {
    return (
      <div className="container mx-auto p-4 flex justify-center items-center min-h-screen-minus-nav">
        <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    );
  }

  if (error || !foodItem) {
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
              <p className="text-sm text-red-700">{error || 'Food item not found'}</p>
              <div className="mt-2">
                <button
                  onClick={handleBack}
                  className="bg-white text-red-700 hover:bg-red-100 px-3 py-1 rounded-md text-sm font-medium"
                >
                  Go back to food items
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
        Back to Food Items
      </button>

      <div className="bg-white shadow-sm rounded-lg overflow-hidden mb-6">
        <div className="bg-gray-50 p-4 flex justify-between items-center border-b">
          <div>
            <h1 className="text-2xl font-bold">{foodItem.name}</h1>
            {foodItem.brand && (
              <p className="text-gray-600">{foodItem.brand}</p>
            )}
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleToggleFavorite}
              className={`p-2 rounded-full ${
                foodItem.is_favorite
                  ? 'text-yellow-500 hover:text-yellow-600 bg-yellow-100'
                  : 'text-gray-400 hover:text-yellow-500 bg-gray-100 hover:bg-yellow-100'
              }`}
              title={foodItem.is_favorite ? 'Remove from favorites' : 'Add to favorites'}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill={foodItem.is_favorite ? 'currentColor' : 'none'} viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={foodItem.is_favorite ? 0 : 2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
            </button>
            <button
              onClick={handleEdit}
              className="p-2 rounded-full text-blue-500 hover:text-blue-600 bg-blue-100"
              title="Edit food item"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              onClick={handleDelete}
              className="p-2 rounded-full text-red-500 hover:text-red-600 bg-red-100"
              title="Delete food item"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>

        <div className="p-6">
          <div className="mb-6">
            <h2 className="text-lg font-medium mb-2">Serving Information</h2>
            <p className="text-gray-600">
              {foodItem.serving_size} {foodItem.serving_unit} per serving
            </p>
          </div>

          <div className="mb-6">
            <h2 className="text-lg font-medium mb-2">Nutrition Information</h2>
            <NutritionSummary 
              nutrition={foodItem.nutrition} 
              title="" 
              showDetails={true} 
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h2 className="text-lg font-medium mb-2">Details</h2>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="grid grid-cols-2 gap-y-2">
                  <div className="text-gray-600">Type:</div>
                  <div>
                    {foodItem.is_custom ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        Custom
                      </span>
                    ) : foodItem.fdcId ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        USDA Database
                      </span>
                    ) : (
                      'Standard'
                    )}
                  </div>
                  
                  {foodItem.fdcId && (
                    <>
                      <div className="text-gray-600">USDA ID:</div>
                      <div>{foodItem.fdcId}</div>
                    </>
                  )}
                  
                  {foodItem.barcode && (
                    <>
                      <div className="text-gray-600">Barcode:</div>
                      <div>{foodItem.barcode}</div>
                    </>
                  )}
                  
                  <div className="text-gray-600">Created:</div>
                  <div>{new Date(foodItem.created_at).toLocaleDateString()}</div>
                  
                  <div className="text-gray-600">Last Updated:</div>
                  <div>{new Date(foodItem.updated_at).toLocaleDateString()}</div>
                </div>
              </div>
            </div>
            
            <div>
              <h2 className="text-lg font-medium mb-2">Quick Add to Meal</h2>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-600 mb-3">Add this food to a meal log:</p>
                <div className="space-y-2">
                  <button
                    onClick={() => navigate('/nutrition/meals/new', { 
                      state: { selectedFoodId: foodItem.id } 
                    })}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-md"
                  >
                    Log This Food
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FoodItemDetail;