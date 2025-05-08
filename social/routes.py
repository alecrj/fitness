from flask import Blueprint, jsonify, request
from utils.firebase_admin import auth_required
import firebase_admin
from firebase_admin import firestore, storage
from datetime import datetime
import uuid
import base64
from social.models import Post, Comment, Like, Follow

# Create blueprint
social_bp = Blueprint('social', __name__)

# Initialize model instances
post_model = Post()
comment_model = Comment()
like_model = Like()
follow_model = Follow()


@social_bp.route('/posts', methods=['POST'])
@auth_required
def create_post(user_id):
    """Create a new social post"""
    try:
        data = request.get_json()
        
        # Handle image upload if provided
        image_url = None
        image_base64 = data.pop('imageBase64', None)
        
        if image_base64:
            bucket = firebase_admin.storage.bucket()
            image_data = base64.b64decode(image_base64)
            image_path = f"social/posts/{user_id}/{uuid.uuid4()}.jpg"
            blob = bucket.blob(image_path)
            blob.upload_from_string(image_data, content_type='image/jpeg')
            image_url = blob.public_url
            data['imageUrl'] = image_url
            
        # Create post using model
        post = post_model.create(user_id, data)
        return jsonify(post), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to create post: {str(e)}"}), 500


@social_bp.route('/posts', methods=['GET'])
@auth_required
def get_posts(user_id):
    """Get social posts with filtering and pagination"""
    try:
        # Extract query parameters
        query_params = {
            'limit': request.args.get('limit', 20),
            'offset': request.args.get('offset', 0),
            'userId': request.args.get('userId'),
            'tag': request.args.get('tag'),
            'recipeId': request.args.get('recipeId'),
            'mealId': request.args.get('mealId')
        }
        
        # Get feed type
        feed_type = request.args.get('feed', 'all')
        
        # If looking for personal feed, set user filter
        if feed_type == 'profile' and not query_params['userId']:
            query_params['userId'] = user_id
            
        # If looking for following feed, we need to get followed users
        if feed_type == 'following':
            # This requires custom handling since we need posts from followed users
            # Get users that the current user follows
            following_result = follow_model.get_following(
                user_id, {'limit': 100, 'offset': 0}
            )
            following_users = following_result['following']
            following_ids = [user['id'] for user in following_users]
            
            # Include the user's own posts
            following_ids.append(user_id)
            
            # Will be handled in the model's list method
            query_params['userIds'] = following_ids
            
        # Get posts using model
        result = post_model.list(query_params)
        
        # Add like status for each post
        for post in result['posts']:
            post['liked'] = like_model.check_status(user_id, post['id'])
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f"Failed to get posts: {str(e)}"}), 500


@social_bp.route('/posts/<post_id>', methods=['GET'])
@auth_required
def get_post(user_id, post_id):
    """Get a specific post by ID"""
    try:
        post = post_model.get(post_id)
        
        # Add like status
        post['liked'] = like_model.check_status(user_id, post_id)
        
        return jsonify(post)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f"Failed to get post: {str(e)}"}), 500


@social_bp.route('/posts/<post_id>', methods=['PUT'])
@auth_required
def update_post(user_id, post_id):
    """Update a post"""
    try:
        data = request.get_json()
        
        # Handle image update if provided
        image_base64 = data.pop('imageBase64', None)
        if image_base64:
            # Get existing post to find old image
            existing_post = post_model.get(post_id)
            
            bucket = firebase_admin.storage.bucket()
            
            # Delete old image if it exists
            if existing_post.get('imageUrl'):
                try:
                    # Extract image path from URL
                    old_image_path = existing_post.get('imageUrl').split('/')[-1]
                    old_blob = bucket.blob(f"social/posts/{user_id}/{old_image_path}")
                    old_blob.delete()
                except Exception:
                    # Continue even if old image deletion fails
                    pass
                    
            # Upload new image
            image_data = base64.b64decode(image_base64)
            image_path = f"social/posts/{user_id}/{uuid.uuid4()}.jpg"
            blob = bucket.blob(image_path)
            blob.upload_from_string(image_data, content_type='image/jpeg')
            data['imageUrl'] = blob.public_url
            
        # Update post using model
        updated_post = post_model.update(post_id, user_id, data)
        return jsonify(updated_post)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to update post: {str(e)}"}), 500


@social_bp.route('/posts/<post_id>', methods=['DELETE'])
@auth_required
def delete_post(user_id, post_id):
    """Delete a post"""
    try:
        # Get the post first to check for images
        post = post_model.get(post_id)
        
        # Delete associated image if it exists
        if post.get('imageUrl'):
            try:
                bucket = firebase_admin.storage.bucket()
                # Extract image path from URL
                image_path = post.get('imageUrl').split('/')[-1]
                blob = bucket.blob(f"social/posts/{user_id}/{image_path}")
                blob.delete()
            except Exception:
                # Continue even if image deletion fails
                pass
                
        # Delete post using model
        post_model.delete(post_id, user_id)
        return jsonify({'message': 'Post deleted successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to delete post: {str(e)}"}), 500


@social_bp.route('/posts/<post_id>/like', methods=['POST'])
@auth_required
def toggle_like(user_id, post_id):
    """Toggle like status for a post"""
    try:
        result = like_model.toggle(user_id, post_id)
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to toggle like: {str(e)}"}), 500


@social_bp.route('/posts/<post_id>/comments', methods=['POST'])
@auth_required
def create_comment(user_id, post_id):
    """Create a comment on a post"""
    try:
        data = request.get_json()
        data['postId'] = post_id
        
        comment = comment_model.create(user_id, data)
        return jsonify(comment), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to create comment: {str(e)}"}), 500


@social_bp.route('/posts/<post_id>/comments', methods=['GET'])
@auth_required
def get_comments(user_id, post_id):
    """Get comments for a post"""
    try:
        query_params = {
            'limit': request.args.get('limit', 20),
            'offset': request.args.get('offset', 0),
            'sort_by': request.args.get('sort_by', 'createdAt'),
            'sort_dir': request.args.get('sort_dir', 'asc')  # Show oldest first by default
        }
        
        result = comment_model.list_for_post(post_id, query_params)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f"Failed to get comments: {str(e)}"}), 500


@social_bp.route('/comments/<comment_id>', methods=['DELETE'])
@auth_required
def delete_comment(user_id, comment_id):
    """Delete a comment"""
    try:
        comment_model.delete(comment_id, user_id)
        return jsonify({'message': 'Comment deleted successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to delete comment: {str(e)}"}), 500


@social_bp.route('/users/<target_user_id>/follow', methods=['POST'])
@auth_required
def toggle_follow(user_id, target_user_id):
    """Toggle follow status for a user"""
    try:
        result = follow_model.toggle(user_id, target_user_id)
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to toggle follow: {str(e)}"}), 500


@social_bp.route('/users/<target_user_id>/followers', methods=['GET'])
@auth_required
def get_followers(user_id, target_user_id):
    """Get followers for a user"""
    try:
        query_params = {
            'limit': request.args.get('limit', 20),
            'offset': request.args.get('offset', 0)
        }
        
        result = follow_model.get_followers(target_user_id, query_params)
        
        # Add following status for each user
        for follower in result['followers']:
            follower['following'] = follow_model.check_status(user_id, follower['id'])
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f"Failed to get followers: {str(e)}"}), 500


@social_bp.route('/users/<target_user_id>/following', methods=['GET'])
@auth_required
def get_following(user_id, target_user_id):
    """Get users that a user follows"""
    try:
        query_params = {
            'limit': request.args.get('limit', 20),
            'offset': request.args.get('offset', 0)
        }
        
        result = follow_model.get_following(target_user_id, query_params)
        
        # Add following status for each user
        for following_user in result['following']:
            following_user['following'] = follow_model.check_status(user_id, following_user['id'])
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f"Failed to get following: {str(e)}"}), 500


@social_bp.route('/users/me/likes', methods=['GET'])
@auth_required
def get_liked_posts(user_id):
    """Get posts liked by the current user"""
    try:
        query_params = {
            'limit': request.args.get('limit', 20),
            'offset': request.args.get('offset', 0)
        }
        
        result = like_model.get_user_likes(user_id, query_params)
        
        # Add like status for each post (will always be true in this case)
        for post in result['posts']:
            post['liked'] = True
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f"Failed to get liked posts: {str(e)}"}), 500


@social_bp.route('/users/<target_user_id>/follow-status', methods=['GET'])
@auth_required
def check_follow_status(user_id, target_user_id):
    """Check if current user follows target user"""
    try:
        following = follow_model.check_status(user_id, target_user_id)
        return jsonify({'following': following})
        
    except Exception as e:
        return jsonify({'error': f"Failed to check follow status: {str(e)}"}), 500


@social_bp.route('/trending/tags', methods=['GET'])
@auth_required
def get_trending_tags(user_id):
    """Get trending tags from posts"""
    try:
        # Get limit parameter
        limit = int(request.args.get('limit', 10))
        
        # Create a Firestore reference
        db = firebase_admin.firestore.client()
        
        # This would ideally be implemented with a proper analytics system
        # For now, we'll use a simple approach based on recent posts
        posts_ref = db.collection('posts')
        recent_posts = posts_ref.order_by('createdAt', direction=firestore.Query.DESCENDING).limit(100).stream()
        
        # Count tag occurrences
        tag_counts = {}
        for post_doc in recent_posts:
            post = post_doc.to_dict()
            for tag in post.get('tags', []):
                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1
                    
        # Sort tags by count
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Return the top tags
        trending_tags = [{'tag': tag, 'count': count} for tag, count in sorted_tags[:limit]]
        
        return jsonify({'trending_tags': trending_tags})
        
    except Exception as e:
        return jsonify({'error': f"Failed to get trending tags: {str(e)}"}), 500