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

# Now import the module we want to test
from social.models import Post, Comment, Like, Follow


class TestPostModel(unittest.TestCase):
    """Test cases for the Post model"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock Firestore client
        self.mock_db = MagicMock()
        
        # Mock collection and document references
        self.mock_collection = MagicMock()
        self.mock_doc_ref = MagicMock()
        self.mock_doc = MagicMock()
        self.mock_user_collection = MagicMock()
        self.mock_user_doc = MagicMock()
        self.mock_user_ref = MagicMock()
        
        # Set up the chain of mocks
        self.mock_db.collection.side_effect = lambda x: self.mock_user_collection if x == 'users' else self.mock_collection
        self.mock_collection.document.return_value = self.mock_doc_ref
        self.mock_doc_ref.get.return_value = self.mock_doc
        self.mock_user_collection.document.return_value = self.mock_user_ref
        self.mock_user_ref.get.return_value = self.mock_user_doc
        
        # Initialize model with mock db
        self.post_model = Post(self.mock_db)
        
        # Test data
        self.test_user_id = "test_user_123"
        self.test_post_id = "test_post_123"
        self.test_post_data = {
            'content': 'This is a test post',
            'tags': ['fitness', 'food', 'test']
        }
        
        # Mock user data
        self.mock_user_data = {
            'name': 'Test User',
            'profile_image_url': 'https://example.com/profile.jpg',
            'email': 'test@example.com'
        }
        
    def test_create_post(self):
        """Test creating a new post"""
        # Mock user document exists
        self.mock_user_doc.exists = True
        self.mock_user_doc.to_dict.return_value = self.mock_user_data
        
        # Set up mock document ID
        self.mock_doc_ref.id = self.test_post_id
        
        # Test creating a post
        post = self.post_model.create(self.test_user_id, self.test_post_data)
        
        # Verify Firestore was called correctly
        self.mock_user_collection.document.assert_called_with(self.test_user_id)
        self.mock_collection.document.assert_called_once()
        self.mock_doc_ref.set.assert_called_once()
        
        # Verify the returned post has the right structure
        self.assertEqual(post['id'], self.test_post_id)
        self.assertEqual(post['content'], 'This is a test post')
        self.assertEqual(post['userId'], self.test_user_id)
        self.assertEqual(post['userName'], 'Test User')
        self.assertEqual(post['tags'], ['fitness', 'food', 'test'])
        self.assertEqual(post['likes'], 0)
        self.assertEqual(post['comments'], 0)
        
    def test_create_post_missing_content(self):
        """Test validation error during post creation"""
        # Test with missing required field
        invalid_data = {
            'tags': ['test']
        }
        
        # Verify validation error is raised
        with self.assertRaises(ValueError) as context:
            self.post_model.create(self.test_user_id, invalid_data)
        
        self.assertTrue('Post content is required' in str(context.exception))
        
    def test_create_post_invalid_user(self):
        """Test creating a post for a non-existent user"""
        # Mock user document doesn't exist
        self.mock_user_doc.exists = False
        
        # Verify validation error is raised
        with self.assertRaises(ValueError) as context:
            self.post_model.create(self.test_user_id, self.test_post_data)
        
        self.assertTrue('User not found' in str(context.exception))
        
    def test_get_post(self):
        """Test getting a post by ID"""
        # Mock post data
        mock_post_data = {
            'userId': self.test_user_id,
            'content': 'This is a test post',
            'tags': ['fitness', 'food', 'test'],
            'likes': 0,
            'comments': 0
        }
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_post_data
        self.mock_doc.id = self.test_post_id
        
        # Test getting the post
        post = self.post_model.get(self.test_post_id)
        
        # Verify Firestore was called correctly
        self.mock_collection.document.assert_called_with(self.test_post_id)
        self.mock_doc_ref.get.assert_called_once()
        
        # Verify the returned post has the right structure
        self.assertEqual(post['id'], self.test_post_id)
        self.assertEqual(post['content'], 'This is a test post')
        self.assertEqual(post['userId'], self.test_user_id)
        
    def test_get_nonexistent_post(self):
        """Test getting a post that doesn't exist"""
        # Mock document doesn't exist
        self.mock_doc.exists = False
        
        # Verify ValueError is raised
        with self.assertRaises(ValueError) as context:
            self.post_model.get(self.test_post_id)
        
        self.assertTrue('Post not found' in str(context.exception))
        
    def test_update_post(self):
        """Test updating a post"""
        # Mock post data
        mock_post_data = {
            'userId': self.test_user_id,
            'content': 'This is a test post',
            'tags': ['fitness', 'food', 'test'],
            'likes': 0,
            'comments': 0
        }
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_post_data
        
        # Update data
        update_data = {
            'content': 'Updated post content',
            'tags': ['fitness', 'updated']
        }
        
        # Test updating the post
        updated_post = self.post_model.update(self.test_post_id, self.test_user_id, update_data)
        
        # Verify Firestore was called correctly
        self.mock_collection.document.assert_called_with(self.test_post_id)
        self.mock_doc_ref.update.assert_called_once()
        
        # Verify the returned post has the updated values
        self.assertEqual(updated_post['content'], 'Updated post content')
        self.assertEqual(updated_post['tags'], ['fitness', 'updated'])
        
    def test_update_unauthorized_post(self):
        """Test unauthorized post update"""
        # Mock post owned by a different user
        mock_post_data = {
            'userId': 'different_user_id',
            'content': 'This is a test post'
        }
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_post_data
        
        # Update data
        update_data = {
            'content': 'Updated post content'
        }
        
        # Verify ValueError is raised for unauthorized update
        with self.assertRaises(ValueError) as context:
            self.post_model.update(self.test_post_id, self.test_user_id, update_data)
        
        self.assertTrue('Unauthorized to update this post' in str(context.exception))
        
    def test_delete_post(self):
        """Test deleting a post"""
        # Mock post data
        mock_post_data = {
            'userId': self.test_user_id,
            'content': 'This is a test post'
        }
        
        self.mock_doc.exists = True
        self.mock_doc.to_dict.return_value = mock_post_data
        
        # Mock comments query
        mock_comments_query = MagicMock()
        mock_comment_docs = [MagicMock(), MagicMock()]
        mock_comments_query.stream.return_value = mock_comment_docs
        self.mock_db.collection.return_value.where.return_value = mock_comments_query
        
        # Test deleting the post
        result = self.post_model.delete(self.test_post_id, self.test_user_id)
        
        # Verify Firestore was called correctly
        self.mock_collection.document.assert_called_with(self.test_post_id)
        self.mock_doc_ref.delete.assert_called_once()
        
        # Verify successful deletion
        self.assertTrue(result)


class TestCommentModel(unittest.TestCase):
    """Test cases for the Comment model"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock Firestore client
        self.mock_db = MagicMock()
        
        # Create a mock Post model
        self.mock_post_model = MagicMock()
        
        # Test data
        self.test_user_id = "test_user_123"
        self.test_post_id = "test_post_123"
        self.test_comment_id = "test_comment_123"
        
        # Initialize model
        self.comment_model = Comment(self.mock_db)
        self.comment_model.post_model = self.mock_post_model
        
        # Mock post data
        self.mock_post = {
            'id': self.test_post_id,
            'content': 'Test post',
            'userId': 'post_author_id',
            'comments': 5
        }
        
        # Mock comment data
        self.test_comment_data = {
            'content': 'This is a test comment',
            'postId': self.test_post_id
        }
        
    def test_create_comment(self):
        """Test creating a new comment"""
        # Mock post retrieval
        self.mock_post_model.get.return_value = self.mock_post
        
        # Mock user collection
        mock_user_collection = MagicMock()
        mock_user_doc = MagicMock()
        mock_user_doc.exists = True
        mock_user_doc.to_dict.return_value = {'name': 'Test User', 'profile_image_url': 'http://example.com/profile.jpg'}
        mock_user_collection.document.return_value.get.return_value = mock_user_doc
        
        # Mock the post collection for updating comment count
        mock_post_collection = MagicMock()
        
        # Set up collection mocking
        self.mock_db.collection.side_effect = lambda x: mock_user_collection if x == 'users' else (
            mock_post_collection if x == 'posts' else MagicMock())
        
        # Set up document mock for the comment
        mock_comment_doc = MagicMock()
        mock_comment_doc.id = self.test_comment_id
        self.mock_db.collection().document.return_value = mock_comment_doc
        
        # Test creating a comment
        comment = self.comment_model.create(self.test_user_id, self.test_comment_data)
        
        # Verify post was retrieved
        self.mock_post_model.get.assert_called_with(self.test_post_id)
        
        # Verify user was looked up
        mock_user_collection.document.assert_called_with(self.test_user_id)
        
        # Verify comment was saved
        mock_comment_doc.set.assert_called_once()
        
        # Verify post comment count was updated
        mock_post_collection.document.assert_called_with(self.test_post_id)
        
        # Verify comment data
        self.assertEqual(comment['postId'], self.test_post_id)
        self.assertEqual(comment['content'], 'This is a test comment')
        self.assertEqual(comment['userId'], self.test_user_id)
        self.assertEqual(comment['id'], self.test_comment_id)
        
    def test_create_comment_invalid_post(self):
        """Test creating a comment on a non-existent post"""
        # Mock post retrieval failure
        self.mock_post_model.get.side_effect = ValueError('Post not found')
        
        # Verify ValueError is raised
        with self.assertRaises(ValueError) as context:
            self.comment_model.create(self.test_user_id, self.test_comment_data)
        
        self.assertTrue('Post not found' in str(context.exception))
        

class TestLikeModel(unittest.TestCase):
    """Test cases for the Like model"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock Firestore client
        self.mock_db = MagicMock()
        
        # Create a mock Post model
        self.mock_post_model = MagicMock()
        
        # Test data
        self.test_user_id = "test_user_123"
        self.test_post_id = "test_post_123"
        self.test_like_id = f"{self.test_user_id}_{self.test_post_id}"
        
        # Initialize model
        self.like_model = Like(self.mock_db)
        self.like_model.post_model = self.mock_post_model
        
        # Mock post data
        self.mock_post = {
            'id': self.test_post_id,
            'content': 'Test post',
            'userId': 'post_author_id',
            'likes': 10
        }
        
    def test_toggle_like_creating(self):
        """Test toggling a like (creating)"""
        # Mock post retrieval
        self.mock_post_model.get.return_value = self.mock_post
        
        # Mock like document doesn't exist
        mock_like_doc = MagicMock()
        mock_like_doc.exists = False
        self.mock_db.collection().document().get.return_value = mock_like_doc
        
        # Test toggling like (creating)
        result = self.like_model.toggle(self.test_user_id, self.test_post_id)
        
        # Verify post was retrieved
        self.mock_post_model.get.assert_called_with(self.test_post_id)
        
        # Verify like document was checked and set
        self.mock_db.collection().document.assert_called_with(self.test_like_id)
        self.mock_db.collection().document().set.assert_called_once()
        
        # Verify post was updated
        self.mock_db.collection().document.assert_called_with(self.test_post_id)
        
        # Verify result
        self.assertTrue(result['liked'])
        self.assertEqual(result['postId'], self.test_post_id)
        self.assertEqual(result['likeCount'], 11)  # 10 + 1
        
    def test_toggle_like_removing(self):
        """Test toggling a like (removing)"""
        # Mock post retrieval
        self.mock_post_model.get.return_value = self.mock_post
        
        # Mock like document exists
        mock_like_doc = MagicMock()
        mock_like_doc.exists = True
        self.mock_db.collection().document().get.return_value = mock_like_doc
        
        # Test toggling like (removing)
        result = self.like_model.toggle(self.test_user_id, self.test_post_id)
        
        # Verify post was retrieved
        self.mock_post_model.get.assert_called_with(self.test_post_id)
        
        # Verify like document was checked and deleted
        self.mock_db.collection().document.assert_called_with(self.test_like_id)
        self.mock_db.collection().document().delete.assert_called_once()
        
        # Verify post was updated
        self.mock_db.collection().document.assert_called_with(self.test_post_id)
        
        # Verify result
        self.assertFalse(result['liked'])
        self.assertEqual(result['postId'], self.test_post_id)
        self.assertEqual(result['likeCount'], 9)  # 10 - 1
        
    def test_check_status(self):
        """Test checking like status"""
        # Mock like document existence check
        mock_like_doc = MagicMock()
        mock_like_doc.exists = True
        self.mock_db.collection().document().get.return_value = mock_like_doc
        
        # Test checking like status
        result = self.like_model.check_status(self.test_user_id, self.test_post_id)
        
        # Verify like document was checked
        self.mock_db.collection.assert_called_with('likes')
        self.mock_db.collection().document.assert_called_with(self.test_like_id)
        
        # Verify result
        self.assertTrue(result)


class TestFollowModel(unittest.TestCase):
    """Test cases for the Follow model"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock Firestore client
        self.mock_db = MagicMock()
        
        # Test data
        self.follower_id = "follower_user_123"
        self.following_id = "following_user_456"
        self.follow_id = f"{self.follower_id}_{self.following_id}"
        
        # Initialize model
        self.follow_model = Follow(self.mock_db)
        
        # Mock user documents
        self.mock_follower_doc = MagicMock()
        self.mock_follower_doc.exists = True
        
        self.mock_following_doc = MagicMock()
        self.mock_following_doc.exists = True
        
    def test_toggle_follow_creating(self):
        """Test toggling a follow relationship (creating)"""
        # Mock user document retrieval
        self.mock_db.collection().document.side_effect = lambda user_id: MagicMock(
            get=MagicMock(return_value=self.mock_follower_doc if user_id == self.follower_id else self.mock_following_doc)
        )
        
        # Mock follow document doesn't exist
        mock_follow_doc = MagicMock()
        mock_follow_doc.exists = False
        
        # Set up document mocks
        self.mock_db.collection().document.return_value.get.return_value = mock_follow_doc
        
        # Test toggling follow (creating)
        result = self.follow_model.toggle(self.follower_id, self.following_id)
        
        # Verify follow document was checked and set
        self.mock_db.collection().document.assert_called_with(self.follow_id)
        
        # Verify user counts were updated
        self.mock_db.collection().document().update.assert_called()
        
        # Verify result
        self.assertTrue(result['following'])
        self.assertEqual(result['followingId'], self.following_id)
        
    def test_toggle_follow_removing(self):
        """Test toggling a follow relationship (removing)"""
        # Mock user document retrieval
        self.mock_db.collection().document.side_effect = lambda user_id: MagicMock(
            get=MagicMock(return_value=self.mock_follower_doc if user_id == self.follower_id else self.mock_following_doc)
        )
        
        # Mock follow document exists
        mock_follow_doc = MagicMock()
        mock_follow_doc.exists = True
        
        # Set up document mocks
        self.mock_db.collection().document().get.return_value = mock_follow_doc
        
        # Test toggling follow (removing)
        result = self.follow_model.toggle(self.follower_id, self.following_id)
        
        # Verify follow document was checked and deleted
        self.mock_db.collection().document.assert_called_with(self.follow_id)
        self.mock_db.collection().document().delete.assert_called_once()
        
        # Verify user counts were updated
        self.mock_db.collection().document().update.assert_called()
        
        # Verify result
        self.assertFalse(result['following'])
        self.assertEqual(result['followingId'], self.following_id)
        
    def test_self_follow(self):
        """Test attempt to follow oneself"""
        # Verify ValueError is raised
        with self.assertRaises(ValueError) as context:
            self.follow_model.toggle(self.follower_id, self.follower_id)
        
        self.assertTrue('Cannot follow yourself' in str(context.exception))
        
    def test_check_follow_status(self):
        """Test checking follow status"""
        # Mock follow document existence check
        mock_follow_doc = MagicMock()
        mock_follow_doc.exists = True
        self.mock_db.collection().document().get.return_value = mock_follow_doc
        
        # Test checking follow status
        result = self.follow_model.check_status(self.follower_id, self.following_id)
        
        # Verify follow document was checked
        self.mock_db.collection.assert_called_with('follows')
        self.mock_db.collection().document.assert_called_with(self.follow_id)
        
        # Verify result
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
