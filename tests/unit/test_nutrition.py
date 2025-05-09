"""Unit tests for nutrition module"""
import pytest
from unittest.mock import patch, MagicMock
import json
import firebase_admin
from flask import jsonify
import requests

# Import the nutrition blueprint
from nutrition.routes import nutrition_bp
from nutrition.models import FoodItem, MealLog

@pytest.fixture
def sample_food_item():
    """Return a sample food item for testing"""
    return {
        'id': 'test-food-id',
        'userId': 'test-user-id',
        'name': 'Test Food',
        'brand': 'Test Brand',
        'serving_size': 100,
        'serving_unit': 'g',
        'calories': 200,
        'protein': 10,
        'carbs': 25,
        'fat': 8,
        'nutrition': {
            'calories': 200,
            'protein': 10,
            'carbs': 25,
            'fat': 8,
            'fiber': 3,
            'sugar': 5
        },
        'is_custom': True,
        'is_favorite': False,
        'created_at': '2023-01-01T00:00:00Z',
        'updated_at': '2023-01-01T00:00:00Z'
    }

@pytest.fixture
def sample_meal():
    """Return a sample meal for testing"""
    return {
        'id': 'test-meal-id',
        'userId': 'test-user-id',
        'name': 'Test Meal',
        'meal_type': 'lunch',
        'meal_time': '2023-01-01T12:00:00Z',
        'food_items': [
            {
                'food_item_id': 'test-food-id',
                'food_item_name': 'Test Food',
                'servings': 1,
                'nutrition': {
                    'calories': 200,
                    'protein': 10,
                    'carbs': 25,
                    'fat': 8,
                    'fiber': 3,
                    'sugar': 5
                }
            }
        ],
        'nutrition_totals': {
            'calories': 200,
            'protein': 10,
            'carbs': 25,
            'fat': 8,
            'fiber': 3,
            'sugar': 5
        },
        'notes': 'Test meal notes',
        'created_at': '2023-01-01T12:00:00Z',
        'updated_at': '2023-01-01T12:00:00Z'
    }

def mock_food_collection(mock_db, items=None):
    """Set up mock food items collection with data"""
    items = items or []
    
    # Mock collection query methods for food items
    mock_collection = mock_db.collection.return_value
    mock_query = MagicMock()
    mock_collection.where.return_value = mock_query
    mock_query.where.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    
    # Create mock doc snapshots for query results
    mock_docs = []
    for i, item in enumerate(items):
        mock_doc = MagicMock()
        mock_doc.id = item.get('id', f'food-{i}')
        mock_doc.to_dict.return_value = item
        mock_docs.append(mock_doc)
    
    # Set up stream method to return docs
    mock_query.stream.return_value = mock_docs
    
    return mock_collection, mock_query, mock_docs

def mock_meal_collection(mock_db, meals=None):
    """Set up mock meals collection with data"""
    meals = meals or []
    
    # Mock collection query methods for meals
    mock_collection = mock_db.collection.return_value
    mock_query = MagicMock()
    mock_collection.where.return_value = mock_query
    mock_query.where.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    
    # Create mock doc snapshots for query results
    mock_docs = []
    for i, meal in enumerate(meals):
        mock_doc = MagicMock()
        mock_doc.id = meal.get('id', f'meal-{i}')
        mock_doc.to_dict.return_value = meal
        mock_docs.append(mock_doc)
    
    # Set up stream method to return docs
    mock_query.stream.return_value = mock_docs
    
    return mock_collection, mock_query, mock_docs

def test_create_food_item(client, mock_auth_middleware, mock_db):
    """Test creating a new food item"""
    # Set up mock document reference
    mock_doc_ref = mock_db.collection.return_value.document.return_value
    mock_doc_ref.id = 'new-food-id'
    
    # Test request data
    data = {
        'name': 'New Food Item',
        'brand': 'Test Brand',
        'serving_size': 100,
        'serving_unit': 'g',
        'nutrition': {
            'calories': 200,
            'protein': 10,
            'carbs': 25,
            'fat': 8,
            'fiber': 3,
            'sugar': 5
        }
    }
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.post('/api/nutrition/foods', 
                              data=json.dumps(data),
                              content_type='application/json')
        
        # Check status code
        assert response.status_code == 201
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['name'] == 'New Food Item'
        assert result['id'] == 'new-food-id'
        assert result['nutrition']['calories'] == 200
        assert result['nutrition']['protein'] == 10
        
        # Verify Firestore document was created
        mock_db.collection.assert_called_with('food_items')
        mock_db.collection().document.assert_called_once()
        mock_doc_ref.set.assert_called_once()

def test_get_food_items(client, mock_auth_middleware, mock_db, sample_food_item):
    """Test getting user's food items"""
    # Set up mock food items collection
    mock_collection, mock_query, mock_docs = mock_food_collection(
        mock_db, [sample_food_item]
    )
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/nutrition/foods')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'items' in result
        assert len(result['items']) == 1
        assert result['items'][0]['name'] == 'Test Food'
        assert result['items'][0]['id'] == 'test-food-id'
        
        # Verify Firestore query was called correctly
        mock_db.collection.assert_called_with('food_items')
        mock_collection.where.assert_called_once()
        mock_query.order_by.assert_called_once()
        mock_query.limit.assert_called_once()
        mock_query.offset.assert_called_once()
        mock_query.stream.assert_called_once()

def test_get_food_item_by_id(client, mock_auth_middleware, mock_db, sample_food_item):
    """Test getting a specific food item by ID"""
    # Set up mock food item document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_food_item
    mock_doc.id = 'test-food-id'
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/nutrition/foods/test-food-id')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['name'] == 'Test Food'
        assert result['id'] == 'test-food-id'
        assert result['nutrition']['calories'] == 200
        
        # Verify Firestore get was called
        mock_db.collection.assert_called_with('food_items')
        mock_db.collection().document.assert_called_with('test-food-id')
        mock_db.collection().document().get.assert_called_once()

def test_update_food_item(client, mock_auth_middleware, mock_db, sample_food_item):
    """Test updating a food item"""
    # Set up mock food item document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_food_item
    
    # Test request data (partial update)
    data = {
        'name': 'Updated Food Name',
        'nutrition': {
            'calories': 250,
            'protein': 12
        }
    }
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.put('/api/nutrition/foods/test-food-id', 
                              data=json.dumps(data),
                              content_type='application/json')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['name'] == 'Updated Food Name'
        assert result['nutrition']['calories'] == 250
        assert result['nutrition']['protein'] == 12
        assert result['id'] == 'test-food-id'
        
        # Original data should be preserved
        assert result['brand'] == 'Test Brand'
        assert result['nutrition']['carbs'] == 25
        
        # Verify Firestore document was updated
        mock_db.collection.assert_called_with('food_items')
        mock_db.collection().document.assert_called_with('test-food-id')
        mock_db.collection().document().update.assert_called_once()

def test_delete_food_item(client, mock_auth_middleware, mock_db, sample_food_item):
    """Test deleting a food item"""
    # Set up mock food item document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_food_item
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.delete('/api/nutrition/foods/test-food-id')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response message
        assert 'message' in result
        assert 'deleted successfully' in result['message']
        
        # Verify Firestore document was deleted
        mock_db.collection.assert_called_with('food_items')
        mock_db.collection().document.assert_called_with('test-food-id')
        mock_db.collection().document().delete.assert_called_once()

def test_favorite_food_item(client, mock_auth_middleware, mock_db, sample_food_item):
    """Test toggling favorite status for a food item"""
    # Set up mock food item document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_food_item
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.post('/api/nutrition/foods/test-food-id/favorite')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'is_favorite' in result
        assert result['is_favorite'] is True  # Should be toggled from false to true
        
        # Verify Firestore document was updated
        mock_db.collection.assert_called_with('food_items')
        mock_db.collection().document.assert_called_with('test-food-id')
        mock_db.collection().document().update.assert_called_once()

def test_search_food_database(client, mock_auth_middleware):
    """Test searching for food items in USDA database"""
    # Mock the USDA API response
    with patch('requests.get') as mock_get:
        # Set up mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'totalHits': 2,
            'foods': [
                {
                    'fdcId': 123456,
                    'description': 'Test USDA Food',
                    'brandName': 'USDA',
                    'foodNutrients': [
                        {'nutrientName': 'Energy', 'value': 100, 'unitName': 'KCAL'},
                        {'nutrientName': 'Protein', 'value': 5, 'unitName': 'G'},
                        {'nutrientName': 'Carbohydrate, by difference', 'value': 15, 'unitName': 'G'},
                        {'nutrientName': 'Total lipid (fat)', 'value': 2, 'unitName': 'G'}
                    ]
                },
                {
                    'fdcId': 789012,
                    'description': 'Another USDA Food',
                    'brandName': 'USDA',
                    'foodNutrients': [
                        {'nutrientName': 'Energy', 'value': 150, 'unitName': 'KCAL'}
                    ]
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Make the request
        response = client.get('/api/nutrition/foods/search?q=test')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'foods' in result
        assert len(result['foods']) == 2
        assert result['foods'][0]['name'] == 'Test USDA Food'
        assert result['foods'][0]['fdcId'] == 123456
        assert 'nutrition' in result['foods'][0]
        assert result['foods'][0]['nutrition']['calories'] == 100
        assert 'totalHits' in result
        
        # Verify API request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert 'api_key' in kwargs['params']
        assert kwargs['params']['query'] == 'test'

def test_food_details(client, mock_auth_middleware):
    """Test getting detailed food information from USDA database"""
    # Mock the USDA API response
    with patch('requests.get') as mock_get:
        # Set up mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'fdcId': 123456,
            'description': 'Detailed Food Data',
            'brandName': 'USDA',
            'ingredients': 'Ingredient list',
            'servingSize': 100,
            'servingSizeUnit': 'g',
            'foodCategory': {'description': 'Fruits'},
            'foodNutrients': [
                {'nutrient': {'id': 1008, 'name': 'Energy', 'unitName': 'kcal'}, 'amount': 100},
                {'nutrient': {'id': 1003, 'name': 'Protein', 'unitName': 'g'}, 'amount': 5},
                {'nutrient': {'id': 1005, 'name': 'Carbohydrate, by difference', 'unitName': 'g'}, 'amount': 15},
                {'nutrient': {'id': 1004, 'name': 'Total lipid (fat)', 'unitName': 'g'}, 'amount': 2}
            ]
        }
        mock_get.return_value = mock_response
        
        # Make the request
        response = client.get('/api/nutrition/foods/details/123456')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['fdcId'] == 123456
        assert result['name'] == 'Detailed Food Data'
        assert result['ingredients'] == 'Ingredient list'
        assert result['serving_size'] == 100
        assert result['serving_unit'] == 'g'
        assert result['category'] == 'Fruits'
        assert 'nutrition' in result
        assert result['nutrition']['calories'] == 100
        assert result['nutrition']['protein'] == 5
        assert len(result['nutrients']) == 4
        
        # Verify API request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert 'api_key' in kwargs['params']
        assert '123456' in args[0]

def test_import_food_from_usda(client, mock_auth_middleware, mock_db):
    """Test importing a food item from USDA database"""
    # Mock the USDA API response and Firestore
    with patch('requests.get') as mock_get, \
         patch('firebase_admin.firestore.client', return_value=mock_db):
        
        # Set up mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'fdcId': 123456,
            'description': 'Imported Food',
            'brandName': 'USDA',
            'servingSize': 100,
            'servingSizeUnit': 'g',
            'foodNutrients': [
                {'nutrient': {'id': 1008, 'name': 'Energy', 'unitName': 'kcal'}, 'amount': 100},
                {'nutrient': {'id': 1003, 'name': 'Protein', 'unitName': 'g'}, 'amount': 5},
                {'nutrient': {'id': 1005, 'name': 'Carbohydrate, by difference', 'unitName': 'g'}, 'amount': 15},
                {'nutrient': {'id': 1004, 'name': 'Total lipid (fat)', 'unitName': 'g'}, 'amount': 2}
            ]
        }
        mock_get.return_value = mock_response
        
        # Set up mock document reference
        mock_doc_ref = mock_db.collection.return_value.document.return_value
        mock_doc_ref.id = 'imported-food-id'
        
        # Test request data
        data = {
            'fdcId': 123456,
            'name': 'Custom Name', # Override default name
            'serving_size': 50 # Override default serving size
        }
        
        # Make the request
        response = client.post('/api/nutrition/foods/import', 
                              data=json.dumps(data),
                              content_type='application/json')
        
        # Check status code
        assert response.status_code == 201
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['name'] == 'Custom Name' # Custom name was used
        assert result['fdcId'] == 123456
        assert result['serving_size'] == 50 # Custom serving size was used
        assert result['nutrition']['calories'] == 100
        assert result['is_custom'] is False # Imported, not custom
        
        # Verify API request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert 'api_key' in kwargs['params']
        assert '123456' in args[0]
        
        # Verify Firestore document was created
        mock_db.collection.assert_called_with('food_items')
        mock_db.collection().document.assert_called_once()
        mock_doc_ref.set.assert_called_once()

def test_create_meal(client, mock_auth_middleware, mock_db, sample_food_item):
    """Test creating a new meal log"""
    # Set up mock document and food item
    mock_doc_ref = mock_db.collection.return_value.document.return_value
    mock_doc_ref.id = 'new-meal-id'
    
    # Set up mock food item retrieval
    food_doc = MagicMock()
    food_doc.exists = True
    food_doc.to_dict.return_value = sample_food_item
    food_doc.id = 'test-food-id'
    
    # Configure get to return food item
    mock_db.collection.return_value.document.return_value.get.return_value = food_doc
    
    # Test request data
    data = {
        'name': 'New Meal',
        'meal_type': 'dinner',
        'food_items': [
            'test-food-id',  # Simple reference
            {
                'food_item_id': 'test-food-id',
                'servings': 0.5
            }
        ],
        'notes': 'Test notes'
    }
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.post('/api/nutrition/meals', 
                              data=json.dumps(data),
                              content_type='application/json')
        
        # Check status code
        assert response.status_code == 201
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['name'] == 'New Meal'
        assert result['meal_type'] == 'dinner'
        assert result['id'] == 'new-meal-id'
        assert len(result['food_items']) == 2
        assert result['food_items'][0]['food_item_name'] == 'Test Food'
        assert result['food_items'][1]['servings'] == 0.5
        
        # Verify nutrition totals
        # First item with 1 serving + second with 0.5 servings = 1.5x nutrition
        assert result['nutrition_totals']['calories'] == 300  # 200 * 1.5
        assert result['nutrition_totals']['protein'] == 15    # 10 * 1.5
        
        # Verify Firestore calls
        assert mock_db.collection.call_count >= 2  # Called for both food_items and meals
        mock_doc_ref.set.assert_called_once()

def test_get_meals(client, mock_auth_middleware, mock_db, sample_meal):
    """Test getting user's meal logs"""
    # Set up mock meals collection
    mock_collection, mock_query, mock_docs = mock_meal_collection(
        mock_db, [sample_meal]
    )
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/nutrition/meals')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'meals' in result
        assert len(result['meals']) == 1
        assert result['meals'][0]['name'] == 'Test Meal'
        assert result['meals'][0]['id'] == 'test-meal-id'
        
        # Verify Firestore query was called correctly
        mock_db.collection.assert_called_with('meals')
        mock_collection.where.assert_called_once()
        mock_query.order_by.assert_called_once()
        mock_query.limit.assert_called_once()
        mock_query.offset.assert_called_once()
        mock_query.stream.assert_called_once()

def test_get_meal_by_id(client, mock_auth_middleware, mock_db, sample_meal):
    """Test getting a specific meal by ID"""
    # Set up mock meal document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_meal
    mock_doc.id = 'test-meal-id'
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/nutrition/meals/test-meal-id')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['name'] == 'Test Meal'
        assert result['id'] == 'test-meal-id'
        assert result['meal_type'] == 'lunch'
        assert len(result['food_items']) == 1
        
        # Verify Firestore get was called
        mock_db.collection.assert_called_with('meals')
        mock_db.collection().document.assert_called_with('test-meal-id')
        mock_db.collection().document().get.assert_called_once()

def test_daily_nutrition_stats(client, mock_auth_middleware, mock_db, sample_meal):
    """Test getting daily nutrition statistics"""
    # Set up mock meals collection
    mock_collection, mock_query, mock_docs = mock_meal_collection(
        mock_db, [sample_meal]
    )
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/nutrition/stats/daily?date=2023-01-01')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['date'] == '2023-01-01'
        assert result['total']['calories'] == 200
        assert result['total']['protein'] == 10
        assert result['meal_count'] == 1
        assert 'by_meal_type' in result
        assert 'lunch' in result['by_meal_type']
        assert result['by_meal_type']['lunch']['calories'] == 200
        assert 'macro_percentages' in result
        
        # Verify Firestore query was called correctly
        mock_db.collection.assert_called_with('meals')
        mock_collection.where.assert_called_once()
        mock_query.stream.assert_called_once()

def test_barcode_lookup(client, mock_auth_middleware, mock_db):
    """Test barcode lookup for food items"""
    # Mock the barcode lookup
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('requests.get') as mock_get:
        
        # Set up mock database query for barcode
        mock_barcode_item = {
            'id': 'barcode-food-id',
            'name': 'Barcode Food',
            'barcode': '12345678',
            'nutrition': {'calories': 150}
        }
        
        # Configure mock to return barcode food
        mock_docs = [MagicMock()]
        mock_docs[0].to_dict.return_value = mock_barcode_item
        mock_docs[0].id = 'barcode-food-id'
        
        # Make the query return our mock docs
        mock_query = MagicMock()
        mock_query.stream.return_value = mock_docs
        mock_db.collection.return_value.where.return_value.limit.return_value = mock_query
        
        # Make the request
        response = client.get('/api/nutrition/barcode/lookup?code=12345678')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'food' in result
        assert result['food']['name'] == 'Barcode Food'
        assert result['food']['id'] == 'barcode-food-id'
        assert result['source'] == 'database'
        
        # Verify Firestore query was called correctly
        mock_db.collection.assert_called_with('food_items')
        mock_db.collection().where.assert_called_once()
        mock_query.stream.assert_called_once()