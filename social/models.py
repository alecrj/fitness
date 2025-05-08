from datetime import datetime
from typing import List, Dict, Any, Optional

class SocialModel:
    """Base class for social models with common methods"""
    @staticmethod
    def validate_content(content: str) -> str:
        """Validates and sanitizes user content"""
        if not content or content.strip() == "":
            raise ValueError("Content cannot be empty")
            
        # Sanitize and truncate if needed
        sanitized = content.strip()
        if len(sanitized) > 5000:  # Set a reasonable limit
            sanitized = sanitized[:5000]
            
        return sanitized

class Post(SocialModel):
    """Model for social posts"""
    def __init__(self, db_ref):
        self.db = db_ref
        self.collection = "posts"
    
    def create(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new post
        
        Args:
            user_id: The ID of the user creating the post
            data: Post content and metadata
                - content: Text content of the post
                - image_url: Optional URL to an image
                - recipe_id: Optional reference to a recipe
                - tags: Optional array of tags
                
        Returns:
            The created post with ID
        """
        # Validate required fields
        if not data.get('content') and not data.get('recipe_id') and not data.get('image_url'):
            raise ValueError("Post must have content, image, or recipe reference")
            
        # Get user profile
        user_ref = self.db.collection('users').document(user_id).get()
        if not user_ref.exists:
            raise ValueError("User profile not found")
            
        user = user_ref.to_dict()
        
        # Process content
        content = data.get('content', '')
        if content:
            content = self.validate_content(content)
            
        # Validate recipe reference if provided
        recipe_id = data.get('recipe_id')
        recipe_data = None
        if recipe_id:
            recipe_ref = self.db.collection('recipes').document(recipe_id).get()
            if not recipe_ref.exists:
                raise ValueError("Recipe not found")
                
            recipe = recipe_ref.to_dict()
            # Check if recipe belongs to user or is public
            if recipe.get('userId') != user_id and not recipe.get('isPublic', False):
                raise ValueError("Cannot share private recipe")
                
            # Include basic recipe info
            recipe_data = {
                'id': recipe_id,
                'title': recipe.get('title'),
                'imageUrl': recipe.get('imageUrl'),
                'description': recipe.get('description', '')
            }
            
        # Create post document
        post = {
            'userId': user_id,
            'userName': user.get('name', 'User'),
            'userProfileImage': user.get('profile_image_url'),
            'content': content,
            'imageUrl': data.get('image_url'),
            'recipeId': recipe_id,
            'recipeData': recipe_data,
            'tags': data.get('tags', []),
            'likeCount': 0,
            'commentCount': 0,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
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
            The post with ID
            
        Raises:
            ValueError: If post not found
        """
        doc = self.db.collection(self.collection).document(post_id).get()
        
        if not doc.exists:
            raise ValueError("Post not found")
            
        post = doc.to_dict()
        post['id'] = doc.id
        return post
    
    def list_feed(self, user_id: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """List posts for user's feed with filtering and pagination
        
        Args:
            user_id: The ID of the user viewing the feed
            query_params: Query parameters for filtering and pagination
                - limit: Number of items per page (default: 20)
                - offset: Starting offset for pagination (default: 0)
                - tag: Filter by specific tag
                - user_id: Filter by specific user
                
        Returns:
            Dict with posts array and pagination info
        """
        # Get pagination params
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Start with base query
        query = self.db.collection(self.collection).order_by('createdAt', direction=self.db.Query.DESCENDING)
        
        # Apply filters
        tag_filter = query_params.get('tag')
        if tag_filter:
            query = query.where('tags', 'array_contains', tag_filter)
            
        specific_user = query_params.get('user_id')
        if specific_user:
            query = query.where('userId', '==', specific_user)
        
        # Execute query
        posts = []
        # Get total first for pagination
        all_posts = [doc for doc in query.stream()]
        total = len(all_posts)
        
        # Apply pagination in memory
        for doc in all_posts[offset:offset+limit]:
            post = doc.to_dict()
            post['id'] = doc.id
            
            # Add user's like status
            post['userLiked'] = False
            try:
                like_ref = self.db.collection('likes').document(f"{user_id}_{doc.id}").get()
                if like_ref.exists:
                    post['userLiked'] = True
            except:
                pass
                
            posts.append(post)
            
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
            post_id: The ID of the post to update
            user_id: The ID of the user updating the post
            data: Updated post data
                - content: New text content
                - tags: New tags array
                
        Returns:
            The updated post
            
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
            raise ValueError("Not authorized to update this post")
            
        # Process content if provided
        if 'content' in data:
            data['content'] = self.validate_content(data['content'])
            
        # Update the document
        update_data = {
            'content': data.get('content', post.get('content', '')),
            'tags': data.get('tags', post.get('tags', [])),
            'updatedAt': datetime.utcnow()
        }
        
        doc_ref.update(update_data)
        
        # Return updated post
        updated_post = post.copy()
        updated_post.update(update_data)
        updated_post['id'] = post_id
        
        return updated_post
    
    def delete(self, post_id: str, user_id: str) -> bool:
        """Delete a post
        
        Args:
            post_id: The ID of the post to delete
            user_id: The ID of the user deleting the post
            
        Returns:
            True if successful
            
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
            raise ValueError("Not authorized to delete this post")
            
        # Delete comments
        comments_ref = self.db.collection('comments').where('postId', '==', post_id).stream()
        for comment_doc in comments_ref:
            comment_doc.reference.delete()
            
        # Delete likes
        likes_ref = self.db.collection('likes').where('postId', '==', post_id).stream()
        for like_doc in likes_ref:
            like_doc.reference.delete()
            
        # Delete the post
        doc_ref.delete()
        return True
    
    def like(self, post_id: str, user_id: str) -> Dict[str, Any]:
        """Like a post
        
        Args:
            post_id: The ID of the post to like
            user_id: The ID of the user liking the post
            
        Returns:
            Dict with updated like count and status
        """
        # Check if post exists
        post_ref = self.db.collection(self.collection).document(post_id)
        post = post_ref.get()
        
        if not post.exists:
            raise ValueError("Post not found")
            
        # Check if already liked
        like_id = f"{user_id}_{post_id}"
        like_ref = self.db.collection('likes').document(like_id).get()
        
        if like_ref.exists:
            # Already liked, so unlike
            self.db.collection('likes').document(like_id).delete()
            
            # Decrement like count
            post_ref.update({
                'likeCount': self.db.Increment(-1)
            })
            
            return {
                'postId': post_id,
                'liked': False,
                'likeCount': post.to_dict().get('likeCount', 1) - 1
            }
        else:
            # Not liked, so add like
            like_data = {
                'userId': user_id,
                'postId': post_id,
                'createdAt': datetime.utcnow()
            }
            
            self.db.collection('likes').document(like_id).set(like_data)
            
            # Increment like count
            post_ref.update({
                'likeCount': self.db.Increment(1)
            })
            
            return {
                'postId': post_id,
                'liked': True,
                'likeCount': post.to_dict().get('likeCount', 0) + 1
            }

class Comment(SocialModel):
    """Model for post comments"""
    def __init__(self, db_ref):
        self.db = db_ref
        self.collection = "comments"
    
    def create(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new comment
        
        Args:
            user_id: The ID of the user creating the comment
            data: Comment content and metadata
                - post_id: ID of the post being commented on
                - content: Text content of the comment
                
        Returns:
            The created comment with ID
        """
        # Validate required fields
        if not data.get('post_id'):
            raise ValueError("Post ID is required")
            
        if not data.get('content'):
            raise ValueError("Comment content is required")
            
        post_id = data.get('post_id')
            
        # Check if post exists
        post_ref = self.db.collection('posts').document(post_id)
        post = post_ref.get()
        
        if not post.exists:
            raise ValueError("Post not found")
            
        # Get user profile
        user_ref = self.db.collection('users').document(user_id).get()
        if not user_ref.exists:
            raise ValueError("User profile not found")
            
        user = user_ref.to_dict()
            
        # Process content
        content = self.validate_content(data.get('content', ''))
            
        # Create comment document
        comment = {
            'userId': user_id,
            'userName': user.get('name', 'User'),
            'userProfileImage': user.get('profile_image_url'),
            'postId': post_id,
            'content': content,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        
        # Save to database
        doc_ref = self.db.collection(self.collection).document()
        doc_ref.set(comment)
        
        # Increment comment count on post
        post_ref.update({
            'commentCount': self.db.Increment(1)
        })
        
        # Return with ID
        comment['id'] = doc_ref.id
        return comment
    
    def list(self, post_id: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """List comments for a post with pagination
        
        Args:
            post_id: The ID of the post to get comments for
            query_params: Query parameters for pagination
                - limit: Number of items per page (default: 20)
                - offset: Starting offset for pagination (default: 0)
                
        Returns:
            Dict with comments array and pagination info
        """
        # Get pagination params
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Query comments for post
        query = self.db.collection(self.collection) \
            .where('postId', '==', post_id) \
            .order_by('createdAt', direction=self.db.Query.ASCENDING)
            
        # Execute query
        comments = []
        # Get total first for pagination
        all_comments = [doc for doc in query.stream()]
        total = len(all_comments)
        
        # Apply pagination in memory
        for doc in all_comments[offset:offset+limit]:
            comment = doc.to_dict()
            comment['id'] = doc.id
            comments.append(comment)
            
        return {
            'comments': comments,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }
    
    def update(self, comment_id: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a comment
        
        Args:
            comment_id: The ID of the comment to update
            user_id: The ID of the user updating the comment
            data: Updated comment data
                - content: New text content
                
        Returns:
            The updated comment
            
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
            raise ValueError("Not authorized to update this comment")
            
        # Process content
        content = self.validate_content(data.get('content', ''))
            
        # Update the document
        update_data = {
            'content': content,
            'updatedAt': datetime.utcnow()
        }
        
        doc_ref.update(update_data)
        
        # Return updated comment
        updated_comment = comment.copy()
        updated_comment.update(update_data)
        updated_comment['id'] = comment_id
        
        return updated_comment
    
    def delete(self, comment_id: str, user_id: str) -> bool:
        """Delete a comment
        
        Args:
            comment_id: The ID of the comment to delete
            user_id: The ID of the user deleting the comment
            
        Returns:
            True if successful
            
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
            raise ValueError("Not authorized to delete this comment")
            
        # Get post to update comment count
        post_id = comment.get('postId')
        post_ref = self.db.collection('posts').document(post_id)
        
        # Delete the comment
        doc_ref.delete()
        
        # Decrement comment count on post
        post_ref.update({
            'commentCount': self.db.Increment(-1)
        })
        
        return True

class Connection(SocialModel):
    """Model for user connections (following/followers)"""
    def __init__(self, db_ref):
        self.db = db_ref
        self.collection = "connections"
    
    def follow(self, follower_id: str, followed_id: str) -> Dict[str, Any]:
        """Follow a user
        
        Args:
            follower_id: The ID of the user following
            followed_id: The ID of the user being followed
            
        Returns:
            Dict with connection status
        """
        # Check if users exist
        if follower_id == followed_id:
            raise ValueError("Cannot follow yourself")
            
        follower_ref = self.db.collection('users').document(follower_id).get()
        if not follower_ref.exists:
            raise ValueError("Follower user not found")
            
        followed_ref = self.db.collection('users').document(followed_id).get()
        if not followed_ref.exists:
            raise ValueError("User to follow not found")
            
        # Check if already following
        connection_id = f"{follower_id}_{followed_id}"
        connection_ref = self.db.collection(self.collection).document(connection_id).get()
        
        if connection_ref.exists:
            # Already following, so unfollow
            self.db.collection(self.collection).document(connection_id).delete()
            
            # Update follower and following counts
            self.db.collection('users').document(follower_id).update({
                'followingCount': self.db.Increment(-1)
            })
            
            self.db.collection('users').document(followed_id).update({
                'followerCount': self.db.Increment(-1)
            })
            
            return {
                'following': False,
                'followerId': follower_id,
                'followedId': followed_id
            }
        else:
            # Not following, so add connection
            connection_data = {
                'followerId': follower_id,
                'followedId': followed_id,
                'createdAt': datetime.utcnow()
            }
            
            self.db.collection(self.collection).document(connection_id).set(connection_data)
            
            # Update follower and following counts
            self.db.collection('users').document(follower_id).update({
                'followingCount': self.db.Increment(1)
            })
            
            self.db.collection('users').document(followed_id).update({
                'followerCount': self.db.Increment(1)
            })
            
            return {
                'following': True,
                'followerId': follower_id,
                'followedId': followed_id
            }
    
    def get_following_status(self, follower_id: str, followed_id: str) -> Dict[str, bool]:
        """Check if user is following another user
        
        Args:
            follower_id: The ID of the potential follower
            followed_id: The ID of the potentially followed user
            
        Returns:
            Dict with following status
        """
        connection_id = f"{follower_id}_{followed_id}"
        connection_ref = self.db.collection(self.collection).document(connection_id).get()
        
        return {
            'following': connection_ref.exists
        }
    
    def list_followers(self, user_id: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """List followers for a user with pagination
        
        Args:
            user_id: The ID of the user to get followers for
            query_params: Query parameters for pagination
                - limit: Number of items per page (default: 20)
                - offset: Starting offset for pagination (default: 0)
                
        Returns:
            Dict with followers array and pagination info
        """
        # Get pagination params
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Query connections where user is being followed
        query = self.db.collection(self.collection) \
            .where('followedId', '==', user_id) \
            .order_by('createdAt', direction=self.db.Query.DESCENDING)
            
        # Execute query
        followers = []
        # Get total first for pagination
        all_connections = [doc for doc in query.stream()]
        total = len(all_connections)
        
        # Apply pagination in memory
        for doc in all_connections[offset:offset+limit]:
            connection = doc.to_dict()
            
            # Get follower user details
            follower_id = connection.get('followerId')
            follower_ref = self.db.collection('users').document(follower_id).get()
            
            if follower_ref.exists:
                follower = follower_ref.to_dict()
                followers.append({
                    'id': follower_id,
                    'name': follower.get('name', 'User'),
                    'profileImage': follower.get('profile_image_url'),
                    'followingSince': connection.get('createdAt')
                })
            
        return {
            'followers': followers,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }
    
    def list_following(self, user_id: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """List users that a user is following with pagination
        
        Args:
            user_id: The ID of the user to get following list for
            query_params: Query parameters for pagination
                - limit: Number of items per page (default: 20)
                - offset: Starting offset for pagination (default: 0)
                
        Returns:
            Dict with following array and pagination info
        """
        # Get pagination params
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Query connections where user is following
        query = self.db.collection(self.collection) \
            .where('followerId', '==', user_id) \
            .order_by('createdAt', direction=self.db.Query.DESCENDING)
            
        # Execute query
        following = []
        # Get total first for pagination
        all_connections = [doc for doc in query.stream()]
        total = len(all_connections)
        
        # Apply pagination in memory
        for doc in all_connections[offset:offset+limit]:
            connection = doc.to_dict()
            
            # Get followed user details
            followed_id = connection.get('followedId')
            followed_ref = self.db.collection('users').document(followed_id).get()
            
            if followed_ref.exists:
                followed = followed_ref.to_dict()
                following.append({
                    'id': followed_id,
                    'name': followed.get('name', 'User'),
                    'profileImage': followed.get('profile_image_url'),
                    'followingSince': connection.get('createdAt')
                })
            
        return {
            'following': following,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }