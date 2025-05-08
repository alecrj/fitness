import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime
import sys
import os

# Add the parent directory to the path so we can import our app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock firebase_admin before importing modules that use it
import firebase_admin
firebase_admin.initialize_app = MagicMock()
firebase_admin.get_app = MagicMock()
firebase_admin.delete_app = MagicMock()
firebase_admin.firestore = MagicMock()
firebase_admin.storage = MagicMock()
firebase_admin.auth = MagicMock()

# Now import our app modules
from nutrition.models import NutritionModel, FoodItem, MealLog


class TestNutritionModel(unittest.TestCase):
    """Test cases for the base NutritionModel class"""

    def test_validate_nutrition_data(self):
        """Test validation of nutrition data"""
        # Test with valid data
        data = {
            'calories': 200,
            'protein': 10,
            'carbs': 25,
            'fat': 8,
            'fiber': 3,
            'sugar': 5
        }
        result = NutritionModel.validate_nutrition_data(data)
        self.assertEqual(result['calories'], 200)
        self.assertEqual(result['protein'], 10)
        self.assertEqual(result['carbs'], 25)
        self.assertEqual(result['fat'], 8)
        self.assertEqual(result['fiber'], 3)
        self.assertEqual(result['sugar'], 5)

        # Test with string values that should be converted to numbers
        data = {
            'calories': '150',
            'protein': '8.5',
            'carbs': '20',
            'fat': '6'
        }
        result = NutritionModel.validate_nutrition_data(data)
        self.assertEqual(result['calories'], 150)
        self.assertEqual(result['protein'], 8.5)
        self.assertEqual(result['carbs'], 20)
        self.assertEqual(result['fat'], 6)

        # Test with negative values that should be converted to 0
        data = {
            'calories': -100,
            'protein': -5
        }
        result = NutritionModel.validate_nutrition_data(data)
        self.assertEqual(result['calories'], 0)
        self.assertEqual(result['protein'], 0)

        # Test with empty data - should set defaults
        data = {}
        result = NutritionModel.validate_nutrition_data(data)
        self.assertEqual(result['calories'], 0)
        self.assertEqual(result['protein'], 0)
        self.assertEqual(result['carbs'], 0)
        self.assertEqual(result['fat'], 0)

    def test_calculate_totals(self):
        """Test calculation of nutrition totals"""
        items = [
            {
                'nutrition': {
                    'calories': 200,
                    'protein': 10,
                    'carbs': 25,
                    'fat': 8,
                    'fiber': 3,
                    'sugar': 5
                }
            },
            {
                'nutrition': {
                    'calories': 300,
                    'protein': 15,
                    'carbs': 30,
                    'fat': 12,
                    'fiber': 4,
                    'sugar': 8
                }
            }
        ]
        result = NutritionModel.calculate_totals(items)
        self.assertEqual(result['calories'], 500)
        self.assertEqual(result['protein'], 25)
        self.assertEqual(result['carbs'], 55)
        self.assertEqual(result['fat'], 20)
        self.assertEqual(result['fiber'], 7)
        self.assertEqual(result['sugar'], 13)

        # Test with missing nutritional values
        items = [
            {
                'nutrition': {
                    'calories': 200,
                    'protein': 10
                }
            },
            {
                'nutrition': {
                    'calories': 300,
                    'carbs': 30
                }
            }
        ]
        result = NutritionModel.calculate_totals(items)
        self.assertEqual(result['calories'], 500)
        self.assertEqual(result['protein'], 10)
        self.assertEqual(result['carbs'], 30)
        self.assertEqual(result['fat'], 0)

        # Test with empty items
        items = []
        result = NutritionModel.calculate_totals(items)
        self.assertEqual(result['calories'], 0)
        self.assertEqual(result['protein'], 0)
        self.assertEqual(result['carbs'], 0)
        self.assertEqual(result['fat'], 0)

        # Test with items missing nutrition field
        items = [{'name': 'Test item'}]
        result = NutritionModel.calculate_totals(items)
        self.assertEqual(result['calories'], 0)
        self.assertEqual(result['protein'], 0)


class TestFoodItem(unittest.TestCase):
    """Test cases for the FoodItem model"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock Firestore client
        self.mock_db = MagicMock()
        
        # Mock collection and document references
        self.mock_collection = MagicMock()
        self.mock_doc_ref = MagicMock()
        self.mock_doc = MagicMock()
        
        # Set up the chain of mocks
        self.mock_db.collection.return_value = self.mock_collection
        self.mock_collection.document.return_value = self.mock_doc_ref
        self.mock_doc_ref.get.return_value = self.mock_doc
        
        # Initialize model with mock db
        self.food_item = FoodItem(self.mock_db)
        
        # Test data
        self.test_user_id = "test_user_123"
        self.test_food_data = {
            'name': 'Test Food',
            'brand': 'Test Brand',
            'serving_size': 100,
            'serving_unit': 'g',
            'nutrition': {
                'calories': 200,
                'protein': 10,
                'carbs': 25,
                'fat': 8
            }
        }
        self.test_food_id = "test_food_123"

    def test_create_food_item(self):
        """Test creating a new food item"""
        # Set up mock document ID
        self.mock_doc_ref.id = self.test_food_id
        
        # Test creation of food item
        food_item = self.food_item.create(self.test_user_id, self.test_food_data)
        
        # Verify Firestore was called correctly
        self.mock_db.collection.assert_called_with("food_items")
        self.mock_collection.document.assert_called_once()
        self.mock_doc_ref.set.assert_called_once()
        
        # Verify the returned food item has the right structure
        self.assertEqual(food_item['id'], self.test_food_id)
        self.assertEqual(food_item['name'], 'Test Food')
        self.assertEqual(food_item['brand'], 'Test Brand')
        self.assertEqual(food_item['userId'], self.test_user_id)
        self.assertEqual(food_item['nutrition']['calories'], 200)
        
    def test_create_food_item_validation_error(self):
        """Test validation error during food item creation"""
        # Test with missing required field
        invalid_data = {
            'brand': 'Test Brand',
            'nutrition': {
                'calories': 200
            }
        }
        
        # Verify validation error is raised
        with self.assertRaises(ValueError) as context:
            self.food_item.create(self.test_user_id, invalid_data)
        
        self.assertTrue('Food item name is required' in str(context.exception))
        
    def test_get_food_item(self):
        """Test getting a food item by ID"""
        # Mock the document data
        mock_food_data = self.test_food_data.copy()
        mock_food_data['userId'] = self.test_user_id
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_food_data
        self.mock_doc.id = self.test_food_id
        
        # Test getting the food item
        food_item = self.food_item.get(self.test_food_id, self.test_user_id)
        
        # Verify Firestore was called correctly
        self.mock_db.collection.assert_called_with("food_items")
        self.mock_collection.document.assert_called_with(self.test_food_id)
        self.mock_doc_ref.get.assert_called_once()
        
        # Verify the returned food item has the right structure
        self.assertEqual(food_item['id'], self.test_food_id)
        self.assertEqual(food_item['name'], 'Test Food')
        self.assertEqual(food_item['userId'], self.test_user_id)
        
    def test_get_nonexistent_food_item(self):
        """Test getting a food item that doesn't exist"""
        # Mock document doesn't exist
        self.mock_doc.exists = False
        
        # Verify ValueError is raised
        with self.assertRaises(ValueError) as context:
            self.food_item.get(self.test_food_id, self.test_user_id)
        
        self.assertTrue('Food item not found' in str(context.exception))
        
    def test_get_unauthorized_food_item(self):
        """Test unauthorized access to a food item"""
        # Mock the document data with a different user ID
        mock_food_data = self.test_food_data.copy()
        mock_food_data['userId'] = "different_user_id"
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_food_data
        
        # Verify ValueError is raised for unauthorized access
        with self.assertRaises(ValueError) as context:
            self.food_item.get(self.test_food_id, self.test_user_id)
        
        self.assertTrue('Unauthorized access' in str(context.exception))
        
    def test_update_food_item(self):
        """Test updating a food item"""
        # Mock the document data
        mock_food_data = self.test_food_data.copy()
        mock_food_data['userId'] = self.test_user_id
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_food_data
        
        # Update data
        update_data = {
            'name': 'Updated Food Name',
            'nutrition': {
                'calories': 250,
                'protein': 15
            }
        }
        
        # Test updating the food item
        updated_item = self.food_item.update(self.test_food_id, self.test_user_id, update_data)
        
        # Verify Firestore was called correctly
        self.mock_db.collection.assert_called_with("food_items")
        self.mock_collection.document.assert_called_with(self.test_food_id)
        self.mock_doc_ref.update.assert_called_once()
        
        # Verify the returned food item has the updated values
        self.assertEqual(updated_item['name'], 'Updated Food Name')
        self.assertEqual(updated_item['nutrition']['calories'], 250)
        self.assertEqual(updated_item['nutrition']['protein'], 15)
        # Original values should be preserved
        self.assertEqual(updated_item['brand'], 'Test Brand')
        
    def test_delete_food_item(self):
        """Test deleting a food item"""
        # Mock the document data
        mock_food_data = self.test_food_data.copy()
        mock_food_data['userId'] = self.test_user_id
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_food_data
        
        # Test deleting the food item
        result = self.food_item.delete(self.test_food_id, self.test_user_id)
        
        # Verify Firestore was called correctly
        self.mock_db.collection.assert_called_with("food_items")
        self.mock_collection.document.assert_called_with(self.test_food_id)
        self.mock_doc_ref.delete.assert_called_once()
        
        # Verify successful deletion
        self.assertTrue(result)


class TestMealLog(unittest.TestCase):
    """Test cases for the MealLog model"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock Firestore client
        self.mock_db = MagicMock()
        
        # Mock collection and document references
        self.mock_collection = MagicMock()
        self.mock_doc_ref = MagicMock()
        self.mock_doc = MagicMock()
        
        # Set up the chain of mocks
        self.mock_db.collection.return_value = self.mock_collection
        self.mock_collection.document.return_value = self.mock_doc_ref
        self.mock_doc_ref.get.return_value = self.mock_doc
        
        # Initialize model with mock db
        self.meal_log = MealLog(self.mock_db)
        
        # Mock the FoodItem model
        self.mock_food_item = MagicMock()
        self.meal_log.food_item = self.mock_food_item
        
        # Test data
        self.test_user_id = "test_user_123"
        self.test_meal_id = "test_meal_123"
        self.test_food_id_1 = "test_food_123"
        self.test_food_id_2 = "test_food_456"
        
        # Test meal data
        self.test_meal_data = {
            'name': 'Test Meal',
            'meal_type': 'lunch',
            'food_items': [
                self.test_food_id_1,
                {
                    'food_item_id': self.test_food_id_2,
                    'servings': 2
                }
            ]
        }
        
        # Mock food items
        self.mock_food_1 = {
            'id': self.test_food_id_1,
            'name': 'Test Food 1',
            'nutrition': {
                'calories': 200,
                'protein': 10,
                'carbs': 25,
                'fat': 8
            }
        }
        
        self.mock_food_2 = {
            'id': self.test_food_id_2,
            'name': 'Test Food 2',
            'nutrition': {
                'calories': 300,
                'protein': 15,
                'carbs': 30,
                'fat': 12
            }
        }

    @patch('firebase_admin.firestore.SERVER_TIMESTAMP')
    def test_create_meal(self, mock_timestamp):
        """Test creating a new meal log"""
        # Set up mock document ID
        self.mock_doc_ref.id = self.test_meal_id
        
        # Set up mock food item retrieval
        self.mock_food_item.get.side_effect = [self.mock_food_1, self.mock_food_2]
        
        # Test creation of meal
        meal = self.meal_log.create(self.test_user_id, self.test_meal_data)
        
        # Verify Firestore was called correctly
        self.mock_db.collection.assert_called_with("meals")
        self.mock_collection.document.assert_called_once()
        self.mock_doc_ref.set.assert_called_once()
        
        # Verify food items were retrieved
        self.assertEqual(self.mock_food_item.get.call_count, 2)
        
        # Verify the returned meal has the right structure
        self.assertEqual(meal['id'], self.test_meal_id)
        self.assertEqual(meal['name'], 'Test Meal')
        self.assertEqual(meal['meal_type'], 'lunch')
        self.assertEqual(meal['userId'], self.test_user_id)
        
        # Verify nutrition calculations
        self.assertEqual(meal['nutrition_totals']['calories'], 800)  # 200 + (300 * 2)
        self.assertEqual(meal['nutrition_totals']['protein'], 40)    # 10 + (15 * 2)
        self.assertEqual(meal['nutrition_totals']['carbs'], 85)      # 25 + (30 * 2)
        self.assertEqual(meal['nutrition_totals']['fat'], 32)        # 8 + (12 * 2)
        
    def test_create_meal_validation_error(self):
        """Test validation error during meal creation"""
        # Test with missing required fields
        invalid_data = {
            'food_items': [self.test_food_id_1]
        }
        
        # Verify validation error is raised
        with self.assertRaises(ValueError) as context:
            self.meal_log.create(self.test_user_id, invalid_data)
        
        self.assertTrue('Meal name is required' in str(context.exception))
        
        # Test with missing meal type
        invalid_data = {
            'name': 'Test Meal',
            'food_items': [self.test_food_id_1]
        }
        
        # Verify validation error is raised
        with self.assertRaises(ValueError) as context:
            self.meal_log.create(self.test_user_id, invalid_data)
        
        self.assertTrue('Meal type is required' in str(context.exception))
        
    def test_get_meal(self):
        """Test getting a meal by ID"""
        # Mock the document data
        mock_meal_data = {
            'userId': self.test_user_id,
            'name': 'Test Meal',
            'meal_type': 'lunch',
            'food_items': []
        }
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_meal_data
        self.mock_doc.id = self.test_meal_id
        
        # Test getting the meal
        meal = self.meal_log.get(self.test_meal_id, self.test_user_id)
        
        # Verify Firestore was called correctly
        self.mock_db.collection.assert_called_with("meals")
        self.mock_collection.document.assert_called_with(self.test_meal_id)
        self.mock_doc_ref.get.assert_called_once()
        
        # Verify the returned meal has the right structure
        self.assertEqual(meal['id'], self.test_meal_id)
        self.assertEqual(meal['name'], 'Test Meal')
        self.assertEqual(meal['userId'], self.test_user_id)
        
    def test_get_nonexistent_meal(self):
        """Test getting a meal that doesn't exist"""
        # Mock document doesn't exist
        self.mock_doc.exists = False
        
        # Verify ValueError is raised
        with self.assertRaises(ValueError) as context:
            self.meal_log.get(self.test_meal_id, self.test_user_id)
        
        self.assertTrue('Meal not found' in str(context.exception))
        
    def test_get_unauthorized_meal(self):
        """Test unauthorized access to a meal"""
        # Mock the document data with a different user ID
        mock_meal_data = {
            'userId': "different_user_id",
            'name': 'Test Meal',
            'meal_type': 'lunch'
        }
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_meal_data
        
        # Verify ValueError is raised for unauthorized access
        with self.assertRaises(ValueError) as context:
            self.meal_log.get(self.test_meal_id, self.test_user_id)
        
        self.assertTrue('Unauthorized access' in str(context.exception))
        
    @patch('firebase_admin.firestore.SERVER_TIMESTAMP')
    def test_update_meal(self, mock_timestamp):
        """Test updating a meal"""
        # Mock the document data
        mock_meal_data = {
            'userId': self.test_user_id,
            'name': 'Test Meal',
            'meal_type': 'lunch',
            'food_items': []
        }
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_meal_data
        
        # Update data
        update_data = {
            'name': 'Updated Meal Name',
            'notes': 'Test notes'
        }
        
        # Test updating the meal
        updated_meal = self.meal_log.update(self.test_meal_id, self.test_user_id, update_data)
        
        # Verify Firestore was called correctly
        self.mock_db.collection.assert_called_with("meals")
        self.mock_collection.document.assert_called_with(self.test_meal_id)
        self.mock_doc_ref.update.assert_called_once()
        
        # Verify the returned meal has the updated values
        self.assertEqual(updated_meal['name'], 'Updated Meal Name')
        self.assertEqual(updated_meal['notes'], 'Test notes')
        # Original values should be preserved
        self.assertEqual(updated_meal['meal_type'], 'lunch')
        
    def test_delete_meal(self):
        """Test deleting a meal"""
        # Mock the document data
        mock_meal_data = {
            'userId': self.test_user_id,
            'name': 'Test Meal',
            'meal_type': 'lunch'
        }
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_meal_data
        
        # Test deleting the meal
        result = self.meal_log.delete(self.test_meal_id, self.test_user_id)
        
        # Verify Firestore was called correctly
        self.mock_db.collection.assert_called_with("meals")
        self.mock_collection.document.assert_called_with(self.test_meal_id)
        self.mock_doc_ref.delete.assert_called_once()
        
        # Verify successful deletion
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()