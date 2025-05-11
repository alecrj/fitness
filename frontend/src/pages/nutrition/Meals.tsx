import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useNutrition } from '../../contexts/NutritionContext';
import MealCard from '../../components/nutrition/MealCard';

const Meals: React.FC = () => {
  const navigate = useNavigate();
  const { meals, totalMeals, mealsLoading, mealsError, fetchMeals } = useNutrition();
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [selectedMealType, setSelectedMealType] = useState<string | null>(null);
  
  const itemsPerPage = 12;

  useEffect(() => {
    loadMeals();
  }, [currentPage, selectedDate, selectedMealType]);

  const loadMeals = async () => {
    const params: any = {
      limit: itemsPerPage,
      offset: (currentPage - 1) * itemsPerPage,
    };

    if (selectedDate) {
      params.date = selectedDate;
    }

    if (selectedMealType) {
      params.meal_type = selectedMealType;
    }

    await fetchMeals(params);
  };

  const handleAddMeal = () => {
    navigate('/nutrition/meals/new');
  };

  const handleViewMeal = (mealId: string) => {
    navigate(`/nutrition/meals/${mealId}`);
  };

  const handleEditMeal = (mealId: string) => {
    navigate(`/nutrition/meals/${mealId}/edit`);
  };

  return (
    <div className="container mx-auto p-4">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
        <h1 className="text-2xl font-bold mb-4 md:mb-0">My Meals</h1>
        <button
          onClick={handleAddMeal}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          Log Meal
        </button>
      </div>

      <div className="mb-6">
        <p>Filter controls will be implemented in the next session.</p>
      </div>

      {mealsLoading ? (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : mealsError ? (
        <div className="bg-red-50 border-l-4 border-red-500 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{mealsError}</p>
            </div>
          </div>
        </div>
      ) : meals.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 className="mt-2 text-lg font-medium text-gray-900">No meals found</h3>
          <p className="mt-1 text-sm text-gray-500">
            {selectedDate || selectedMealType
              ? 'Try adjusting your filters'
              : 'Start logging your meals to keep track of your nutrition'}
          </p>
          <div className="mt-6">
            <button
              onClick={handleAddMeal}
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg className="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Log Meal
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {meals.map(meal => (
              <MealCard
                key={meal.id}
                meal={meal}
                onSelect={() => handleViewMeal(meal.id)}
                onEdit={() => handleEditMeal(meal.id)}
              />
            ))}
          </div>

          {totalMeals > itemsPerPage && (
            <div className="flex justify-center mt-8">
              <p>Pagination will be implemented in the next session.</p>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Meals;