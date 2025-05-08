# social/models.py
from datetime import datetime
from typing import List, Dict, Any, Optional
import firebase_admin
from firebase_admin import firestore

class Post:
    """Model for social posts in the application"""
    
    def __init__(self, db=None):
        """Initialize the Post model with database reference"""
        self.db = db or firebase_admin.firestore.client()
        self.collection = "posts"
    
    def create(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new social post
        
        Args:
            user_id: The ID of the user creating the post
            data: Post content and metadata
            
        Returns:
            Dict containing the created post with ID
            
        Raises:
            ValueError: If required fields are missing
        """
        # Validate required fields
        if not data.get('content'):
            raise ValueError("Post content is required")
        
        # Get user details
        user_doc = self.db.collection('users').document(user_id).get()
        if not user_doc.exists:
            raise ValueError("User not found")
        
        user = user_doc.to_dict()
        
        # Create post document
        post = {
            'userId': user_id,
            'userName': user.get('name', 'User'),
            'userProfileImage': user.get('profile_image_url'),
            'content': data['content'],
            'imageUrl': data.get('imageUrl'),
            'recipeId': data.get('recipeId'),
            'mealId': data.get('mealId'),
            'tags': data.get('tags', []),
            'likes': 0,
            'comments': 0,
            'createdAt': firestore.SERVER_TIMESTAMP,
            'updatedAt': firestore.SERVER_TIMESTAMP
        }
        
        # Save to database
        doc_ref = self.db.collection(self.collection).document()
        doc_ref.set(post)
        
        # Return with ID
        post['id'] = doc_ref.id
        return post
    
    def get(self, post_id: str) -> Dict[str, Any]:
        """Get a post by ID
        
        Args:
            post_id: The ID of the post to retrieve
            
        Returns:
            Dict containing the post data
            
        Raises:
            ValueError: If post not found
        """
        doc = self.db.collection(self.collection).document(post_id).get()
        
        if not doc.exists:
            raise ValueError("Post not found")
            
        post = doc.to_dict()
        post['id'] = doc.id
        return post
    
    def list(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """List posts with filtering and pagination
        
        Args:
            query_params: Dict containing filter and pagination parameters
            
        Returns:
            Dict containing posts and pagination info
        """
        # Start with base query
        query = self.db.collection(self.collection)
        
        # Apply user filter if provided
        if query_params.get('userId'):
            query = query.where('userId', '==', query_params['userId'])
        
        # Apply tag filter if provided
        if query_params.get('tag'):
            query = query.where('tags', 'array_contains', query_params['tag'])
            
        # Apply recipe filter if provided
        if query_params.get('recipeId'):
            query = query.where('recipeId', '==', query_params['recipeId'])
        
        # Apply meal filter if provided
        if query_params.get('mealId'):
            query = query.where('mealId', '==', query_params['mealId'])
            
        # Apply sorting - newest first by default
        query = query.order_by('createdAt', direction=firestore.Query.DESCENDING)
        
        # Pagination
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Execute query with pagination
        posts = []
        post_docs = query.limit(limit).offset(offset).stream()
        
        for doc in post_docs:
            post = doc.to_dict()
            post['id'] = doc.id
            posts.append(post)
            
        # Get total count (for pagination)
        # Note: This is not efficient for large collections
        # In production, consider using a counter or alternative approach
        total_query = query.stream()
        total = sum(1 for _ in total_query)
            
        return {
            'posts': posts,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }
    
    def update(self, post_id: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a post
        
        Args:
            post_id: ID of the post to update
            user_id: ID of the user making the update (for authorization)
            data: Updated post data
            
        Returns:
            Dict containing the updated post
            
        Raises:
            ValueError: If post not found or user not authorized
        """
        doc_ref = self.db.collection(self.collection).document(post_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise ValueError("Post not found")
            
        post = doc.to_dict()
        
        # Check ownership
        if post.get('userId') != user_id:
            raise ValueError("Unauthorized to update this post")
            
        # Update fields
        update_data = {
            'content': data.get('content', post.get('content')),
            'imageUrl': data.get('imageUrl', post.get('imageUrl')),
            'tags': data.get('tags', post.get('tags', [])),
            'updatedAt': firestore.SERVER_TIMESTAMP
        }
        
        # Update document
        doc_ref.update(update_data)
        
        # Return updated post
        updated_post = post.copy()
        updated_post.update(update_data)
        updated_post['id'] = post_id
        
        return updated_post
    
    def delete(self, post_id: str, user_id: str) -> bool:
        """Delete a post
        
        Args:
            post_id: ID of the post to delete
            user_id: ID of the user making the deletion (for authorization)
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If post not found or user not authorized
        """
        doc_ref = self.db.collection(self.collection).document(post_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise ValueError("Post not found")
            
        post = doc.to_dict()
        
        # Check ownership
        if post.get('userId') != user_id:
            raise ValueError("Unauthorized to delete this post")
            
        # Delete the document
        doc_ref.delete()
        
        # Also delete associated comments
        comments_query = self.db.collection('comments').where('postId', '==', post_id)
        for comment_doc in comments_query.stream():
            comment_doc.reference.delete()
            
        return True


class Comment:
    """Model for comments on social posts"""
    
    def __init__(self, db=None):
        """Initialize the Comment model with database reference"""
        self.db = db or firebase_admin.firestore.client()
        self.collection = "comments"
        self.post_model = Post(db)
    
    def create(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new comment
        
        Args:
            user_id: The ID of the user creating the comment
            data: Comment content and metadata
            
        Returns:
            Dict containing the created comment
            
        Raises:
            ValueError: If required fields are missing or post not found
        """
        # Validate required fields
        if not data.get('content'):
            raise ValueError("Comment content is required")
            
        if not data.get('postId'):
            raise ValueError("Post ID is required")
            
        # Verify post exists
        try:
            post = self.post_model.get(data['postId'])
        except ValueError:
            raise ValueError("Post not found")
            
        # Get user details
        user_doc = self.db.collection('users').document(user_id).get()
        if not user_doc.exists:
            raise ValueError("User not found")
            
        user = user_doc.to_dict()
        
        # Create comment document
        comment = {
            'userId': user_id,
            'userName': user.get('name', 'User'),
            'userProfileImage': user.get('profile_image_url'),
            'postId': data['postId'],
            'content': data['content'],
            'createdAt': firestore.SERVER_TIMESTAMP,
            'updatedAt': firestore.SERVER_TIMESTAMP
        }
        
        # Save to database
        doc_ref = self.db.collection(self.collection).document()
        doc_ref.set(comment)
        
        # Increment comment count on post
        self.db.collection('posts').document(data['postId']).update({
            'comments': firestore.Increment(1)
        })
        
        # Return with ID
        comment['id'] = doc_ref.id
        return comment
    
    def list_for_post(self, post_id: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """List comments for a specific post
        
        Args:
            post_id: The ID of the post to get comments for
            query_params: Dict containing pagination parameters
            
        Returns:
            Dict containing comments and pagination info
        """
        # Start with base query
        query = self.db.collection(self.collection).where('postId', '==', post_id)
        
        # Apply sorting - newest first by default
        sort_by = query_params.get('sort_by', 'createdAt')
        sort_dir = query_params.get('sort_dir', 'desc')
        direction = firestore.Query.DESCENDING if sort_dir == 'desc' else firestore.Query.ASCENDING
        query = query.order_by(sort_by, direction=direction)
        
        # Pagination
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Execute query
        comments = []
        comment_docs = query.limit(limit).offset(offset).stream()
        
        for doc in comment_docs:
            comment = doc.to_dict()
            comment['id'] = doc.id
            comments.append(comment)
            
        # Get total count
        total_query = self.db.collection(self.collection).where('postId', '==', post_id).stream()
        total = sum(1 for _ in total_query)
            
        return {
            'comments': comments,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }
    
    def delete(self, comment_id: str, user_id: str) -> bool:
        """Delete a comment
        
        Args:
            comment_id: The ID of the comment to delete
            user_id: The ID of the user making the deletion (for authorization)
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If comment not found or user not authorized
        """
        doc_ref = self.db.collection(self.collection).document(comment_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise ValueError("Comment not found")
            
        comment = doc.to_dict()
        
        # Check ownership
        if comment.get('userId') != user_id:
            raise ValueError("Unauthorized to delete this comment")
            
        # Get post ID for decrementing comment count
        post_id = comment.get('postId')
        
        # Delete the document
        doc_ref.delete()
        
        # Decrement comment count on post
        if post_id:
            self.db.collection('posts').document(post_id).update({
                'comments': firestore.Increment(-1)
            })
            
        return True


class Like:
    """Model for likes on posts"""
    
    def __init__(self, db=None):
        """Initialize the Like model with database reference"""
        self.db = db or firebase_admin.firestore.client()
        self.collection = "likes"
        self.post_model = Post(db)
    
    def toggle(self, user_id: str, post_id: str) -> Dict[str, Any]:
        """Toggle like status for a post
        
        Args:
            user_id: The ID of the user toggling the like
            post_id: The ID of the post to like/unlike
            
        Returns:
            Dict containing the updated like status
            
        Raises:
            ValueError: If post not found
        """
        # Verify post exists
        try:
            post = self.post_model.get(post_id)
        except ValueError:
            raise ValueError("Post not found")
            
        # Check if like already exists
        like_id = f"{user_id}_{post_id}"
        like_ref = self.db.collection(self.collection).document(like_id)
        like_doc = like_ref.get()
        
        if like_doc.exists:
            # Unlike: Delete the like document
            like_ref.delete()
            
            # Decrement like count on post
            self.db.collection('posts').document(post_id).update({
                'likes': firestore.Increment(-1)
            })
            
            return {
                'liked': False,
                'postId': post_id,
                'likeCount': post['likes'] - 1
            }
        else:
            # Like: Create like document
            like_data = {
                'userId': user_id,
                'postId': post_id,
                'createdAt': firestore.SERVER_TIMESTAMP
            }
            
            like_ref.set(like_data)
            
            # Increment like count on post
            self.db.collection('posts').document(post_id).update({
                'likes': firestore.Increment(1)
            })
            
            return {
                'liked': True,
                'postId': post_id,
                'likeCount': post['likes'] + 1
            }
    
    def check_status(self, user_id: str, post_id: str) -> bool:
        """Check if user has liked a post
        
        Args:
            user_id: The ID of the user
            post_id: The ID of the post
            
        Returns:
            Boolean indicating if the post is liked by the user
        """
        like_id = f"{user_id}_{post_id}"
        like_doc = self.db.collection(self.collection).document(like_id).get()
        return like_doc.exists
    
    def get_user_likes(self, user_id: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Get posts liked by a user
        
        Args:
            user_id: The ID of the user
            query_params: Dict containing pagination parameters
            
        Returns:
            Dict containing liked posts and pagination info
        """
        # Start with base query
        query = self.db.collection(self.collection).where('userId', '==', user_id)
        
        # Apply sorting - newest first by default
        query = query.order_by('createdAt', direction=firestore.Query.DESCENDING)
        
        # Pagination
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Execute query
        like_docs = query.limit(limit).offset(offset).stream()
        post_ids = [doc.to_dict()['postId'] for doc in like_docs]
        
        # Fetch the actual posts
        posts = []
        for post_id in post_ids:
            try:
                post = self.post_model.get(post_id)
                posts.append(post)
            except ValueError:
                # Skip posts that no longer exist
                continue
                
        # Get total count
        total_query = self.db.collection(self.collection).where('userId', '==', user_id).stream()
        total = sum(1 for _ in total_query)
            
        return {
            'posts': posts,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }


class Follow:
    """Model for user following relationships"""
    
    def __init__(self, db=None):
        """Initialize the Follow model with database reference"""
        self.db = db or firebase_admin.firestore.client()
        self.collection = "follows"
    
    def toggle(self, follower_id: str, following_id: str) -> Dict[str, Any]:
        """Toggle follow status between two users
        
        Args:
            follower_id: The ID of the user doing the following
            following_id: The ID of the user being followed
            
        Returns:
            Dict containing the updated follow status
            
        Raises:
            ValueError: If users not found or trying to follow self
        """
        # Prevent self-following
        if follower_id == following_id:
            raise ValueError("Cannot follow yourself")
            
        # Verify both users exist
        follower_doc = self.db.collection('users').document(follower_id).get()
        following_doc = self.db.collection('users').document(following_id).get()
        
        if not follower_doc.exists:
            raise ValueError("Follower user not found")
            
        if not following_doc.exists:
            raise ValueError("Following user not found")
            
        # Check if follow relationship already exists
        follow_id = f"{follower_id}_{following_id}"
        follow_ref = self.db.collection(self.collection).document(follow_id)
        follow_doc = follow_ref.get()
        
        if follow_doc.exists:
            # Unfollow: Delete the follow document
            follow_ref.delete()
            
            # Update follower counts
            self.db.collection('users').document(follower_id).update({
                'following_count': firestore.Increment(-1)
            })
            
            self.db.collection('users').document(following_id).update({
                'follower_count': firestore.Increment(-1)
            })
            
            return {
                'following': False,
                'followingId': following_id
            }
        else:
            # Follow: Create follow document
            follow_data = {
                'followerId': follower_id,
                'followingId': following_id,
                'createdAt': firestore.SERVER_TIMESTAMP
            }
            
            follow_ref.set(follow_data)
            
            # Update follower counts
            self.db.collection('users').document(follower_id).update({
                'following_count': firestore.Increment(1)
            })
            
            self.db.collection('users').document(following_id).update({
                'follower_count': firestore.Increment(1)
            })
            
            return {
                'following': True,
                'followingId': following_id
            }
    
    def check_status(self, follower_id: str, following_id: str) -> bool:
        """Check if one user follows another
        
        Args:
            follower_id: The ID of the potential follower
            following_id: The ID of the potentially followed user
            
        Returns:
            Boolean indicating if follow relationship exists
        """
        follow_id = f"{follower_id}_{following_id}"
        follow_doc = self.db.collection(self.collection).document(follow_id).get()
        return follow_doc.exists
    
    def get_followers(self, user_id: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Get users who follow a specific user
        
        Args:
            user_id: The ID of the user whose followers to get
            query_params: Dict containing pagination parameters
            
        Returns:
            Dict containing followers and pagination info
        """
        # Start with base query
        query = self.db.collection(self.collection).where('followingId', '==', user_id)
        
        # Apply sorting
        query = query.order_by('createdAt', direction=firestore.Query.DESCENDING)
        
        # Pagination
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Execute query
        follow_docs = query.limit(limit).offset(offset).stream()
        
        # Get the follower user profiles
        followers = []
        for doc in follow_docs:
            follow_data = doc.to_dict()
            follower_id = follow_data['followerId']
            
            user_doc = self.db.collection('users').document(follower_id).get()
            if user_doc.exists:
                user = user_doc.to_dict()
                user['id'] = user_doc.id
                followers.append(user)
                
        # Get total count
        total_query = self.db.collection(self.collection).where('followingId', '==', user_id).stream()
        total = sum(1 for _ in total_query)
            
        return {
            'followers': followers,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }
    
    def get_following(self, user_id: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Get users that a specific user follows
        
        Args:
            user_id: The ID of the user whose followings to get
            query_params: Dict containing pagination parameters
            
        Returns:
            Dict containing followed users and pagination info
        """
        # Start with base query
        query = self.db.collection(self.collection).where('followerId', '==', user_id)
        
        # Apply sorting
        query = query.order_by('createdAt', direction=firestore.Query.DESCENDING)
        
        # Pagination
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Execute query
        follow_docs = query.limit(limit).offset(offset).stream()
        
        # Get the following user profiles
        following = []
        for doc in follow_docs:
            follow_data = doc.to_dict()
            following_id = follow_data['followingId']
            
            user_doc = self.db.collection('users').document(following_id).get()
            if user_doc.exists:
                user = user_doc.to_dict()
                user['id'] = user_doc.id
                following.append(user)
                
        # Get total count
        total_query = self.db.collection(self.collection).where('followerId', '==', user_id).stream()
        total = sum(1 for _ in total_query)
            
        return {
            'following': following,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }