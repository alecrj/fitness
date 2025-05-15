import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useNutrition } from '../../contexts/NutritionContext';
import NutritionStats from '../../components/nutrition/NutritionStats';
import MealCard from '../../components/nutrition/MealCard';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { 
    fetchMeals, 
    meals, 
    fetchDailyStats,
    dailyStats,
    statsLoading
  } = useNutrition();

  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().split('T')[0]
  );
  const [statsMode, setStatsMode] = useState<'daily' | 'weekly'>('daily');
  
  useEffect(() => {
    // Fetch meals for the selected date
    fetchMeals({
      date: selectedDate,
      limit: 10
    });
    
    // Fetch stats for the selected date
    fetchDailyStats(selectedDate);
  }, [selectedDate]);

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedDate(e.target.value);
  };

  const handleAddMeal = () => {
    navigate('/nutrition/meals/new');
  };

  const handleViewAllMeals = () => {
    navigate('/nutrition/meals');
  };

  const handleViewMeal = (mealId: string) => {
    navigate(`/nutrition/meals/${mealId}`);
  };

  const handleEditMeal = (mealId: string) => {
    navigate(`/nutrition/meals/${mealId}/edit`);
  };

  const handleQuickLinks = (path: string) => {
    navigate(path);
  };

  const formatDate = (dateString: string): string => {
    const options: Intl.DateTimeFormatOptions = { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <div className="container mx-auto p-4">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold">Nutrition Dashboard</h1>
          <p className="text-gray-600">Track your nutrition goals and progress</p>
        </div>
        <div className="mt-4 md:mt-0">
          <div className="flex space-x-2">
            <input
              type="date"
              value={selectedDate}
              onChange={handleDateChange}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
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
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-sm overflow-hidden">
            <div className="px-4 py-3 bg-gray-50 border-b flex justify-between items-center">
              <h2 className="font-medium">Nutrition Statistics</h2>
              <div className="flex border rounded-md overflow-hidden">
                <button
                  onClick={() => setStatsMode('daily')}
                  className={`px-3 py-1 text-sm ${
                    statsMode === 'daily'
                      ? 'bg-blue-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  Daily
                </button>
                <button
                  onClick={() => setStatsMode('weekly')}
                  className={`px-3 py-1 text-sm ${
                    statsMode === 'weekly'
                      ? 'bg-blue-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  Weekly
                </button>
              </div>
            </div>
            <div className="p-4">
              <NutritionStats mode={statsMode} />
            </div>
          </div>
        </div>

        <div>
          <div className="bg-white rounded-lg shadow-sm overflow-hidden mb-6">
            <div className="px-4 py-3 bg-gray-50 border-b">
              <h2 className="font-medium">Quick Links</h2>
            </div>
            <div className="p-4">
              <div className="space-y-2">
                <button
                  onClick={() => handleQuickLinks('/nutrition/foods')}
                  className="w-full flex items-center justify-between px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-md"
                >
                  <span className="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    My Food Items
                  </span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
                <button
                  onClick={() => handleQuickLinks('/nutrition/foods/new')}
                  className="w-full flex items-center justify-between px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-md"
                >
                  <span className="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                    Add Food Item
                  </span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
                <button
                  onClick={() => handleQuickLinks('/nutrition/usda-search')}
                  className="w-full flex items-center justify-between px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-md"
                >
                  <span className="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    USDA Database
                  </span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
                <button
                  onClick={() => handleQuickLinks('/nutrition/meals')}
                  className="w-full flex items-center justify-between px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-md"
                >
                  <span className="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Meal History
                  </span>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          {!statsLoading && dailyStats && (
            <div className="bg-white rounded-lg shadow-sm overflow-hidden">
              <div className="px-4 py-3 bg-gray-50 border-b">
                <h2 className="font-medium">Macronutrient Breakdown</h2>
              </div>
              <div className="p-4">
                {dailyStats.total.calories > 0 ? (
                  <>
                    <div className="mb-6">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700">Protein</span>
                        <span className="text-sm text-gray-600">
                          {Math.round((dailyStats.total.protein * 4 / dailyStats.total.calories) * 100)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2.5">
                        <div
                          className="bg-green-600 h-2.5 rounded-full"
                          style={{ width: `${Math.round((dailyStats.total.protein * 4 / dailyStats.total.calories) * 100)}%` }}
                        />
                      </div>
                    </div>
                    <div className="mb-6">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700">Carbs</span>
                        <span className="text-sm text-gray-600">
                          {Math.round((dailyStats.total.carbs * 4 / dailyStats.total.calories) * 100)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2.5">
                        <div
                          className="bg-yellow-600 h-2.5 rounded-full"
                          style={{ width: `${Math.round((dailyStats.total.carbs * 4 / dailyStats.total.calories) * 100)}%` }}
                        />
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700">Fat</span>
                        <span className="text-sm text-gray-600">
                          {Math.round((dailyStats.total.fat * 9 / dailyStats.total.calories) * 100)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2.5">
                        <div
                          className="bg-purple-600 h-2.5 rounded-full"
                          style={{ width: `${Math.round((dailyStats.total.fat * 9 / dailyStats.total.calories) * 100)}%` }}
                        />
                      </div>
                    </div>
                  </>
                ) : (
                  <p className="text-gray-500 text-center py-4">
                    No data available for the selected date
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="mb-8">
        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="px-4 py-3 bg-gray-50 border-b flex justify-between items-center">
            <h2 className="font-medium">Meals for {formatDate(selectedDate)}</h2>
            <button
              onClick={handleViewAllMeals}
              className="text-blue-600 hover:text-blue-800 text-sm"
            >
              View All Meals
            </button>
          </div>
          <div className="p-4">
            {meals.length === 0 ? (
              <div className="text-center py-8">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 className="mt-2 text-lg font-medium text-gray-900">No meals logged</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Get started by logging your first meal for this day.
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
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;