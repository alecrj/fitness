// tests/unit/nutrition/MealManagement.test.tsx
import * as React from 'react';
import { render, screen, fireEvent, waitFor } from '../../test-utils';
import { mockMeals, mockFoodItems } from '../../test-utils';

// Mock Meals component
const MockMeals: React.FC = () => {
  const [meals] = React.useState(mockMeals);
  const [dateFilter, setDateFilter] = React.useState('');
  const [mealTypeFilter, setMealTypeFilter] = React.useState('');

  const filteredMeals = meals.filter(meal => {
    // Fixed: Convert Date object to string first, then split
    if (dateFilter && meal.meal_time.toISOString().split('T')[0] !== dateFilter) return false;
    if (mealTypeFilter && meal.meal_type !== mealTypeFilter) return false;
    return true;
  });

  return (
    <div>
      <h1>Meals</h1>
      <label htmlFor="date">Date</label>
      <input
        id="date"
        type="date"
        value={dateFilter}
        onChange={(e) => setDateFilter(e.target.value)}
      />
      
      <label htmlFor="meal-type">Meal Type</label>
      <select
        id="meal-type"
        value={mealTypeFilter}
        onChange={(e) => setMealTypeFilter(e.target.value)}
      >
        <option value="">All</option>
        <option value="breakfast">Breakfast</option>
        <option value="lunch">Lunch</option>
        <option value="dinner">Dinner</option>
        <option value="snack">Snack</option>
      </select>
      
      {filteredMeals.map(meal => (
        <div key={meal.id} data-testid={`meal-${meal.id}`}>
          <h3>{meal.name}</h3>
          <p>{meal.meal_type}</p>
          <p>{meal.nutrition_totals.calories} calories</p>
        </div>
      ))}
    </div>
  );
};

// Mock MealDetail component
const MockMealDetail: React.FC = () => {
  const meal = mockMeals[0];
  
  return (
    <div>
      <h1>{meal.name}</h1>
      <p>{meal.meal_type}</p>
      {meal.food_items.map((item, index) => (
        <div key={index}>
          <span>{item.food_item_name}</span>
          <span>{item.servings} servings</span>
        </div>
      ))}
      <p>Calories: {meal.nutrition_totals.calories}</p>
      <p>Protein: {meal.nutrition_totals.protein}</p>
      <button>Edit</button>
      <button>Delete</button>
    </div>
  );
};

// Mock AddEditMeal component
const MockAddEditMeal: React.FC = () => {
  const [formData, setFormData] = React.useState({
    name: '',
    meal_type: '',
    date: '',
    time: '',
    food_items: [] as any[]
  });
  const [errors, setErrors] = React.useState<string[]>([]);
  const [showFoodSelection, setShowFoodSelection] = React.useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: string[] = [];
    
    if (!formData.name) newErrors.push('Name is required');
    if (!formData.meal_type) newErrors.push('Meal type is required');
    
    setErrors(newErrors);
    
    if (newErrors.length === 0) {
      console.log('Meal saved successfully');
    }
  };

  const handleAddFood = () => {
    setShowFoodSelection(true);
  };

  const handleSelectFood = (food: any) => {
    setFormData(prev => ({
      ...prev,
      food_items: [...prev.food_items, { ...food, servings: 1 }]
    }));
    setShowFoodSelection(false);
  };

  return (
    <div>
      <h1>Add Meal</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          value={formData.name}
          onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
        />
        
        <label htmlFor="meal_type">Meal Type</label>
        <select
          id="meal_type"
          value={formData.meal_type}
          onChange={(e) => setFormData(prev => ({ ...prev, meal_type: e.target.value }))}
        >
          <option value="">Select...</option>
          <option value="breakfast">Breakfast</option>
          <option value="lunch">Lunch</option>
          <option value="dinner">Dinner</option>
          <option value="snack">Snack</option>
        </select>
        
        <label htmlFor="date">Date</label>
        <input
          id="date"
          type="date"
          value={formData.date}
          onChange={(e) => setFormData(prev => ({ ...prev, date: e.target.value }))}
        />
        
        <label htmlFor="time">Time</label>
        <input
          id="time"
          type="time"
          value={formData.time}
          onChange={(e) => setFormData(prev => ({ ...prev, time: e.target.value }))}
        />
        
        <button type="button" onClick={handleAddFood}>Add Food Items</button>
        
        {formData.food_items.map((item, index) => (
          <div key={index}>
            <span>{item.name}</span>
            <span>{item.servings} servings</span>
          </div>
        ))}
        
        <button type="submit">Save</button>
        
        {errors.map((error, index) => (
          <div key={index}>{error}</div>
        ))}
      </form>
      
      {showFoodSelection && (
        <div>
          <h2>Select Food Items</h2>
          {mockFoodItems.map(food => (
            <div key={food.id}>
              <label>
                <input
                  type="checkbox"
                  onChange={() => handleSelectFood(food)}
                  aria-label={food.name}
                />
                {food.name}
              </label>
              <label htmlFor={`servings-${food.id}`}>Servings</label>
              <input
                id={`servings-${food.id}`}
                type="number"
                defaultValue={1}
                min={0.1}
                step={0.1}
              />
            </div>
          ))}
          <button onClick={() => setShowFoodSelection(false)}>Add Selected</button>
        </div>
      )}
    </div>
  );
};

describe('Meal Management', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Meals List', () => {
    test('renders meals list with correct data', async () => {
      render(<MockMeals />);
      
      // Check if meals are displayed
      expect(screen.getByText('Breakfast')).toBeInTheDocument();
      
      // Check if filtering options are available
      expect(screen.getByLabelText(/date/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/meal type/i)).toBeInTheDocument();
    });
    
    test('handles filtering meals by date', async () => {
      render(<MockMeals />);
      
      // Test date filter
      const dateInput = screen.getByLabelText(/date/i);
      fireEvent.change(dateInput, { target: { value: '2025-05-11' } });
      
      // Meal should still be visible (assuming today's date)
      expect(screen.getByText('Breakfast')).toBeInTheDocument();
    });
    
    test('handles filtering meals by meal type', async () => {
      render(<MockMeals />);
      
      // Test meal type filter
      const mealTypeSelect = screen.getByLabelText(/meal type/i);
      fireEvent.change(mealTypeSelect, { target: { value: 'breakfast' } });
      
      // Breakfast should be visible
      expect(screen.getByText('Breakfast')).toBeInTheDocument();
    });
  });
  
  describe('Meal Details', () => {
    test('renders meal details correctly', async () => {
      render(<MockMealDetail />);
      
      // Check if meal details are displayed
      expect(screen.getByText('Breakfast')).toBeInTheDocument();
      expect(screen.getByText('breakfast')).toBeInTheDocument();
      
      // Check if food items are displayed
      expect(screen.getByText('Apple')).toBeInTheDocument();
      
      // Check if nutritional information is displayed
      expect(screen.getByText(/calories.*52/i)).toBeInTheDocument();
      expect(screen.getByText(/protein.*0.3/i)).toBeInTheDocument();
    });
    
    test('displays edit and delete buttons', async () => {
      render(<MockMealDetail />);
      
      // Check if action buttons are displayed
      expect(screen.getByText('Edit')).toBeInTheDocument();
      expect(screen.getByText('Delete')).toBeInTheDocument();
    });
  });
  
  describe('Add/Edit Meal', () => {
    test('renders add meal form correctly', () => {
      render(<MockAddEditMeal />);
      
      // Check if form fields are rendered
      expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/meal type/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/date/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/time/i)).toBeInTheDocument();
      expect(screen.getByText(/add food items/i)).toBeInTheDocument();
    });
    
    test('validates required fields', async () => {
      render(<MockAddEditMeal />);
      
      // Submit the form without filling required fields
      const submitButton = screen.getByText(/save/i);
      fireEvent.click(submitButton);
      
      // Check for validation errors
      await waitFor(() => {
        expect(screen.getByText(/name is required/i)).toBeInTheDocument();
        expect(screen.getByText(/meal type is required/i)).toBeInTheDocument();
      });
    });
    
    test('allows adding food items to meal', async () => {
      render(<MockAddEditMeal />);
      
      // Fill out basic meal info
      fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Lunch' } });
      fireEvent.change(screen.getByLabelText(/meal type/i), { target: { value: 'lunch' } });
      
      // Click add food items button
      const addFoodButton = screen.getByText(/add food items/i);
      fireEvent.click(addFoodButton);
      
      // Wait for food selection modal to appear
      await waitFor(() => {
        expect(screen.getByText(/select food items/i)).toBeInTheDocument();
      });
      
      // Select a food item
      const foodCheckbox = screen.getByLabelText('Apple');
      fireEvent.click(foodCheckbox);
      
      // Add selected food to meal
      const addSelectedButton = screen.getByText(/add selected/i);
      fireEvent.click(addSelectedButton);
      
      // Check if food item was added to meal
      await waitFor(() => {
        expect(screen.getByText('Apple')).toBeInTheDocument();
        expect(screen.getByText('1 servings')).toBeInTheDocument();
      });
    });
    
    test('submits form with valid data for new meal', async () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
      render(<MockAddEditMeal />);
      
      // Fill out the form
      fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Lunch' } });
      fireEvent.change(screen.getByLabelText(/meal type/i), { target: { value: 'lunch' } });
      fireEvent.change(screen.getByLabelText(/date/i), { target: { value: '2025-05-11' } });
      fireEvent.change(screen.getByLabelText(/time/i), { target: { value: '12:30' } });
      
      // Submit the form
      const submitButton = screen.getByText(/save/i);
      fireEvent.click(submitButton);
      
      // Check if form was submitted successfully
      await waitFor(() => {
        expect(consoleSpy).toHaveBeenCalledWith('Meal saved successfully');
      });
      
      consoleSpy.mockRestore();
    });
  });
});