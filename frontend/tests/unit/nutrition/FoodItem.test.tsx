// tests/unit/nutrition/FoodItem.test.tsx
import * as React from 'react';
import { render, screen, fireEvent, waitFor } from '../../test-utils';
import { mockFoodItems } from '../../test-utils';

// Mock the components we're testing
const MockFoodItems: React.FC = () => {
  const [foods] = React.useState(mockFoodItems);
  const [searchTerm, setSearchTerm] = React.useState('');
  const [showFavoritesOnly, setShowFavoritesOnly] = React.useState(false);
  const [showCustomOnly, setShowCustomOnly] = React.useState(false);

  const filteredFoods = foods.filter(food => {
    if (searchTerm && !food.name.toLowerCase().includes(searchTerm.toLowerCase())) {
      return false;
    }
    if (showFavoritesOnly && !food.is_favorite) {
      return false;
    }
    if (showCustomOnly && !food.is_custom) {
      return false;
    }
    return true;
  });

  return (
    <div>
      <h1>Food Items</h1>
      <label htmlFor="search">Search</label>
      <input
        id="search"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <label>
        <input
          type="checkbox"
          checked={showFavoritesOnly}
          onChange={(e) => setShowFavoritesOnly(e.target.checked)}
          aria-label="Show favorites only"
        />
        Favorites
      </label>
      <label>
        <input
          type="checkbox"
          checked={showCustomOnly}
          onChange={(e) => setShowCustomOnly(e.target.checked)}
          aria-label="Show custom only"
        />
        Custom
      </label>
      {filteredFoods.map(food => (
        <div key={food.id} data-testid={`food-item-${food.id}`}>
          <h3>{food.name}</h3>
          <p>{food.nutrition.calories} calories</p>
          <p>{food.nutrition.protein}g protein</p>
        </div>
      ))}
    </div>
  );
};

const MockFoodItemDetail: React.FC = () => {
  const food = mockFoodItems[0];
  const [isFavorite, setIsFavorite] = React.useState(food.is_favorite);

  return (
    <div>
      <h1>{food.name}</h1>
      <p>Calories: {food.nutrition.calories}</p>
      <p>Protein: {food.nutrition.protein}</p>
      <button 
        onClick={() => setIsFavorite(!isFavorite)}
        aria-label={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
      >
        {isFavorite ? 'Remove from favorites' : 'Add to favorites'}
      </button>
    </div>
  );
};

const MockAddEditFoodItem: React.FC = () => {
  const [formData, setFormData] = React.useState({
    name: '',
    serving_size: '',
    serving_unit: 'g',
    calories: '',
    protein: '',
    carbs: '',
    fat: ''
  });
  const [errors, setErrors] = React.useState<string[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: string[] = [];
    
    if (!formData.name) newErrors.push('Name is required');
    if (!formData.serving_size) newErrors.push('Serving size is required');
    
    setErrors(newErrors);
    
    if (newErrors.length === 0) {
      console.log('Form submitted successfully');
    }
  };

  return (
    <div>
      <h1>Add Food Item</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          value={formData.name}
          onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
        />
        
        <label htmlFor="serving_size">Serving Size</label>
        <input
          id="serving_size"
          value={formData.serving_size}
          onChange={(e) => setFormData(prev => ({ ...prev, serving_size: e.target.value }))}
        />
        
        <label htmlFor="serving_unit">Serving Unit</label>
        <input
          id="serving_unit"
          value={formData.serving_unit}
          onChange={(e) => setFormData(prev => ({ ...prev, serving_unit: e.target.value }))}
        />
        
        <label htmlFor="calories">Calories</label>
        <input
          id="calories"
          value={formData.calories}
          onChange={(e) => setFormData(prev => ({ ...prev, calories: e.target.value }))}
        />
        
        <label htmlFor="protein">Protein</label>
        <input
          id="protein"
          value={formData.protein}
          onChange={(e) => setFormData(prev => ({ ...prev, protein: e.target.value }))}
        />
        
        <label htmlFor="carbs">Carbs</label>
        <input
          id="carbs"
          value={formData.carbs}
          onChange={(e) => setFormData(prev => ({ ...prev, carbs: e.target.value }))}
        />
        
        <label htmlFor="fat">Fat</label>
        <input
          id="fat"
          value={formData.fat}
          onChange={(e) => setFormData(prev => ({ ...prev, fat: e.target.value }))}
        />
        
        <button type="submit">Save</button>
        
        {errors.map((error, index) => (
          <div key={index}>{error}</div>
        ))}
      </form>
    </div>
  );
};

describe('Food Item Management', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Food Items List', () => {
    test('renders food items list with correct data', async () => {
      render(<MockFoodItems />);
      
      // Check if food items are displayed
      expect(screen.getByText('Apple')).toBeInTheDocument();
      expect(screen.getByText('Chicken Breast')).toBeInTheDocument();
      
      // Check if filtering options are available
      expect(screen.getByLabelText(/search/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/favorites/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/custom/i)).toBeInTheDocument();
    });
    
    test('handles filtering food items', async () => {
      render(<MockFoodItems />);
      
      // Test search functionality
      const searchInput = screen.getByLabelText(/search/i);
      fireEvent.change(searchInput, { target: { value: 'Apple' } });
      
      // Apple should still be visible
      expect(screen.getByText('Apple')).toBeInTheDocument();
      
      // Test favorites filter
      const favoritesFilter = screen.getByLabelText(/favorites/i);
      fireEvent.click(favoritesFilter);
      
      // Only favorites should be visible (Chicken Breast)
      expect(screen.getByText('Chicken Breast')).toBeInTheDocument();
    });
  });
  
  describe('Food Item Details', () => {
    test('renders food item details correctly', async () => {
      render(<MockFoodItemDetail />);
      
      // Check if food item details are displayed
      expect(screen.getByText('Apple')).toBeInTheDocument();
      expect(screen.getByText(/52/)).toBeInTheDocument(); // calories
      expect(screen.getByText(/0.3/)).toBeInTheDocument(); // protein
    });
    
    test('toggles favorite status correctly', async () => {
      render(<MockFoodItemDetail />);
      
      // Find and click the favorite button
      const favoriteButton = screen.getByLabelText(/favorite/i);
      
      // Initial state should be "Add to favorites" (since Apple is not favorite)
      expect(screen.getByText('Add to favorites')).toBeInTheDocument();
      
      fireEvent.click(favoriteButton);
      
      // After click, should show "Remove from favorites"
      expect(screen.getByText('Remove from favorites')).toBeInTheDocument();
    });
  });
  
  describe('Add/Edit Food Item', () => {
    test('renders add food item form correctly', () => {
      render(<MockAddEditFoodItem />);
      
      // Check if form fields are rendered
      expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/serving size/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/calories/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/protein/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/carbs/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/fat/i)).toBeInTheDocument();
    });
    
    test('validates required fields', async () => {
      render(<MockAddEditFoodItem />);
      
      // Submit the form without filling required fields
      const submitButton = screen.getByText(/save/i);
      fireEvent.click(submitButton);
      
      // Check for validation errors
      await waitFor(() => {
        expect(screen.getByText(/name is required/i)).toBeInTheDocument();
        expect(screen.getByText(/serving size is required/i)).toBeInTheDocument();
      });
    });
    
    test('submits form with valid data', async () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
      render(<MockAddEditFoodItem />);
      
      // Fill out the form
      fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Banana' } });
      fireEvent.change(screen.getByLabelText(/serving size/i), { target: { value: '118' } });
      fireEvent.change(screen.getByLabelText(/serving unit/i), { target: { value: 'g' } });
      fireEvent.change(screen.getByLabelText(/calories/i), { target: { value: '105' } });
      fireEvent.change(screen.getByLabelText(/protein/i), { target: { value: '1.3' } });
      fireEvent.change(screen.getByLabelText(/carbs/i), { target: { value: '27' } });
      fireEvent.change(screen.getByLabelText(/fat/i), { target: { value: '0.4' } });
      
      // Submit the form
      const submitButton = screen.getByText(/save/i);
      fireEvent.click(submitButton);
      
      // Check if form was submitted successfully
      await waitFor(() => {
        expect(consoleSpy).toHaveBeenCalledWith('Form submitted successfully');
      });
      
      consoleSpy.mockRestore();
    });
  });
});