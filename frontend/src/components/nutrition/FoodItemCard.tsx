import React from 'react';
import { FoodItem } from '../../types/nutrition';
import { useNutrition } from '../../contexts/NutritionContext';

interface FoodItemCardProps {
  foodItem: FoodItem;
  onSelect?: () => void;
  selectable?: boolean;
  onEdit?: () => void;
  onDelete?: () => void;
}

const FoodItemCard: React.FC<FoodItemCardProps> = ({ 
  foodItem, 
  onSelect, 
  selectable = false,
  onEdit,
  onDelete
}) => {
  const { toggleFavorite } = useNutrition();

  const handleFavoriteToggle = async (e: React.MouseEvent) => {
    e.stopPropagation();
    await toggleFavorite(foodItem.id);
  };

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onEdit) onEdit();
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onDelete) onDelete();
  };

  const cardClickHandler = () => {
    if (selectable && onSelect) {
      onSelect();
    }
  };

  return (
    <div 
      className={`border rounded-lg p-4 shadow-sm hover:shadow-md transition-all ${selectable ? 'cursor-pointer' : ''}`}
      onClick={cardClickHandler}
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-medium text-lg">{foodItem.name}</h3>
          {foodItem.brand && (
            <p className="text-sm text-gray-600">{foodItem.brand}</p>
          )}
        </div>
        <div className="flex items-center space-x-2">
          <button 
            onClick={handleFavoriteToggle}
            className="text-yellow-500 hover:text-yellow-600"
            title={foodItem.is_favorite ? "Remove from favorites" : "Add to favorites"}
          >
            {foodItem.is_favorite ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
            )}
          </button>
          {onEdit && (
            <button 
              onClick={handleEdit}
              className="text-blue-500 hover:text-blue-600"
              title="Edit food item"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
          )}
          {onDelete && (
            <button 
              onClick={handleDelete}
              className="text-red-500 hover:text-red-600"
              title="Delete food item"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          )}
        </div>
      </div>

      <div className="mt-2">
        <p className="text-sm">
          {foodItem.serving_size} {foodItem.serving_unit}
        </p>
      </div>

      <div className="mt-3 grid grid-cols-4 gap-2">
        <div className="text-center">
          <p className="text-sm font-medium">{foodItem.nutrition.calories}</p>
          <p className="text-xs text-gray-600">Calories</p>
        </div>
        <div className="text-center">
          <p className="text-sm font-medium">{foodItem.nutrition.protein}g</p>
          <p className="text-xs text-gray-600">Protein</p>
        </div>
        <div className="text-center">
          <p className="text-sm font-medium">{foodItem.nutrition.carbs}g</p>
          <p className="text-xs text-gray-600">Carbs</p>
        </div>
        <div className="text-center">
          <p className="text-sm font-medium">{foodItem.nutrition.fat}g</p>
          <p className="text-xs text-gray-600">Fat</p>
        </div>
      </div>

      {foodItem.is_custom ? (
        <div className="mt-2">
          <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">Custom</span>
        </div>
      ) : foodItem.fdcId ? (
        <div className="mt-2">
          <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded">USDA</span>
        </div>
      ) : null}
    </div>
  );
};

export default FoodItemCard;