import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FoodItem } from '../../types/nutrition';
import FoodItemCard from '../../components/nutrition/FoodItemCard';
import { useNutrition } from '../../contexts/NutritionContext';
import BarcodeScanner from '../../components/nutrition/BarcodeScanner';

const FoodItems: React.FC = () => {
  const navigate = useNavigate();
  const { 
    foodItems, 
    totalFoodItems, 
    foodItemsLoading, 
    foodItemsError, 
    fetchFoodItems, 
    deleteFoodItem 
  } = useNutrition();

  const [searchQuery, setSearchQuery] = useState('');
  const [showFavorites, setShowFavorites] = useState(false);
  const [showCustomOnly, setShowCustomOnly] = useState(false);
  const [showBarcodeScanner, setShowBarcodeScanner] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 12;

  useEffect(() => {
    loadFoodItems();
  }, [showFavorites, showCustomOnly, searchQuery, currentPage]);

  const loadFoodItems = async () => {
    const params: any = {
      limit: itemsPerPage,
      offset: (currentPage - 1) * itemsPerPage
    };

    if (showFavorites) {
      params.is_favorite = true;
    }

    if (showCustomOnly) {
      params.is_custom = true;
    }

    if (searchQuery) {
      params.q = searchQuery;
    }

    await fetchFoodItems(params);
  };

  const handleCreateFood = () => {
    navigate('/nutrition/foods/new');
  };

  const handleEditFood = (foodId: string) => {
    navigate(`/nutrition/foods/${foodId}/edit`);
  };

  const handleDeleteFood = async (foodId: string) => {
    if (window.confirm('Are you sure you want to delete this food item?')) {
      await deleteFoodItem(foodId);
      loadFoodItems();
    }
  };

  const handleFoodDetail = (foodId: string) => {
    navigate(`/nutrition/foods/${foodId}`);
  };

  const handleScanBarcode = () => {
    setShowBarcodeScanner(true);
  };

  const handleBarcodeScanComplete = (foodItem: FoodItem) => {
    setShowBarcodeScanner(false);
    navigate(`/nutrition/foods/${foodItem.id}`);
  };

  const totalPages = Math.ceil(totalFoodItems / itemsPerPage);

  return (
    <div className="container mx-auto p-4">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
        <h1 className="text-2xl font-bold mb-4 md:mb-0">My Food Items</h1>
        <div className="flex space-x-2">
          <button
            onClick={handleCreateFood}
            className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md"
          >
            Add Food Item
          </button>
          <button
            onClick={handleScanBarcode}
            className="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-md"
          >
            Scan Barcode
          </button>
        </div>
      </div>

      <div className="mb-6">
        <div className="flex flex-col md:flex-row space-y-3 md:space-y-0 md:space-x-3">
          <div className="flex-1">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search food items..."
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setShowFavorites(!showFavorites)}
              className={`px-3 py-2 border rounded-md ${
                showFavorites
                  ? 'bg-yellow-100 border-yellow-300 text-yellow-800'
                  : 'bg-white border-gray-300 text-gray-700'
              }`}
            >
              Favorites
            </button>
            <button
              onClick={() => setShowCustomOnly(!showCustomOnly)}
              className={`px-3 py-2 border rounded-md ${
                showCustomOnly
                  ? 'bg-blue-100 border-blue-300 text-blue-800'
                  : 'bg-white border-gray-300 text-gray-700'
              }`}
            >
              Custom Only
            </button>
          </div>
        </div>
      </div>

      {foodItemsLoading ? (
        <div className="flex justify-center items-center py-12">
          <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      ) : foodItemsError ? (
        <div className="bg-red-50 border-l-4 border-red-500 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{foodItemsError}</p>
            </div>
          </div>
        </div>
      ) : foodItems.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 className="mt-2 text-lg font-medium text-gray-900">No food items found</h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchQuery || showFavorites || showCustomOnly
              ? 'Try adjusting your search or filters'
              : 'Get started by adding your first food item'}
          </p>
          <div className="mt-6">
            <button
              onClick={handleCreateFood}
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Add Food Item
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {foodItems.map((foodItem) => (
              <FoodItemCard
                key={foodItem.id}
                foodItem={foodItem}
                onSelect={() => handleFoodDetail(foodItem.id)}
                onEdit={() => handleEditFood(foodItem.id)}
                onDelete={() => handleDeleteFood(foodItem.id)}
              />
            ))}
          </div>

          {totalPages > 1 && (
            <div className="flex justify-center mt-8">
              <nav className="flex items-center space-x-2">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-1 rounded-md border border-gray-300 disabled:opacity-50"
                >
                  Previous
                </button>
                <span className="text-sm text-gray-700">
                  Page {currentPage} of {totalPages}
                </span>
                <button
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1 rounded-md border border-gray-300 disabled:opacity-50"
                >
                  Next
                </button>
              </nav>
            </div>
          )}
        </>
      )}

      {showBarcodeScanner && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-lg w-full mx-4">
            <BarcodeScanner
              onScanComplete={handleBarcodeScanComplete}
              onCancel={() => setShowBarcodeScanner(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default FoodItems;