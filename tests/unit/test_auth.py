"""Unit tests for authentication module"""
import pytest
from unittest.mock import patch, MagicMock
import json
import firebase_admin
from flask import jsonify

# Import the auth blueprint
from auth.routes import auth_bp

def test_profile_create(client, mock_auth_middleware, mock_db):
    """Test creating a user profile"""
    # Mock the Firestore client used in the view
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('firebase_admin.storage.bucket') as mock_bucket:
        
        # Mock storage blob for image upload
        mock_blob = MagicMock()
        mock_bucket.return_value.blob.return_value = mock_blob
        mock_blob.public_url = 'https://example.com/image.jpg'
        
        # Test request data
        data = {
            'name': 'Test User',
            'profile_image_base64': 'SGVsbG8gV29ybGQ='  # Base64 for "Hello World"
        }
        
        # Make the request
        response = client.post('/api/auth/profile', 
                              data=json.dumps(data),
                              content_type='application/json')
        
        # Check status code
        assert response.status_code == 201
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['name'] == 'Test User'
        assert result['id'] == 'test-user-id'
        assert result['profile_image_url'] == 'https://example.com/image.jpg'
        
        # Verify Firestore set was called
        mock_db.collection.assert_called_with('users')
        mock_db.collection().document.assert_called_with('test-user-id')
        mock_db.collection().document().set.assert_called_once()
        
        # Verify storage blob upload was called
        mock_bucket.return_value.blob.assert_called_once()
        mock_blob.upload_from_string.assert_called_once()

def test_profile_get_exists(client, mock_auth_middleware, mock_db):
    """Test getting an existing user profile"""
    # Set up mock data
    mock_user_data = {
        'id': 'test-user-id',
        'name': 'Test User',
        'profile_image_url': 'https://example.com/image.jpg',
        'created_at': '2023-01-01T00:00:00Z',
        'updated_at': '2023-01-01T00:00:00Z'
    }
    
    # Configure mock to return user data
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = mock_user_data
    mock_doc.id = 'test-user-id'
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/auth/profile')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['name'] == 'Test User'
        assert result['id'] == 'test-user-id'
        assert result['profile_image_url'] == 'https://example.com/image.jpg'
        
        # Verify Firestore get was called
        mock_db.collection.assert_called_with('users')
        mock_db.collection().document.assert_called_with('test-user-id')
        mock_db.collection().document().get.assert_called_once()

def test_profile_get_not_found(client, mock_auth_middleware, mock_db):
    """Test getting a non-existent user profile"""
    # Configure mock to return no user data
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = False
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/auth/profile')
        
        # Check status code
        assert response.status_code == 404
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate error message
        assert 'error' in result
        assert 'User not found' in result['error']
        
        # Verify Firestore get was called
        mock_db.collection.assert_called_with('users')
        mock_db.collection().document.assert_called_with('test-user-id')
        mock_db.collection().document().get.assert_called_once()

def test_auth_middleware_unauthorized(client):
    """Test auth middleware with unauthorized request"""
    # Mock the auth_required decorator to simulate auth failure
    with patch('utils.firebase_admin.auth_required') as mock_auth_required:
        # Make the decorator return an unauthorized response
        mock_auth_required.side_effect = lambda f: lambda *args, **kwargs: (
            jsonify({'error': 'Unauthorized'}), 401
        )
        
        # Make the request
        response = client.get('/api/auth/profile')
        
        # Check status code
        assert response.status_code == 401
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate error message
        assert 'error' in result
        assert result['error'] == 'Unauthorized'