import React, { useEffect, useState } from 'react';
import { NutritionStats as NutritionStatsType, WeeklyNutritionStats, MealType } from '../../types/nutrition';
import { useNutrition } from '../../contexts/NutritionContext';

interface NutritionStatsProps {
  mode: 'daily' | 'weekly';
}

const NutritionStats: React.FC<NutritionStatsProps> = ({ mode }) => {
  const { 
    fetchDailyStats, 
    fetchWeeklyStats, 
    dailyStats, 
    weeklyStats, 
    statsLoading, 
    statsError 
  } = useNutrition();

  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().split('T')[0]
  );
  const [dateRange, setDateRange] = useState<{ start: string; end: string }>(() => {
    const today = new Date();
    const lastWeek = new Date(today);
    lastWeek.setDate(today.getDate() - 6);
    
    return {
      start: lastWeek.toISOString().split('T')[0],
      end: today.toISOString().split('T')[0]
    };
  });

  useEffect(() => {
    if (mode === 'daily') {
      fetchDailyStats(selectedDate);
    } else {
      fetchWeeklyStats(dateRange.start, dateRange.end);
    }
  }, [mode, selectedDate, dateRange, fetchDailyStats, fetchWeeklyStats]);

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedDate(e.target.value);
  };

  const handleStartDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDateRange(prev => ({ ...prev, start: e.target.value }));
  };

  const handleEndDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDateRange(prev => ({ ...prev, end: e.target.value }));
  };

  // Calculate progress percentage for nutrition goals
  const calculateProgress = (current: number, goal: number): number => {
    if (!goal) return 0;
    const percentage = (current / goal) * 100;
    return Math.min(percentage, 100); // Cap at 100%
  };

  const renderDailyStats = (stats: NutritionStatsType) => (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Calories</h3>
          <p className="text-3xl font-bold">{stats.total.calories}</p>
          {stats.goal?.calories && (
            <div className="mt-2">
              <div className="flex justify-between text-xs text-gray-500">
                <span>{Math.round((stats.total.calories / stats.goal.calories) * 100)}%</span>
                <span>Goal: {stats.goal.calories}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5 mt-1">
                <div 
                  className="bg-blue-600 h-2.5 rounded-full" 
                  style={{ width: `${calculateProgress(stats.total.calories, stats.goal.calories)}%` }}
                />
              </div>
            </div>
          )}
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Protein</h3>
          <p className="text-3xl font-bold">{stats.total.protein}g</p>
          {stats.goal?.protein && (
            <div className="mt-2">
              <div className="flex justify-between text-xs text-gray-500">
                <span>{Math.round((stats.total.protein / stats.goal.protein) * 100)}%</span>
                <span>Goal: {stats.goal.protein}g</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5 mt-1">
                <div 
                  className="bg-green-600 h-2.5 rounded-full" 
                  style={{ width: `${calculateProgress(stats.total.protein, stats.goal.protein)}%` }}
                />
              </div>
            </div>
          )}
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Carbs</h3>
          <p className="text-3xl font-bold">{stats.total.carbs}g</p>
          {stats.goal?.carbs && (
            <div className="mt-2">
              <div className="flex justify-between text-xs text-gray-500">
                <span>{Math.round((stats.total.carbs / stats.goal.carbs) * 100)}%</span>
                <span>Goal: {stats.goal.carbs}g</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5 mt-1">
                <div 
                  className="bg-yellow-600 h-2.5 rounded-full" 
                  style={{ width: `${calculateProgress(stats.total.carbs, stats.goal.carbs)}%` }}
                />
              </div>
            </div>
          )}
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Fat</h3>
          <p className="text-3xl font-bold">{stats.total.fat}g</p>
          {stats.goal?.fat && (
            <div className="mt-2">
              <div className="flex justify-between text-xs text-gray-500">
                <span>{Math.round((stats.total.fat / stats.goal.fat) * 100)}%</span>
                <span>Goal: {stats.goal.fat}g</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5 mt-1">
                <div 
                  className="bg-purple-600 h-2.5 rounded-full" 
                  style={{ width: `${calculateProgress(stats.total.fat, stats.goal.fat)}%` }}
                />
              </div>
            </div>
          )}
        </div>
      </div>
      
      <h3 className="text-lg font-medium text-gray-900 mb-3">Breakdown by Meal</h3>
      {Object.entries(stats.by_meal).length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(stats.by_meal).map(([mealTypeKey, mealData]) => (
            <div key={mealTypeKey} className="bg-white p-4 rounded-lg shadow">
              <h4 className="font-medium">{mealTypeKey.charAt(0).toUpperCase() + mealTypeKey.slice(1)}</h4>
              <p className="text-sm text-gray-500">{mealData.count} meal(s)</p>
              
              <div className="mt-3 grid grid-cols-4 gap-2 text-center">
                <div>
                  <p className="font-medium">{mealData.nutrition.calories}</p>
                  <p className="text-xs text-gray-500">Calories</p>
                </div>
                <div>
                  <p className="font-medium">{mealData.nutrition.protein}g</p>
                  <p className="text-xs text-gray-500">Protein</p>
                </div>
                <div>
                  <p className="font-medium">{mealData.nutrition.carbs}g</p>
                  <p className="text-xs text-gray-500">Carbs</p>
                </div>
                <div>
                  <p className="font-medium">{mealData.nutrition.fat}g</p>
                  <p className="text-xs text-gray-500">Fat</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-gray-500 italic">No meals logged for this day.</p>
      )}
    </div>
  );

  const renderWeeklyStats = (stats: WeeklyNutritionStats) => (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Avg. Calories</h3>
          <p className="text-3xl font-bold">{Math.round(stats.average.calories)}</p>
          <p className="text-sm text-gray-500 mt-1">Total: {stats.total.calories}</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Avg. Protein</h3>
          <p className="text-3xl font-bold">{Math.round(stats.average.protein)}g</p>
          <p className="text-sm text-gray-500 mt-1">Total: {stats.total.protein}g</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Avg. Carbs</h3>
          <p className="text-3xl font-bold">{Math.round(stats.average.carbs)}g</p>
          <p className="text-sm text-gray-500 mt-1">Total: {stats.total.carbs}g</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900">Avg. Fat</h3>
          <p className="text-3xl font-bold">{Math.round(stats.average.fat)}g</p>
          <p className="text-sm text-gray-500 mt-1">Total: {stats.total.fat}g</p>
        </div>
      </div>
      
      <h3 className="text-lg font-medium text-gray-900 mb-3">Daily Breakdown</h3>
      <div className="bg-white p-4 rounded-lg shadow overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Calories</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Protein (g)</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Carbs (g)</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fat (g)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {stats.daily_stats.map((day) => (
              <tr key={day.date}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {new Date(day.date).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {day.nutrition.calories}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {day.nutrition.protein}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {day.nutrition.carbs}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {day.nutrition.fat}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  return (
    <div>
      <div className="mb-6">
        {mode === 'daily' ? (
          <div>
            <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-1">
              Select Date
            </label>
            <input
              type="date"
              id="date"
              value={selectedDate}
              onChange={handleDateChange}
              className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            />
          </div>
        ) : (
          <div className="flex flex-col sm:flex-row sm:space-x-4">
            <div>
              <label htmlFor="startDate" className="block text-sm font-medium text-gray-700 mb-1">
                Start Date
              </label>
              <input
                type="date"
                id="startDate"
                value={dateRange.start}
                onChange={handleStartDateChange}
                className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="endDate" className="block text-sm font-medium text-gray-700 mb-1">
                End Date
              </label>
              <input
                type="date"
                id="endDate"
                value={dateRange.end}
                onChange={handleEndDateChange}
                className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              />
            </div>
          </div>
        )}
      </div>

      {statsLoading ? (
        <div className="flex justify-center items-center py-8">
          <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      ) : statsError ? (
        <div className="bg-red-50 border-l-4 border-red-500 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{statsError}</p>
            </div>
          </div>
        </div>
      ) : mode === 'daily' && dailyStats ? (
        renderDailyStats(dailyStats)
      ) : mode === 'weekly' && weeklyStats ? (
        renderWeeklyStats(weeklyStats)
      ) : (
        <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                No nutrition data available for the selected {mode === 'daily' ? 'date' : 'date range'}.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NutritionStats;