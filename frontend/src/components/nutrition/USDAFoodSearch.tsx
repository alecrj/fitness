import React, { useState } from 'react';
import { USDAFoodSearchResult, USDAFoodDetail } from '../../types/nutrition';
import { useNutrition } from '../../contexts/NutritionContext';

interface USDAFoodSearchProps {
  onImport: () => void;
}

const USDAFoodSearch: React.FC<USDAFoodSearchProps> = ({ onImport }) => {
  const { 
    searchUSDAFoods, 
    usdaSearchResults, 
    usdaSearchLoading, 
    usdaSearchError,
    getUSDAFoodDetails,
    importUSDAFood
  } = useNutrition();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFood, setSelectedFood] = useState<USDAFoodSearchResult | null>(null);
  const [foodDetails, setFoodDetails] = useState<USDAFoodDetail | null>(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [servingSize, setServingSize] = useState(100);
  const [servingUnit, setServingUnit] = useState('g');
  const [importLoading, setImportLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      await searchUSDAFoods(searchQuery);
    }
  };

  const handleFoodSelect = async (food: USDAFoodSearchResult) => {
    setSelectedFood(food);
    setDetailsLoading(true);
    
    try {
      const details = await getUSDAFoodDetails(food.fdcId);
      if (details) {
        setFoodDetails(details);
        
        // Set serving size and unit from details if available
        if (details.servingSize) {
          setServingSize(details.servingSize);
        }
        if (details.servingSizeUnit) {
          setServingUnit(details.servingSizeUnit);
        }
      }
    } catch (error) {
      console.error('Error fetching food details:', error);
    } finally {
      setDetailsLoading(false);
    }
  };

  const handleImport = async () => {
    if (!selectedFood) return;
    
    setImportLoading(true);
    
    try {
      await importUSDAFood(selectedFood.fdcId, servingSize, servingUnit);
      onImport();
    } catch (error) {
      console.error('Error importing food:', error);
    } finally {
      setImportLoading(false);
    }
  };

  const getNutrientValue = (nutrientName: string): string => {
    if (!foodDetails || !foodDetails.foodNutrients) return 'N/A';
    
    const nutrient = foodDetails.foodNutrients.find(
      n => n.nutrientName.toLowerCase() === nutrientName.toLowerCase()
    );
    
    return nutrient ? `${nutrient.value} ${nutrient.unitName}` : 'N/A';
  };

  return (
    <div>
      <h2 className="text-lg font-medium mb-4">Search USDA Food Database</h2>
      
      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for foods..."
            className="flex-1 border rounded-md px-3 py-2"
            required
          />
          <button
            type="submit"
            disabled={usdaSearchLoading}
            className="bg-blue-600 text-white px-4 py-2 rounded-md disabled:bg-blue-400"
          >
            {usdaSearchLoading ? 'Searching...' : 'Search'}
          </button>
        </div>
        {usdaSearchError && (
          <p className="text-red-500 text-sm mt-2">{usdaSearchError}</p>
        )}
      </form>

      <div className="grid md:grid-cols-2 gap-4">
        {/* Search results */}
        <div className="border rounded-lg p-4">
          <h3 className="font-medium mb-2">Search Results</h3>
          
          {usdaSearchLoading ? (
            <p className="text-gray-500">Loading results...</p>
          ) : usdaSearchResults && usdaSearchResults.foods.length > 0 ? (
            <div className="max-h-96 overflow-y-auto">
              <ul className="divide-y">
                {usdaSearchResults.foods.map((food) => (
                  <li 
                    key={food.fdcId}
                    className={`py-2 cursor-pointer hover:bg-gray-100 ${selectedFood?.fdcId === food.fdcId ? 'bg-blue-50' : ''}`}
                    onClick={() => handleFoodSelect(food)}
                  >
                    <p className="font-medium">{food.description}</p>
                    {food.brandOwner && (
                      <p className="text-sm text-gray-600">{food.brandOwner}</p>
                    )}
                    {food.foodCategory && (
                      <p className="text-xs text-gray-500">{food.foodCategory}</p>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ) : usdaSearchResults ? (
            <p className="text-gray-500">No results found. Try a different search term.</p>
          ) : (
            <p className="text-gray-500">Search for foods to see results.</p>
          )}
        </div>

        {/* Food details and import */}
        <div className="border rounded-lg p-4">
          <h3 className="font-medium mb-2">Food Details</h3>
          
          {detailsLoading ? (
            <p className="text-gray-500">Loading details...</p>
          ) : selectedFood && foodDetails ? (
            <div>
              <h4 className="text-lg font-medium">{foodDetails.description}</h4>
              
              {foodDetails.brandOwner && (
                <p className="text-sm text-gray-600 mb-3">{foodDetails.brandOwner}</p>
              )}
              
              <div className="mb-4">
                <h5 className="font-medium text-sm">Nutrition Information</h5>
                <div className="grid grid-cols-2 gap-x-4 gap-y-1 mt-1">
                  <div className="text-sm">Calories: {getNutrientValue('Energy')}</div>
                  <div className="text-sm">Protein: {getNutrientValue('Protein')}</div>
                  <div className="text-sm">Carbs: {getNutrientValue('Carbohydrate, by difference')}</div>
                  <div className="text-sm">Fat: {getNutrientValue('Total lipid (fat)')}</div>
                  <div className="text-sm">Fiber: {getNutrientValue('Fiber, total dietary')}</div>
                  <div className="text-sm">Sugar: {getNutrientValue('Sugars, total including NLEA')}</div>
                </div>
              </div>
              
              <div className="mb-4">
                <h5 className="font-medium text-sm mb-2">Adjust Serving Size</h5>
                <div className="flex gap-2">
                  <div className="flex-1">
                    <input
                      type="number"
                      min="0"
                      step="0.1"
                      value={servingSize}
                      onChange={(e) => setServingSize(parseFloat(e.target.value) || 0)}
                      className="w-full border rounded-md px-3 py-2"
                    />
                  </div>
                  <div className="flex-1">
                    <select
                      value={servingUnit}
                      onChange={(e) => setServingUnit(e.target.value)}
                      className="w-full border rounded-md px-3 py-2"
                    >
                      <option value="g">grams (g)</option>
                      <option value="ml">milliliters (ml)</option>
                      <option value="oz">ounces (oz)</option>
                      <option value="cup">cup</option>
                      <option value="tbsp">tablespoon</option>
                      <option value="tsp">teaspoon</option>
                      <option value="serving">serving</option>
                    </select>
                  </div>
                </div>
              </div>
              
              <button
                onClick={handleImport}
                disabled={importLoading}
                className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:bg-green-400"
              >
                {importLoading ? 'Importing...' : 'Import Food Item'}
              </button>
            </div>
          ) : (
            <p className="text-gray-500">Select a food from the search results to see details.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default USDAFoodSearch;