import React, { useState, useEffect } from 'react';
import { FoodItem, FoodItemRequest, NutritionData } from '../../types/nutrition';

interface FoodItemFormProps {
  initialData?: FoodItem;
  onSubmit: (foodItem: FoodItemRequest) => void;
  onCancel: () => void;
  isSubmitting: boolean;
}

const FoodItemForm: React.FC<FoodItemFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
  isSubmitting
}) => {
  const [name, setName] = useState('');
  const [brand, setBrand] = useState('');
  const [barcode, setBarcode] = useState('');
  const [servingSize, setServingSize] = useState<number>(100);
  const [servingUnit, setServingUnit] = useState('g');
  const [nutrition, setNutrition] = useState<NutritionData>({
    calories: 0,
    protein: 0,
    carbs: 0,
    fat: 0,
    fiber: 0,
    sugar: 0,
    sodium: 0,
    cholesterol: 0
  });

  useEffect(() => {
    if (initialData) {
      setName(initialData.name);
      setBrand(initialData.brand || '');
      setBarcode(initialData.barcode || '');
      setServingSize(initialData.serving_size);
      setServingUnit(initialData.serving_unit);
      setNutrition({
        calories: initialData.nutrition.calories,
        protein: initialData.nutrition.protein,
        carbs: initialData.nutrition.carbs,
        fat: initialData.nutrition.fat,
        fiber: initialData.nutrition.fiber || 0,
        sugar: initialData.nutrition.sugar || 0,
        sodium: initialData.nutrition.sodium || 0,
        cholesterol: initialData.nutrition.cholesterol || 0
      });
    }
  }, [initialData]);

  const handleNutritionChange = (key: keyof NutritionData, value: string) => {
    const numValue = parseFloat(value) || 0;
    setNutrition(prev => ({
      ...prev,
      [key]: numValue
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const foodItemData: FoodItemRequest = {
      name,
      brand: brand || undefined,
      barcode: barcode || undefined,
      serving_size: servingSize,
      serving_unit: servingUnit,
      nutrition: {
        calories: nutrition.calories,
        protein: nutrition.protein,
        carbs: nutrition.carbs,
        fat: nutrition.fat,
        fiber: nutrition.fiber,
        sugar: nutrition.sugar,
        sodium: nutrition.sodium,
        cholesterol: nutrition.cholesterol
      },
      is_custom: true
    };
    
    onSubmit(foodItemData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Food Name*
        </label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          placeholder="e.g., Apple, Chicken Breast"
          required
        />
      </div>

      <div>
        <label htmlFor="brand" className="block text-sm font-medium text-gray-700">
          Brand (Optional)
        </label>
        <input
          type="text"
          id="brand"
          value={brand}
          onChange={(e) => setBrand(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          placeholder="e.g., Trader Joe's"
        />
      </div>

      <div>
        <label htmlFor="barcode" className="block text-sm font-medium text-gray-700">
          Barcode (Optional)
        </label>
        <input
          type="text"
          id="barcode"
          value={barcode}
          onChange={(e) => setBarcode(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          placeholder="e.g., 123456789012"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="servingSize" className="block text-sm font-medium text-gray-700">
            Serving Size*
          </label>
          <input
            type="number"
            id="servingSize"
            value={servingSize}
            onChange={(e) => setServingSize(parseFloat(e.target.value) || 0)}
            min="0"
            step="0.1"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            required
          />
        </div>
        <div>
          <label htmlFor="servingUnit" className="block text-sm font-medium text-gray-700">
            Serving Unit*
          </label>
          <select
            id="servingUnit"
            value={servingUnit}
            onChange={(e) => setServingUnit(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            required
          >
            <option value="g">grams (g)</option>
            <option value="ml">milliliters (ml)</option>
            <option value="oz">ounces (oz)</option>
            <option value="cup">cup</option>
            <option value="tbsp">tablespoon</option>
            <option value="tsp">teaspoon</option>
            <option value="serving">serving</option>
            <option value="piece">piece</option>
          </select>
        </div>
      </div>

      <div className="border-t border-gray-200 pt-4">
        <h3 className="text-lg font-medium leading-6 text-gray-900">Nutrition Information</h3>
        <p className="mt-1 text-sm text-gray-500">
          Enter nutrition information per serving.
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="calories" className="block text-sm font-medium text-gray-700">
            Calories*
          </label>
          <input
            type="number"
            id="calories"
            value={nutrition.calories}
            onChange={(e) => handleNutritionChange('calories', e.target.value)}
            min="0"
            step="1"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div>
          <label htmlFor="protein" className="block text-sm font-medium text-gray-700">
            Protein (g)*
          </label>
          <input
            type="number"
            id="protein"
            value={nutrition.protein}
            onChange={(e) => handleNutritionChange('protein', e.target.value)}
            min="0"
            step="0.1"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            required
          />
        </div>
        <div>
          <label htmlFor="carbs" className="block text-sm font-medium text-gray-700">
            Carbs (g)*
          </label>
          <input
            type="number"
            id="carbs"
            value={nutrition.carbs}
            onChange={(e) => handleNutritionChange('carbs', e.target.value)}
            min="0"
            step="0.1"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            required
          />
        </div>
        <div>
          <label htmlFor="fat" className="block text-sm font-medium text-gray-700">
            Fat (g)*
          </label>
          <input
            type="number"
            id="fat"
            value={nutrition.fat}
            onChange={(e) => handleNutritionChange('fat', e.target.value)}
            min="0"
            step="0.1"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="fiber" className="block text-sm font-medium text-gray-700">
            Fiber (g)
          </label>
          <input
            type="number"
            id="fiber"
            value={nutrition.fiber}
            onChange={(e) => handleNutritionChange('fiber', e.target.value)}
            min="0"
            step="0.1"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="sugar" className="block text-sm font-medium text-gray-700">
            Sugar (g)
          </label>
          <input
            type="number"
            id="sugar"
            value={nutrition.sugar}
            onChange={(e) => handleNutritionChange('sugar', e.target.value)}
            min="0"
            step="0.1"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="sodium" className="block text-sm font-medium text-gray-700">
            Sodium (mg)
          </label>
          <input
            type="number"
            id="sodium"
            value={nutrition.sodium}
            onChange={(e) => handleNutritionChange('sodium', e.target.value)}
            min="0"
            step="1"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="cholesterol" className="block text-sm font-medium text-gray-700">
            Cholesterol (mg)
          </label>
          <input
            type="number"
            id="cholesterol"
            value={nutrition.cholesterol}
            onChange={(e) => handleNutritionChange('cholesterol', e.target.value)}
            min="0"
            step="1"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          />
        </div>
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          disabled={isSubmitting}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Saving...' : initialData ? 'Update Food Item' : 'Create Food Item'}
        </button>
      </div>
    </form>
  );
};

export default FoodItemForm;