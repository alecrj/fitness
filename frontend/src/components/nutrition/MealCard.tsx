import React from 'react';
import { Meal, MealType } from '../../types/nutrition';
import { useNutrition } from '../../contexts/NutritionContext';

interface MealCardProps {
  meal: Meal;
  onSelect?: () => void;
  onEdit?: () => void;
  onDelete?: () => void;
}

const MealCard: React.FC<MealCardProps> = ({ 
  meal, 
  onSelect, 
  onEdit, 
  onDelete 
}) => {
  // Helper function to format date/time
  const formatDateTime = (dateTimeString: string): string => {
    const date = new Date(dateTimeString);
    return new Intl.DateTimeFormat('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      hour12: true
    }).format(date);
  };

  // Helper function to get meal type badge color
  const getMealTypeColor = (type: MealType): string => {
    switch (type) {
      case MealType.BREAKFAST:
        return 'bg-yellow-100 text-yellow-800';
      case MealType.LUNCH:
        return 'bg-green-100 text-green-800';
      case MealType.DINNER:
        return 'bg-blue-100 text-blue-800';
      case MealType.SNACK:
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // Handle card click
  const handleCardClick = () => {
    if (onSelect) {
      onSelect();
    }
  };

  // Handle edit click
  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onEdit) {
      onEdit();
    }
  };

  // Handle delete click
  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onDelete) {
      onDelete();
    }
  };

  return (
    <div 
      className="border rounded-lg p-4 shadow-sm hover:shadow-md transition-all cursor-pointer"
      onClick={handleCardClick}
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-medium text-lg">{meal.name}</h3>
          <p className="text-sm text-gray-600">{formatDateTime(meal.meal_time)}</p>
        </div>
        <div className="flex items-center space-x-2">
          <span className={`inline-block px-2 py-1 text-xs rounded-full ${getMealTypeColor(meal.meal_type)}`}>
            {meal.meal_type.charAt(0).toUpperCase() + meal.meal_type.slice(1)}
          </span>
          {onEdit && (
            <button 
              onClick={handleEdit}
              className="text-blue-500 hover:text-blue-600"
              title="Edit meal"
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
              title="Delete meal"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          )}
        </div>
      </div>

      <div className="mt-3">
        <div className="flex justify-between items-center mb-2">
          <h4 className="font-medium text-sm">Nutrition Summary</h4>
          <span className="text-sm font-medium">{meal.food_items.length} food item(s)</span>
        </div>
        <div className="grid grid-cols-4 gap-2">
          <div className="text-center">
            <p className="text-sm font-medium">{meal.nutrition_totals.calories}</p>
            <p className="text-xs text-gray-600">Calories</p>
          </div>
          <div className="text-center">
            <p className="text-sm font-medium">{meal.nutrition_totals.protein}g</p>
            <p className="text-xs text-gray-600">Protein</p>
          </div>
          <div className="text-center">
            <p className="text-sm font-medium">{meal.nutrition_totals.carbs}g</p>
            <p className="text-xs text-gray-600">Carbs</p>
          </div>
          <div className="text-center">
            <p className="text-sm font-medium">{meal.nutrition_totals.fat}g</p>
            <p className="text-xs text-gray-600">Fat</p>
          </div>
        </div>
      </div>

      {meal.tags && meal.tags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1">
          {meal.tags.map(tag => (
            <span 
              key={tag} 
              className="inline-block bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      {meal.notes && (
        <div className="mt-3 border-t pt-2">
          <p className="text-sm text-gray-600 line-clamp-2">{meal.notes}</p>
        </div>
      )}
    </div>
  );
};

export default MealCard;