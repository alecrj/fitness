import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useNutrition } from '../../contexts/NutritionContext';
import USDAFoodSearch from '../../components/nutrition/USDAFoodSearch';

const USDASearch: React.FC = () => {
  const navigate = useNavigate();
  const [importSuccess, setImportSuccess] = useState(false);

  const handleImportSuccess = () => {
    setImportSuccess(true);
    
    // Reset the success message after 3 seconds
    setTimeout(() => {
      setImportSuccess(false);
    }, 3000);
  };

  const handleBackToFoods = () => {
    navigate('/nutrition/foods');
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <div className="mb-6">
        <button
          onClick={handleBackToFoods}
          className="flex items-center text-blue-600 hover:text-blue-800"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
          </svg>
          Back to Food Items
        </button>
      </div>

      <div className="bg-white shadow-sm rounded-lg overflow-hidden">
        <div className="bg-gray-50 p-4 border-b">
          <h1 className="text-2xl font-bold">USDA Food Database</h1>
          <p className="text-gray-600">
            Search and import food items from the USDA food database
          </p>
        </div>

        {importSuccess && (
          <div className="bg-green-50 border-l-4 border-green-500 p-4 mx-4 mt-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-green-700">
                  Food item successfully imported to your database.
                </p>
              </div>
            </div>
          </div>
        )}

        <div className="p-6">
          <USDAFoodSearch onImport={handleImportSuccess} />
        </div>
      </div>
      
      <div className="mt-8 bg-blue-50 rounded-lg p-6">
        <h2 className="text-lg font-medium text-blue-800 mb-2">About the USDA Food Database</h2>
        <p className="text-blue-700 mb-3">
          The USDA Food Data Central provides information about food items, including their nutrition content.
        </p>
        <div className="space-y-2 text-blue-700">
          <p>
            <strong>Tips for searching:</strong>
          </p>
          <ul className="list-disc pl-5 space-y-1">
            <li>Be specific in your search terms (e.g., "raw apple" instead of just "apple")</li>
            <li>Include brand names when looking for packaged foods</li>
            <li>Try different variations of the food name if you don't find what you're looking for</li>
            <li>Search results include branded foods, foundation foods, survey (FNDDS) foods, and more</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default USDASearch;