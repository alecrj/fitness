"""Unit tests for social module"""
import pytest
from unittest.mock import patch, MagicMock
import json
import firebase_admin
from flask import jsonify
import requests

# Import the social blueprint
from social.routes import social_bp
from social.models import Post, Comment, Like, Follow

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
def sample_post():
    """Return a sample social post for testing"""
    return {
        'id': 'test-post-id',
        'userId': 'test-user-id',
        'userName': 'Test User',
        'userProfileImage': 'https://example.com/profile.jpg',
        'content': 'This is a test post',
        'imageUrl': 'https://example.com/post.jpg',
        'tags': ['fitness', 'nutrition'],
        'likes': 5,
        'comments': 2,
        'createdAt': '2023-01-01T00:00:00Z',
        'updatedAt': '2023-01-01T00:00:00Z'
    }

@pytest.fixture
def sample_comment():
    """Return a sample comment for testing"""
    return {
        'id': 'test-comment-id',
        'userId': 'test-user-id',
        'userName': 'Test User',
        'userProfileImage': 'https://example.com/profile.jpg',
        'postId': 'test-post-id',
        'content': 'This is a test comment',
        'createdAt': '2023-01-01T00:00:00Z',
        'updatedAt': '2023-01-01T00:00:00Z'
    }

def mock_social_collection(mock_db, items=None, collection_name='posts'):
    """Set up mock collection with data for social module testing"""
    items = items or []
    
    # Mock collection query methods
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
        mock_doc.id = item.get('id', f'{collection_name[:-1]}-{i}')
        mock_doc.to_dict.return_value = item
        mock_docs.append(mock_doc)
    
    # Set up stream method to return docs
    mock_query.stream.return_value = mock_docs
    
    return mock_collection, mock_query, mock_docs

def test_create_post(client, mock_auth_middleware, mock_db):
    """Test creating a new social post"""
    # Mock the Firestore client and storage bucket
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('firebase_admin.storage.bucket') as mock_bucket:
        
        # Mock storage blob for image upload
        mock_blob = MagicMock()
        mock_bucket.return_value.blob.return_value = mock_blob
        mock_blob.public_url = 'https://example.com/post.jpg'
        
        # Set up mock document reference
        mock_doc_ref = mock_db.collection.return_value.document.return_value
        mock_doc_ref.id = 'new-post-id'
        
        # Set up mock user document for profile data
        user_doc = MagicMock()
        user_doc.exists = True
        user_doc.to_dict.return_value = {
            'name': 'Test User',
            'profile_image_url': 'https://example.com/profile.jpg'
        }
        
        # Make user query return our mock user
        mock_db.collection.return_value.document.return_value.get.return_value = user_doc
        
        # Test request data
        data = {
            'content': 'This is a new test post',
            'imageBase64': 'SGVsbG8gV29ybGQ=',  # Base64 for "Hello World"
            'tags': ['fitness', 'motivation']
        }
        
        # Make the request
        response = client.post('/api/social/posts', 
                              data=json.dumps(data),
                              content_type='application/json')
        
        # Check status code
        assert response.status_code == 201
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['content'] == 'This is a new test post'
        assert result['id'] == 'new-post-id'
        assert result['imageUrl'] == 'https://example.com/post.jpg'
        assert len(result['tags']) == 2
        assert result['tags'][0] == 'fitness'
        assert result['userName'] == 'Test User'
        
        # Verify Firestore document was created
        mock_db.collection.assert_any_call('users')
        mock_db.collection.assert_any_call('posts')
        mock_db.collection().document.assert_any_call('test-user-id')
        mock_doc_ref.set.assert_called_once()
        
        # Verify image was uploaded if base64 was provided
        mock_bucket.return_value.blob.assert_called_once()
        mock_blob.upload_from_string.assert_called_once()

def test_get_posts(client, mock_auth_middleware, mock_db, sample_post):
    """Test getting social posts feed"""
    # Set up mock posts collection
    mock_collection, mock_query, mock_docs = mock_social_collection(
        mock_db, [sample_post]
    )
    
    # Mock the like status check
    like_model_mock = MagicMock()
    like_model_mock.check_status.return_value = False
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('social.models.Like', return_value=like_model_mock):
        
        response = client.get('/api/social/posts')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'posts' in result
        assert len(result['posts']) == 1
        assert result['posts'][0]['content'] == 'This is a test post'
        assert result['posts'][0]['id'] == 'test-post-id'
        assert 'liked' in result['posts'][0]
        assert result['posts'][0]['liked'] is False
        
        # Verify Firestore query was called correctly
        mock_db.collection.assert_called_with('posts')
        mock_collection.where.assert_called_once()
        mock_query.order_by.assert_called_once()
        mock_query.limit.assert_called_once()
        mock_query.offset.assert_called_once()
        mock_query.stream.assert_called_once()
        
        # Verify like status was checked
        like_model_mock.check_status.assert_called_once()

def test_get_post_by_id(client, mock_auth_middleware, mock_db, sample_post):
    """Test getting a specific post by ID"""
    # Set up mock post document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_post
    mock_doc.id = 'test-post-id'
    
    # Mock the like status check
    like_model_mock = MagicMock()
    like_model_mock.check_status.return_value = True
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('social.models.Like', return_value=like_model_mock):
        
        response = client.get('/api/social/posts/test-post-id')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['content'] == 'This is a test post'
        assert result['id'] == 'test-post-id'
        assert result['liked'] is True
        
        # Verify Firestore get was called
        mock_db.collection.assert_called_with('posts')
        mock_db.collection().document.assert_called_with('test-post-id')
        mock_db.collection().document().get.assert_called_once()
        
        # Verify like status was checked
        like_model_mock.check_status.assert_called_once()

def test_update_post(client, mock_auth_middleware, mock_db, sample_post):
    """Test updating a social post"""
    # Set up mock post document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_post
    
    # Mock the Firestore client and storage bucket
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('firebase_admin.storage.bucket') as mock_bucket:
        
        # Test request data (partial update)
        data = {
            'content': 'Updated post content',
            'tags': ['fitness', 'motivation', 'progress']
        }
        
        # Make the request
        response = client.put('/api/social/posts/test-post-id', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['content'] == 'Updated post content'
        assert len(result['tags']) == 3
        assert result['id'] == 'test-post-id'
        
        # Original data should be preserved
        assert result['userName'] == 'Test User'
        assert result['likes'] == 5
        
        # Verify Firestore document was updated
        mock_db.collection.assert_called_with('posts')
        mock_db.collection().document.assert_called_with('test-post-id')
        mock_db.collection().document().update.assert_called_once()

def test_delete_post(client, mock_auth_middleware, mock_db, sample_post):
    """Test deleting a social post"""
    # Set up mock post document
    mock_doc = mock_db.collection.return_value.document.return_value.get.return_value
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_post
    
    # Mock the Firestore client and storage bucket
    with patch('firebase_admin.firestore.client', return_value=mock_db), \
         patch('firebase_admin.storage.bucket') as mock_bucket:
        
        # Set up mock blob for image deletion
        mock_blob = MagicMock()
        mock_bucket.return_value.blob.return_value = mock_blob
        
        # Make the request
        response = client.delete('/api/social/posts/test-post-id')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response message
        assert 'message' in result
        assert 'deleted successfully' in result['message']
        
        # Verify Firestore document was deleted
        mock_db.collection.assert_called_with('posts')
        mock_db.collection().document.assert_called_with('test-post-id')
        mock_db.collection().document().delete.assert_called_once()
        
        # Verify image was deleted if URL was provided in post
        mock_bucket.return_value.blob.assert_called_once()
        mock_blob.delete.assert_called_once()

def test_toggle_like(client, mock_auth_middleware, mock_db):
    """Test liking/unliking a post"""
    # Mock the Like model toggle method
    like_model_mock = MagicMock()
    like_model_mock.toggle.return_value = {
        'liked': True,
        'postId': 'test-post-id',
        'likeCount': 6
    }
    
    # Make the request
    with patch('social.models.Like', return_value=like_model_mock):
        response = client.post('/api/social/posts/test-post-id/like')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['liked'] is True
        assert result['postId'] == 'test-post-id'
        assert result['likeCount'] == 6
        
        # Verify like toggle was called
        like_model_mock.toggle.assert_called_once_with('test-user-id', 'test-post-id')

def test_create_comment(client, mock_auth_middleware, mock_db):
    """Test creating a comment on a post"""
    # Mock the Comment model create method
    comment_model_mock = MagicMock()
    comment_model_mock.create.return_value = {
        'id': 'new-comment-id',
        'userId': 'test-user-id',
        'userName': 'Test User',
        'userProfileImage': 'https://example.com/profile.jpg',
        'postId': 'test-post-id',
        'content': 'Test comment content',
        'createdAt': '2023-01-01T00:00:00Z',
        'updatedAt': '2023-01-01T00:00:00Z'
    }
    
    # Test request data
    data = {
        'content': 'Test comment content',
        'postId': 'test-post-id'
    }
    
    # Make the request
    with patch('social.models.Comment', return_value=comment_model_mock):
        response = client.post('/api/social/posts/test-post-id/comments', 
                              data=json.dumps(data),
                              content_type='application/json')
        
        # Check status code
        assert response.status_code == 201
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['content'] == 'Test comment content'
        assert result['id'] == 'new-comment-id'
        assert result['postId'] == 'test-post-id'
        assert result['userName'] == 'Test User'
        
        # Verify comment was created
        comment_model_mock.create.assert_called_once_with('test-user-id', data)

def test_get_comments(client, mock_auth_middleware, mock_db, sample_comment):
    """Test getting comments for a post"""
    # Mock the Comment model list_for_post method
    comment_model_mock = MagicMock()
    comment_model_mock.list_for_post.return_value = {
        'comments': [sample_comment],
        'pagination': {
            'total': 1,
            'limit': 20,
            'offset': 0
        }
    }
    
    # Make the request
    with patch('social.models.Comment', return_value=comment_model_mock):
        response = client.get('/api/social/posts/test-post-id/comments')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'comments' in result
        assert len(result['comments']) == 1
        assert result['comments'][0]['content'] == 'This is a test comment'
        assert result['comments'][0]['id'] == 'test-comment-id'
        assert 'pagination' in result
        
        # Verify list_for_post was called
        comment_model_mock.list_for_post.assert_called_once()
        args, kwargs = comment_model_mock.list_for_post.call_args
        assert args[0] == 'test-post-id'

def test_delete_comment(client, mock_auth_middleware, mock_db):
    """Test deleting a comment"""
    # Mock the Comment model delete method
    comment_model_mock = MagicMock()
    comment_model_mock.delete.return_value = True
    
    # Make the request
    with patch('social.models.Comment', return_value=comment_model_mock):
        response = client.delete('/api/social/comments/test-comment-id')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response message
        assert 'message' in result
        assert 'deleted successfully' in result['message']
        
        # Verify delete was called
        comment_model_mock.delete.assert_called_once_with('test-comment-id', 'test-user-id')

def test_toggle_follow(client, mock_auth_middleware, mock_db):
    """Test following/unfollowing a user"""
    # Mock the Follow model toggle method
    follow_model_mock = MagicMock()
    follow_model_mock.toggle.return_value = {
        'following': True,
        'followingId': 'target-user-id'
    }
    
    # Make the request
    with patch('social.models.Follow', return_value=follow_model_mock):
        response = client.post('/api/social/users/target-user-id/follow')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert result['following'] is True
        assert result['followingId'] == 'target-user-id'
        
        # Verify follow toggle was called
        follow_model_mock.toggle.assert_called_once_with('test-user-id', 'target-user-id')

def test_get_followers(client, mock_auth_middleware, mock_db, sample_user):
    """Test getting a user's followers"""
    # Mock the Follow model get_followers method
    follow_model_mock = MagicMock()
    follow_model_mock.get_followers.return_value = {
        'followers': [sample_user],
        'pagination': {
            'total': 1,
            'limit': 20,
            'offset': 0
        }
    }
    follow_model_mock.check_status.return_value = False
    
    # Make the request
    with patch('social.models.Follow', return_value=follow_model_mock):
        response = client.get('/api/social/users/target-user-id/followers')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'followers' in result
        assert len(result['followers']) == 1
        assert result['followers'][0]['name'] == 'Test User'
        assert result['followers'][0]['id'] == 'test-user-id'
        assert 'following' in result['followers'][0]
        assert result['followers'][0]['following'] is False
        assert 'pagination' in result
        
        # Verify get_followers was called
        follow_model_mock.get_followers.assert_called_once()
        args, kwargs = follow_model_mock.get_followers.call_args
        assert args[0] == 'target-user-id'

def test_get_following(client, mock_auth_middleware, mock_db, sample_user):
    """Test getting users that a user follows"""
    # Mock the Follow model get_following method
    follow_model_mock = MagicMock()
    follow_model_mock.get_following.return_value = {
        'following': [sample_user],
        'pagination': {
            'total': 1,
            'limit': 20,
            'offset': 0
        }
    }
    follow_model_mock.check_status.return_value = True
    
    # Make the request
    with patch('social.models.Follow', return_value=follow_model_mock):
        response = client.get('/api/social/users/target-user-id/following')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'following' in result
        assert len(result['following']) == 1
        assert result['following'][0]['name'] == 'Test User'
        assert result['following'][0]['id'] == 'test-user-id'
        assert 'following' in result['following'][0]
        assert result['following'][0]['following'] is True
        assert 'pagination' in result
        
        # Verify get_following was called
        follow_model_mock.get_following.assert_called_once()
        args, kwargs = follow_model_mock.get_following.call_args
        assert args[0] == 'target-user-id'

def test_get_liked_posts(client, mock_auth_middleware, mock_db, sample_post):
    """Test getting posts liked by a user"""
    # Mock the Like model get_user_likes method
    like_model_mock = MagicMock()
    like_model_mock.get_user_likes.return_value = {
        'posts': [sample_post],
        'pagination': {
            'total': 1,
            'limit': 20,
            'offset': 0
        }
    }
    
    # Make the request
    with patch('social.models.Like', return_value=like_model_mock):
        response = client.get('/api/social/users/me/likes')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'posts' in result
        assert len(result['posts']) == 1
        assert result['posts'][0]['content'] == 'This is a test post'
        assert result['posts'][0]['id'] == 'test-post-id'
        assert 'liked' in result['posts'][0]
        assert result['posts'][0]['liked'] is True
        assert 'pagination' in result
        
        # Verify get_user_likes was called
        like_model_mock.get_user_likes.assert_called_once_with('test-user-id', {'limit': 20, 'offset': 0})

def test_check_follow_status(client, mock_auth_middleware, mock_db):
    """Test checking if a user follows another user"""
    # Mock the Follow model check_status method
    follow_model_mock = MagicMock()
    follow_model_mock.check_status.return_value = True
    
    # Make the request
    with patch('social.models.Follow', return_value=follow_model_mock):
        response = client.get('/api/social/users/target-user-id/follow-status')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'following' in result
        assert result['following'] is True
        
        # Verify check_status was called
        follow_model_mock.check_status.assert_called_once_with('test-user-id', 'target-user-id')

def test_get_trending_tags(client, mock_auth_middleware, mock_db):
    """Test getting trending tags"""
    # Mock the posts collection
    mock_collection, mock_query, mock_docs = mock_social_collection(
        mock_db, [
            {'tags': ['fitness', 'nutrition']}, 
            {'tags': ['fitness', 'motivation']},
            {'tags': ['fitness']}
        ]
    )
    
    # Make the request
    with patch('firebase_admin.firestore.client', return_value=mock_db):
        response = client.get('/api/social/trending/tags')
        
        # Check status code
        assert response.status_code == 200
        
        # Parse response
        result = json.loads(response.data)
        
        # Validate response data
        assert 'trending_tags' in result
        assert isinstance(result['trending_tags'], list)
        
        # Verify Firestore query was called
        mock_db.collection.assert_called_with('posts')
        mock_collection.order_by.assert_called_once()
        mock_collection.limit.assert_called_once()
        mock_query.stream.assert_called_once()