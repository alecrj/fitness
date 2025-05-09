"""Unit tests for recipe module"""
import pytest
from unittest.mock import patch, MagicMock
import json
import firebase_admin
from flask import jsonify
import requests

# Import the recipes blueprint
from recipes.routes import recipes_bp

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

def mock_recipe_collection(mock_db, recipes=None):
    """Set up mock recipes collection with data"""
    recipes = recipes or []
    
    # Mock collection query methods for recipes
    mock_collection = mock_db.collection.return_value
    mock_query = MagicMock()
    mock_collection.where.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    
    # Create mock doc snapshots for query results
    mock_docs = []
    for i, recipe in enumerate(recipes):
        mock_doc = MagicMock()
        mock_doc.id = recipe.get('id', f'recipe-{i}')
        mock_doc.to_dict.return_value = recipe
        mock_docs.append(mock_doc)
    
    # Set up stream method to return docs
    mock_query.stream.return_value = mock_docs
    
    return mock_collection, mock_query, mock_docs

def test_get_recipes(client, mock_auth_middleware, mock_db, sample_recipe):
    """Test getting user's recipes"""
    # Set up mock recipes collection
    mock_collection, mock_query, mock_docs = mock_recipe_collection(
        mock_db, [sample_recipe]
    )
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/recipes')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'recipes' in result
        assert len(result['recipes']) == 1
        assert result['recipes'][0]['title'] == 'Test Recipe'
        assert result['recipes'][0]['id'] == 'test-recipe-id'
        
        # Verify Firestore query was called correctly
        mock_db.collection.assert_called_with('recipes')
        mock_collection.where.assert_called_once()
        mock_query.order_by.assert_called_once()
        mock_query.limit.assert_called_once()
        mock_query.offset.assert_called_once()
        mock_query.stream.assert_called_once()

def test_get_recipe_by_id(client, mock_auth_middleware, mock_db, sample_recipe):
    """Test getting a specific recipe by ID"""
    # Set up mock recipe document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_recipe
    mock_doc.id = 'test-recipe-id'
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/recipes/test-recipe-id')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['title'] == 'Test Recipe'
        assert result['id'] == 'test-recipe-id'
        assert len(result['ingredients']) == 2
        assert len(result['instructions']) == 2
        
        # Verify Firestore get was called
        mock_db.collection.assert_called_with('recipes')
        mock_db.collection().document.assert_called_with('test-recipe-id')
        mock_db.collection().document().get.assert_called_once()

def test_create_recipe(client, mock_auth_middleware, mock_db):
    """Test creating a new recipe"""
    # Mock the Firestore client and storage bucket
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('firebase_admin.storage.bucket') as mock_bucket:
        
        # Mock storage blob for image upload
        mock_blob = MagicMock()
        mock_bucket.return_value.blob.return_value = mock_blob
        mock_blob.public_url = 'https://example.com/image.jpg'
        
        # Set up mock document reference
        mock_doc_ref = mock_db.collection.return_value.document.return_value
        mock_doc_ref.id = 'new-recipe-id'
        
        # Test request data
        data = {
            'title': 'New Recipe',
            'description': 'A new test recipe',
            'ingredients': ['Ingredient 1', 'Ingredient 2'],
            'instructions': ['Step 1', 'Step 2'],
            'prepTime': 10,
            'cookTime': 20,
            'servings': 4,
            'imageBase64': 'SGVsbG8gV29ybGQ='  # Base64 for "Hello World"
        }
        
        # Make the request
        response = client.post('/api/recipes', 
                              data=json.dumps(data),
                              content_type='application/json')
        
        # Check status code
        assert response.status_code == 201
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['title'] == 'New Recipe'
        assert result['id'] == 'new-recipe-id'
        assert len(result['ingredients']) == 2
        assert len(result['instructions']) == 2
        
        # Verify Firestore document was created
        mock_db.collection.assert_called_with('recipes')
        mock_db.collection().document.assert_called_once()
        mock_doc_ref.set.assert_called_once()
        
        # Verify image was uploaded if base64 was provided
        mock_bucket.return_value.blob.assert_called_once()
        mock_blob.upload_from_string.assert_called_once()

def test_update_recipe(client, mock_auth_middleware, mock_db, sample_recipe):
    """Test updating an existing recipe"""
    # Set up mock recipe document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_recipe
    
    # Mock the Firestore client and storage bucket
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('firebase_admin.storage.bucket') as mock_bucket:
        
        # Test request data (partial update)
        data = {
            'title': 'Updated Recipe Title',
            'instructions': ['New Step 1', 'New Step 2', 'New Step 3']
        }
        
        # Make the request
        response = client.put('/api/recipes/test-recipe-id', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['title'] == 'Updated Recipe Title'
        assert len(result['instructions']) == 3
        assert result['id'] == 'test-recipe-id'
        
        # Original data should be preserved
        assert result['description'] == 'A test recipe'
        assert len(result['ingredients']) == 2
        
        # Verify Firestore document was updated
        mock_db.collection.assert_called_with('recipes')
        mock_db.collection().document.assert_called_with('test-recipe-id')
        mock_db.collection().document().update.assert_called_once()

def test_delete_recipe(client, mock_auth_middleware, mock_db, sample_recipe):
    """Test deleting a recipe"""
    # Set up mock recipe document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_recipe
    
    # Mock the Firestore client and storage bucket
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('firebase_admin.storage.bucket') as mock_bucket:
        
        # Set up mock blob for image deletion
        mock_blob = MagicMock()
        mock_bucket.return_value.blob.return_value = mock_blob
        
        # Make the request
        response = client.delete('/api/recipes/test-recipe-id')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response message
        assert 'message' in result
        assert 'deleted successfully' in result['message']
        
        # Verify Firestore document was deleted
        mock_db.collection.assert_called_with('recipes')
        mock_db.collection().document.assert_called_with('test-recipe-id')
        mock_db.collection().document().delete.assert_called_once()
        
        # Verify image was deleted if URL was provided in recipe
        mock_bucket.return_value.blob.assert_called_once()
        mock_blob.delete.assert_called_once()

def test_recipe_import(client, mock_auth_middleware, mock_db):
    """Test importing a recipe from URL"""
    # Mock the requests library and recipe scraper
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('firebase_admin.storage.bucket') as mock_bucket, \
         patch('requests.get') as mock_get, \
         patch('recipe_scrapers.scrape_me') as mock_scraper:
        
        # Mock storage blob for image upload
        mock_blob = MagicMock()
        mock_bucket.return_value.blob.return_value = mock_blob
        mock_blob.public_url = 'https://example.com/image.jpg'
        
        # Set up mock document reference
        mock_doc_ref = mock_db.collection.return_value.document.return_value
        mock_doc_ref.id = 'imported-recipe-id'
        
        # Mock the recipe scraper
        mock_scraper_instance = MagicMock()
        mock_scraper.return_value = mock_scraper_instance
        
        # Set up scraped recipe data
        mock_scraper_instance.title.return_value = "Imported Recipe"
        mock_scraper_instance.image.return_value = "https://example.com/original.jpg"
        mock_scraper_instance.total_time.return_value = 45
        mock_scraper_instance.yields.return_value = "4 servings"
        mock_scraper_instance.ingredients.return_value = ["Ingredient 1", "Ingredient 2"]
        mock_scraper_instance.instructions.return_value = "Step 1. Step 2."
        mock_scraper_instance.instructions_list.return_value = ["Step 1", "Step 2"]
        mock_scraper_instance.nutrients.return_value = {
            "calories": "300 kcal", 
            "fat": "10 g"
        }
        
        # Mock the image download response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'image data'
        mock_get.return_value = mock_response
        
        # Test request data
        data = {
            'url': 'https://example.com/recipe'
        }
        
        # Make the request
        response = client.post('/api/recipes/import', 
                              data=json.dumps(data),
                              content_type='application/json')
        
        # Check status code
        assert response.status_code == 201
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['title'] == 'Imported Recipe'
        assert result['id'] == 'imported-recipe-id'
        assert len(result['ingredients']) == 2
        assert len(result['instructions']) == 2
        assert result['imageUrl'] == 'https://example.com/image.jpg'
        
        # Verify Firestore document was created
        mock_db.collection.assert_called_with('recipes')
        mock_doc_ref.set.assert_called_once()
        
        # Verify scraped image was downloaded and uploaded to storage
        mock_get.assert_called_once()
        mock_bucket.return_value.blob.assert_called_once()
        mock_blob.upload_from_string.assert_called_once()

def test_search_recipes(client, mock_auth_middleware, mock_db, sample_recipe):
    """Test searching for recipes"""
    # Set up mock recipes collection
    recipes = [
        sample_recipe,
        {
            'id': 'test-recipe-2',
            'userId': 'test-user-id',
            'title': 'Another Recipe',
            'description': 'Another test recipe',
            'ingredients': ['Ingredient A', 'Ingredient B'],
            'instructions': ['Step A', 'Step B'],
            'tags': ['vegetarian', 'quick'],
            'createdAt': '2023-01-02T00:00:00Z',
            'updatedAt': '2023-01-02T00:00:00Z'
        }
    ]
    
    mock_collection, mock_query, mock_docs = mock_recipe_collection(
        mock_db, recipes
    )
    
    # Make the request with search parameters
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/recipes/search?q=test&tags=vegetarian')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'recipes' in result
        assert 'pagination' in result
        assert result['pagination']['total'] == 2  # Both recipes match in this mock
        
        # Verify Firestore query was called correctly
        mock_db.collection.assert_called_with('recipes')
        mock_collection.where.assert_called_once()
        mock_query.order_by.assert_called_once()
        mock_query.limit.assert_called_once()
        mock_query.offset.assert_called_once()
        mock_query.stream.assert_called_once()

def test_supported_sites(client):
    """Test getting list of supported recipe sites"""
    # Mock the recipe scrapers SCRAPERS dictionary
    with patch('recipe_scrapers.SCRAPERS', {'example.com': None, 'test.com': None}):
        # Make the request
        response = client.get('/api/recipes/supported-sites')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'supported_sites' in result
        assert len(result['supported_sites']) == 2
        assert 'example.com' in result['supported_sites']
        assert 'test.com' in result['supported_sites']

def test_recipe_share_unshare(client, mock_auth_middleware, mock_db, sample_recipe):
    """Test sharing and unsharing a recipe"""
    # Set up mock recipe document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_recipe
    
    # Mock the Firestore client
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        # Test sharing
        response = client.post('/api/recipes/share/test-recipe-id')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'message' in result
        assert 'shared successfully' in result['message']
        assert result['isPublic'] is True
        
        # Verify Firestore update was called
        mock_db.collection.assert_called_with('recipes')
        mock_db.collection().document.assert_called_with('test-recipe-id')
        mock_db.collection().document().update.assert_called_once()
        
        # Reset mock for unshare test
        mock_db.reset_mock()
        
        # Test unsharing
        response = client.post('/api/recipes/unshare/test-recipe-id')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'message' in result
        assert 'now private' in result['message']
        assert result['isPublic'] is False
        
        # Verify Firestore update was called
        mock_db.collection.assert_called_with('recipes')
        mock_db.collection().document.assert_called_with('test-recipe-id')
        mock_db.collection().document().update.assert_called_once()