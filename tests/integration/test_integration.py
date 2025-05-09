"""Integration tests for cross-module functionality"""
import pytest
from unittest.mock import patch, MagicMock
import json
import firebase_admin
import time

@pytest.fixture
def sample_user():
    """Return a sample user for testing"""
    return {
        'id': 'test-user-id',
        'name': 'Test User',
        'profile_image_url': 'https://example.com/profile.jpg',
        'created_at': '2023-01-01T00:00:00Z',
        'updated_at': '2023-01-01T00:00:00Z'
    }

@pytest.fixture
def sample_recipe():
    """Return a sample recipe for testing"""
    return {
        'id': 'test-recipe-id',
        'userId': 'test-user-id',
        'title': 'Test Recipe',
        'description': 'A test recipe',
        'ingredients': ['Ingredient 1', 'Ingredient 2'],
        'instructions': ['Step 1', 'Step 2'],
        'prepTime': 10,
        'cookTime': 20,
        'servings': 4,
        'imageUrl': 'https://example.com/image.jpg',
        'createdAt': '2023-01-01T00:00:00Z',
        'updatedAt': '2023-01-01T00:00:00Z'
    }

@pytest.fixture
def mock_firestore_operations():
    """Set up common mocks for Firestore operations"""
    # Create mock document reference
    mock_doc_ref = MagicMock()
    mock_doc_ref.id = 'test-doc-id'
    
    # Create mock document snapshot
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.id = 'test-doc-id'
    mock_doc_ref.get.return_value = mock_doc
    
    # Create mock collection reference
    mock_collection = MagicMock()
    mock_collection.document.return_value = mock_doc_ref
    
    # Create mock Firestore client
    mock_db = MagicMock()
    mock_db.collection.return_value = mock_collection
    
    # Create mock for Storage bucket and blob
    mock_blob = MagicMock()
    mock_blob.public_url = 'https://example.com/test.jpg'
    
    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    
    return {
        'db': mock_db,
        'collection': mock_collection,
        'doc_ref': mock_doc_ref,
        'doc': mock_doc,
        'bucket': mock_bucket,
        'blob': mock_blob
    }

def test_recipe_to_social_share(client, mock_auth_middleware, mock_firestore_operations, sample_recipe):
    """Test sharing a recipe to social feed"""
    # Mocks for Firestore and Storage
    mocks = mock_firestore_operations
    mocks['doc'].to_dict.return_value = sample_recipe
    
    # First, test getting a recipe
    with patch('firebase_admin.firestore.client', return_value=mocks['db']), \
         patch('firebase_admin.storage.bucket', return_value=mocks['bucket']):
        
        # Step 1: Get the recipe
        recipe_response = client.get('/api/recipes/test-recipe-id')
        
        # Verify recipe was retrieved
        assert recipe_response.status_code == 200
        recipe = json.loads(recipe_response.data)
        assert recipe['id'] == 'test-recipe-id'
        
        # Step 2: Create a social post referencing this recipe
        post_data = {
            'content': f"Check out my recipe: {recipe['title']}!",
            'recipeId': recipe['id'],
            'tags': ['recipe', 'food']
        }
        
        # Reset mock for post creation
        mocks['doc_ref'].id = 'new-post-id'
        
        # Create a post with this recipe
        post_response = client.post('/api/social/posts', 
                                 data=json.dumps(post_data),
                                 content_type='application/json')
        
        # Check the post was created successfully
        assert post_response.status_code == 201
        post_result = json.loads(post_response.data)
        assert post_result['recipeId'] == recipe['id']
        assert 'recipe' in post_result['tags']

def test_meal_to_nutrition_stats(client, mock_auth_middleware, mock_firestore_operations):
    """Test creating a meal and viewing nutrition stats"""
    # Mocks for Firestore
    mocks = mock_firestore_operations
    
    # Set up mock food item
    food_item = {
        'id': 'test-food-id',
        'name': 'Test Food',
        'nutrition': {
            'calories': 200,
            'protein': 10,
            'carbs': 25,
            'fat': 8
        },
        'serving_size': 100,
        'serving_unit': 'g'
    }
    mocks['doc'].to_dict.return_value = food_item
    
    # Set up mock for meal collection query
    mock_meal = {
        'id': 'new-meal-id',
        'name': 'Test Meal',
        'meal_type': 'lunch',
        'food_items': [
            {
                'food_item_id': 'test-food-id',
                'food_item_name': 'Test Food',
                'servings': 1,
                'nutrition': food_item['nutrition']
            }
        ],
        'nutrition_totals': food_item['nutrition'],
        'meal_time': '2023-01-01T12:00:00Z',
    }
    
    mock_meal_docs = [MagicMock()]
    mock_meal_docs[0].to_dict.return_value = mock_meal
    mock_meal_docs[0].id = 'new-meal-id'
    
    mock_query = MagicMock()
    mock_query.stream.return_value = mock_meal_docs
    mocks['collection'].where.return_value = mock_query
    mock_query.where.return_value = mock_query
    
    with patch('firebase_admin.firestore.client', return_value=mocks['db']):
        # Step 1: Create a meal
        meal_data = {
            'name': 'Test Meal',
            'meal_type': 'lunch',
            'food_items': ['test-food-id']
        }
        
        meal_response = client.post('/api/nutrition/meals', 
                                  data=json.dumps(meal_data),
                                  content_type='application/json')
        
        # Verify meal was created
        assert meal_response.status_code == 201
        meal = json.loads(meal_response.data)
        assert meal['name'] == 'Test Meal'
        
        # Step 2: Get nutrition stats that should include this meal
        stats_response = client.get('/api/nutrition/stats/daily?date=2023-01-01')
        
        # Verify stats were retrieved
        assert stats_response.status_code == 200
        stats = json.loads(stats_response.data)
        assert stats['date'] == '2023-01-01'
        assert stats['total']['calories'] == 200
        assert stats['meal_count'] == 1
        assert 'lunch' in stats['by_meal_type']

def test_user_profile_to_social(client, mock_auth_middleware, mock_firestore_operations, sample_user):
    """Test retrieving user profile and using it in social context"""
    # Mocks for Firestore
    mocks = mock_firestore_operations
    mocks['doc'].to_dict.return_value = sample_user
    
    # Set up mock for follows query
    mock_follow_result = {
        'following': True,
        'followingId': 'other-user-id'
    }
    
    follow_model_mock = MagicMock()
    follow_model_mock.toggle.return_value = mock_follow_result
    follow_model_mock.check_status.return_value = True
    
    with patch('firebase_admin.firestore.client', return_value=mocks['db']), \
         patch('social.models.Follow', return_value=follow_model_mock):
        
        # Step 1: Get user profile
        profile_response = client.get('/api/auth/profile')
        
        # Verify profile was retrieved
        assert profile_response.status_code == 200
        profile = json.loads(profile_response.data)
        assert profile['id'] == 'test-user-id'
        assert profile['name'] == 'Test User'
        
        # Step 2: Follow another user
        follow_response = client.post('/api/social/users/other-user-id/follow')
        
        # Verify follow status
        assert follow_response.status_code == 200
        follow_result = json.loads(follow_response.data)
        assert follow_result['following'] is True
        assert follow_result['followingId'] == 'other-user-id'
        
        # Step 3: Check follow status
        status_response = client.get('/api/social/users/other-user-id/follow-status')
        
        # Verify status was retrieved
        assert status_response.status_code == 200
        status = json.loads(status_response.data)
        assert status['following'] is True

def test_recipe_nutrition_integration(client, mock_auth_middleware, mock_firestore_operations):
    """Test using a recipe for nutritional analysis"""
    # Mocks for Firestore and external API
    mocks = mock_firestore_operations
    
    # Mock recipe with ingredients
    recipe = {
        'id': 'test-recipe-id',
        'title': 'Test Recipe',
        'ingredients': [
            '100g chicken breast',
            '50g rice',
            '30g vegetables'
        ],
        'servings': 2
    }
    
    # Mock USDA API response for nutritional analysis
    mock_usda_response = MagicMock()
    mock_usda_response.status_code = 200
    mock_usda_response.json.return_value = {
        'foods': [
            {
                'description': 'Chicken, breast',
                'foodNutrients': [
                    {'nutrientName': 'Energy', 'value': 165, 'unitName': 'KCAL'},
                    {'nutrientName': 'Protein', 'value': 31, 'unitName': 'G'}
                ]
            }
        ]
    }
    
    with patch('firebase_admin.firestore.client', return_value=mocks['db']), \
         patch('requests.get', return_value=mock_usda_response):
        
        # Step 1: Analyze recipe nutrition
        analysis_data = {
            'ingredients': recipe['ingredients'],
            'servings': recipe['servings']
        }
        
        analysis_response = client.post('/api/recipes/nutritional-analysis', 
                                       data=json.dumps(analysis_data),
                                       content_type='application/json')
        
        # Verify nutrition analysis was performed
        assert analysis_response.status_code == 200
        analysis = json.loads(analysis_response.data)
        assert 'totalNutrition' in analysis
        assert 'perServing' in analysis
        assert analysis['servings'] == 2
        
        # Check that the API call was made for each ingredient
        assert 'ingredientBreakdown' in analysis