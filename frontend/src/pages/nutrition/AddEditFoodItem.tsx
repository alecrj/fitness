import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FoodItemRequest } from '../../types/nutrition';
import FoodItemForm from '../../components/nutrition/FoodItemForm';
import { useNutrition } from '../../contexts/NutritionContext';

const AddEditFoodItem: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { getFoodItem, createFoodItem, updateFoodItem } = useNutrition();
  
  const [foodItem, setFoodItem] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const isEditMode = !!id;

  useEffect(() => {
    if (isEditMode) {
      loadFoodItem();
    }
  }, [id]);

  const loadFoodItem = async () => {
    if (!id) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const foodItemData = await getFoodItem(id);
      if (foodItemData) {
        setFoodItem(foodItemData);
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

  const handleSubmit = async (data: FoodItemRequest) => {
    setSubmitting(true);
    setError(null);
    
    try {
      if (isEditMode && id) {
        await updateFoodItem(id, data);
        navigate(`/nutrition/foods/${id}`);
      } else {
        const newFoodItem = await createFoodItem(data);
        if (newFoodItem) {
          navigate(`/nutrition/foods/${newFoodItem.id}`);
        } else {
          setError('Failed to create food item');
        }
      }
    } catch (err) {
      console.error('Error saving food item:', err);
      setError('Failed to save food item');
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancel = () => {
    if (isEditMode && id) {
      navigate(`/nutrition/foods/${id}`);
    } else {
      navigate('/nutrition/foods');
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-3xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">
          {isEditMode ? 'Edit Food Item' : 'Add Food Item'}
        </h1>
        <p className="text-gray-600 mt-1">
          {isEditMode 
            ? 'Update the details of your food item' 
            : 'Add a new food item to your personal database'}
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
          <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      ) : (
        <div className="bg-white shadow-sm rounded-lg p-6">
          <FoodItemForm
            initialData={foodItem}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isSubmitting={submitting}
          />
        </div>
      )}
    </div>
  );
};

export default AddEditFoodItem;