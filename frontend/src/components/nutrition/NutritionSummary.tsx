import React from 'react';
import { NutritionData } from '../../types/nutrition';

interface NutritionSummaryProps {
  nutrition: NutritionData;
  title?: string;
  showDetails?: boolean;
  goals?: NutritionData;
}

const NutritionSummary: React.FC<NutritionSummaryProps> = ({
  nutrition,
  title = 'Nutrition Summary',
  showDetails = false,
  goals
}) => {
  // Calculate progress percentage for nutrition goals
  const calculateProgress = (current: number, goal: number): number => {
    if (!goal) return 0;
    const percentage = (current / goal) * 100;
    return Math.min(percentage, 100); // Cap at 100%
  };

  return (
    <div className="bg-white rounded-lg shadow p-4">
      {title && <h3 className="text-lg font-medium mb-3">{title}</h3>}
      
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-gray-600 text-sm">Calories</p>
          <div className="flex items-baseline">
            <p className="text-2xl font-medium mr-2">{nutrition.calories}</p>
            {goals?.calories && (
              <p className="text-sm text-gray-500">
                of {goals.calories} ({Math.round((nutrition.calories / goals.calories) * 100)}%)
              </p>
            )}
          </div>
          {goals?.calories && (
            <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
              <div 
                className="bg-blue-600 rounded-full h-2"
                style={{ width: `${calculateProgress(nutrition.calories, goals.calories)}%` }}
              />
            </div>
          )}
        </div>
        
        <div>
          <p className="text-gray-600 text-sm">Protein</p>
          <div className="flex items-baseline">
            <p className="text-2xl font-medium mr-2">{nutrition.protein}g</p>
            {goals?.protein && (
              <p className="text-sm text-gray-500">
                of {goals.protein}g ({Math.round((nutrition.protein / goals.protein) * 100)}%)
              </p>
            )}
          </div>
          {goals?.protein && (
            <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
              <div 
                className="bg-green-600 rounded-full h-2"
                style={{ width: `${calculateProgress(nutrition.protein, goals.protein)}%` }}
              />
            </div>
          )}
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-gray-600 text-sm">Carbs</p>
          <div className="flex items-baseline">
            <p className="text-2xl font-medium mr-2">{nutrition.carbs}g</p>
            {goals?.carbs && (
              <p className="text-sm text-gray-500">
                of {goals.carbs}g ({Math.round((nutrition.carbs / goals.carbs) * 100)}%)
              </p>
            )}
          </div>
          {goals?.carbs && (
            <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
              <div 
                className="bg-yellow-600 rounded-full h-2"
                style={{ width: `${calculateProgress(nutrition.carbs, goals.carbs)}%` }}
              />
            </div>
          )}
        </div>
        
        <div>
          <p className="text-gray-600 text-sm">Fat</p>
          <div className="flex items-baseline">
            <p className="text-2xl font-medium mr-2">{nutrition.fat}g</p>
            {goals?.fat && (
              <p className="text-sm text-gray-500">
                of {goals.fat}g ({Math.round((nutrition.fat / goals.fat) * 100)}%)
              </p>
            )}
          </div>
          {goals?.fat && (
            <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
              <div 
                className="bg-purple-600 rounded-full h-2"
                style={{ width: `${calculateProgress(nutrition.fat, goals.fat)}%` }}
              />
            </div>
          )}
        </div>
      </div>
      
      {showDetails && (
        <div className="grid grid-cols-2 gap-4 mt-4 pt-4 border-t border-gray-200">
          {nutrition.fiber !== undefined && (
            <div>
              <p className="text-gray-600 text-sm">Fiber</p>
              <p className="text-lg font-medium">{nutrition.fiber}g</p>
            </div>
          )}
          
          {nutrition.sugar !== undefined && (
            <div>
              <p className="text-gray-600 text-sm">Sugar</p>
              <p className="text-lg font-medium">{nutrition.sugar}g</p>
            </div>
          )}
          
          {nutrition.sodium !== undefined && (
            <div>
              <p className="text-gray-600 text-sm">Sodium</p>
              <p className="text-lg font-medium">{nutrition.sodium}mg</p>
            </div>
          )}
          
          {nutrition.cholesterol !== undefined && (
            <div>
              <p className="text-gray-600 text-sm">Cholesterol</p>
              <p className="text-lg font-medium">{nutrition.cholesterol}mg</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NutritionSummary;