"""Test configuration for pytest"""
import os
import sys
import pytest
from unittest.mock import MagicMock, patch
import tempfile
import json
import firebase_admin

# Add the parent directory to the path so we can import our app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock Firebase for testing
@pytest.fixture(scope="session", autouse=True)
def mock_firebase():
    """Mock Firebase services for all tests"""
    # Create mocks for Firebase services
    mock_auth = MagicMock()
    mock_firestore = MagicMock()
    mock_storage = MagicMock()
    
    # Patch Firebase initialization
    with patch.object(firebase_admin, 'initialize_app', return_value=None), \
         patch.object(firebase_admin, 'get_app', return_value=None), \
         patch.object(firebase_admin, 'delete_app', return_value=None), \
         patch.object(firebase_admin, 'auth', mock_auth), \
         patch.object(firebase_admin, 'firestore', mock_firestore), \
         patch.object(firebase_admin, 'storage', mock_storage):
        yield {
            'auth': mock_auth,
            'firestore': mock_firestore,
            'storage': mock_storage
        }

@pytest.fixture
def app():
    """Create Flask test app"""
    from app import create_app
    
    # Create a temporary file for configuration
    with tempfile.NamedTemporaryFile(suffix='.json') as f:
        # Write mock Firebase credentials
        json.dump({
            "type": "service_account",
            "project_id": "test-project",
            "private_key_id": "test-key-id",
            "private_key": "test-private-key",
            "client_email": "test@example.com",
            "client_id": "test-client-id",
            "auth_uri": "https://example.com/auth",
            "token_uri": "https://example.com/token",
            "auth_provider_x509_cert_url": "https://example.com/cert",
            "client_x509_cert_url": "https://example.com/client-cert"
        }, f)
        f.flush()
        
        # Set test environment variables
        os.environ['FLASK_ENV'] = 'testing'
        os.environ['FIREBASE_CREDENTIALS_PATH'] = f.name
        os.environ['FIREBASE_STORAGE_BUCKET'] = 'test-bucket'
        os.environ['SECRET_KEY'] = 'test-key'
        os.environ['USDA_API_KEY'] = 'test-api-key'
        
        # Create app instance
        app = create_app()
        app.config['TESTING'] = True
        
        yield app

@pytest.fixture
def client(app):
    """Create Flask test client"""
    return app.test_client()

@pytest.fixture
def mock_db():
    """Create a mock Firestore database"""
    # Create a mock Firestore client
    mock_db = MagicMock()
    
    # Mock collection method
    mock_collection = MagicMock()
    mock_db.collection.return_value = mock_collection
    
    # Mock document method
    mock_doc_ref = MagicMock()
    mock_collection.document.return_value = mock_doc_ref
    
    # Mock document snapshot
    mock_doc = MagicMock()
    mock_doc_ref.get.return_value = mock_doc
    
    # Set up default behavior for exists
    mock_doc.exists = True
    
    # Set up default behavior for to_dict
    mock_doc.to_dict.return_value = {}
    
    return mock_db

@pytest.fixture
def mock_auth_middleware():
    """Mock the auth_required decorator"""
    with patch('utils.firebase_admin.auth_required') as mock_auth_required:
        # Make the decorator simply call the wrapped function with a user_id
        mock_auth_required.side_effect = lambda f: lambda *args, **kwargs: f(*args, user_id='test-user-id', **kwargs)
        yield mock_auth_required

@pytest.fixture
def auth_headers():
    """Create authentication headers for testing"""
    return {
        'Authorization': 'Bearer test-token'
    }