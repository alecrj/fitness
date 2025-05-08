from flask import Blueprint, jsonify, request
from utils.firebase_admin import auth_required
import firebase_admin
from firebase_admin import firestore, storage
from datetime import datetime
import uuid
import base64
from io import BytesIO
import requests
from recipe_scrapers import scrape_me, WebsiteNotImplementedError, SCRAPERS
import re
from bs4 import BeautifulSoup
import json
import urllib.parse
from config import Config

# Create blueprint
recipes_bp = Blueprint('recipes', __name__)
db = firebase_admin.firestore.client()
bucket = firebase_admin.storage.bucket()

# Helper function to extract Instagram URLs
def extract_instagram_url(url):
    """Extract clean Instagram URL from potential app links or other formats"""
    instagram_pattern = r'(https?://(?:www\.)?instagram\.com/[^/]+/[^/]+/[^/?]+)'
    match = re.search(instagram_pattern, url)
    if match:
        return match.group(1)
    return url

@recipes_bp.route('/import', methods=['POST'])
@auth_required
def import_recipe(user_id):
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
        
    try:
        # Handle Instagram URLs differently
        if 'instagram.com' in url or 'instagram.' in url:
            return handle_instagram_recipe(url, user_id)
        
        # For all other URLs, use recipe_scrapers
        scraper = scrape_me(url)
        
        recipe = {
            'userId': user_id,
            'url': url,
            'title': scraper.title(),
            'image': scraper.image(),
            'total_time': scraper.total_time(),
            'yields': scraper.yields(),
            'ingredients': scraper.ingredients(),
            'instructions': scraper.instructions_list(),
            'nutrients': scraper.nutrients(),
            'createdAt': firestore.SERVER_TIMESTAMP,
            'updatedAt': firestore.SERVER_TIMESTAMP,
            'source': 'web',
            'sourceUrl': url
        }
        
        # Save recipe image to Firebase Storage
        if recipe['image']:
            try:
                image_response = requests.get(recipe['image'])
                if image_response.status_code == 200:
                    image_path = f"recipes/{user_id}/{uuid.uuid4()}.jpg"
                    blob = bucket.blob(image_path)
                    blob.upload_from_string(image_response.content, content_type='image/jpeg')
                    recipe['imageStoragePath'] = image_path
                    recipe['imageUrl'] = blob.public_url
            except Exception as img_error:
                # Continue even if image saving fails
                print(f"Error saving recipe image: {str(img_error)}")
                
        # Save recipe to Firestore
        doc_ref = db.collection('recipes').document()
        doc_ref.set(recipe)
        
        # Return with ID
        recipe['id'] = doc_ref.id
        
        return jsonify(recipe), 201
        
    except WebsiteNotImplementedError:
        return jsonify({'error': 'This website is not supported for recipe scraping'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def handle_instagram_recipe(url, user_id):
    """Custom handler for scraping recipes from Instagram posts"""
    cleaned_url = extract_instagram_url(url)
    
    try:
        # For Instagram, we need to use a different approach
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(cleaned_url, headers=headers)
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to retrieve content from Instagram'}), 500
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract metadata from Instagram
        # This is a simplified approach and may need adjustments based on Instagram's structure
        meta_tags = soup.find_all('meta')
        
        title = None
        description = None
        image_url = None
        
        for tag in meta_tags:
            if tag.get('property') == 'og:title':
                title = tag.get('content')
            elif tag.get('property') == 'og:description':
                description = tag.get('content')
            elif tag.get('property') == 'og:image':
                image_url = tag.get('content')
        
        # Parse caption for ingredients and instructions
        ingredients = []
        instructions = []
        
        if description:
            # Simple heuristic: lines that start with numbers or bullets are likely ingredients
            lines = description.split('\n')
            for line in lines:
                line = line.strip()
                if re.match(r'^[\d\-\*\•\◾\▪\-]\s', line) or 'ingredient' in line.lower():
                    ingredients.append(line)
                elif len(line) > 20:  # Longer lines might be instructions
                    instructions.append(line)
        
        recipe = {
            'userId': user_id,
            'url': cleaned_url,
            'title': title or "Instagram Recipe",
            'image': image_url,
            'ingredients': ingredients,
            'instructions': instructions,
            'description': description,
            'createdAt': firestore.SERVER_TIMESTAMP,
            'updatedAt': firestore.SERVER_TIMESTAMP,
            'source': 'instagram',
            'sourceUrl': cleaned_url,
            'needsReview': True  # Flag for user to review and edit
        }
        
        # Save recipe image to Firebase Storage
        if image_url:
            try:
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_path = f"recipes/{user_id}/{uuid.uuid4()}.jpg"
                    blob = bucket.blob(image_path)
                    blob.upload_from_string(image_response.content, content_type='image/jpeg')
                    recipe['imageStoragePath'] = image_path
                    recipe['imageUrl'] = blob.public_url
            except Exception as img_error:
                # Continue even if image saving fails
                print(f"Error saving Instagram image: {str(img_error)}")
        
        # Save recipe to Firestore
        doc_ref = db.collection('recipes').document()
        doc_ref.set(recipe)
        
        # Return with ID
        recipe['id'] = doc_ref.id
        
        return jsonify(recipe), 201
        
    except Exception as e:
        return jsonify({'error': f"Failed to import Instagram recipe: {str(e)}"}), 500

@recipes_bp.route('/supported-sites', methods=['GET'])
def get_supported_sites():
    # Return list of supported recipe websites for scraping
    supported_sites = list(SCRAPERS.keys())
    return jsonify({'supported_sites': supported_sites})

@recipes_bp.route('', methods=['GET'])
@auth_required
def get_recipes(user_id):
    try:
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        
        query = db.collection('recipes').where('userId', '==', user_id).order_by('createdAt', direction=firestore.Query.DESCENDING)
        
        # Get total count (for pagination)
        total_query = query.stream()
        total = sum(1 for _ in total_query)
        
        # Get current page
        recipes_docs = query.offset(offset).limit(limit).stream()
        
        recipes = []
        for doc in recipes_docs:
            recipe = doc.to_dict()
            recipe['id'] = doc.id
            recipes.append(recipe)
            
        return jsonify({
            'recipes': recipes,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipes_bp.route('/<recipe_id>', methods=['GET'])
@auth_required
def get_recipe(user_id, recipe_id):
    try:
        doc_ref = db.collection('recipes').document(recipe_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'Recipe not found'}), 404
            
        recipe = doc.to_dict()
        
        # Check ownership or public status
        if recipe.get('userId') != user_id and not recipe.get('isPublic', False):
            return jsonify({'error': 'Unauthorized'}), 403
            
        recipe['id'] = doc.id
        return jsonify(recipe)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipes_bp.route('', methods=['POST'])
@auth_required
def create_recipe(user_id):
    data = request.get_json()
    
    required_fields = ['title', 'ingredients', 'instructions']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
        
    try:
        recipe = {
            'userId': user_id,
            'title': data['title'],
            'description': data.get('description', ''),
            'ingredients': data['ingredients'],
            'instructions': data['instructions'],
            'prepTime': data.get('prepTime'),
            'cookTime': data.get('cookTime'),
            'servings': data.get('servings'),
            'difficulty': data.get('difficulty'),
            'cuisine': data.get('cuisine'),
            'tags': data.get('tags', []),
            'createdAt': firestore.SERVER_TIMESTAMP,
            'updatedAt': firestore.SERVER_TIMESTAMP,
            'isPublic': data.get('isPublic', False),
            'source': 'user',
            'nutrition': data.get('nutrition', {})
        }
        
        # Handle recipe image if provided as base64
        image_base64 = data.get('imageBase64')
        if image_base64:
            image_data = base64.b64decode(image_base64)
            image_path = f"recipes/{user_id}/{uuid.uuid4()}.jpg"
            blob = bucket.blob(image_path)
            blob.upload_from_string(image_data, content_type='image/jpeg')
            recipe['imageStoragePath'] = image_path
            recipe['imageUrl'] = blob.public_url
            
        # Save to Firestore
        doc_ref = db.collection('recipes').document()
        doc_ref.set(recipe)
        
        # Return with ID
        recipe['id'] = doc_ref.id
        
        return jsonify(recipe), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipes_bp.route('/<recipe_id>', methods=['PUT'])
@auth_required
def update_recipe(user_id, recipe_id):
    data = request.get_json()
    
    try:
        # Get the recipe and verify ownership
        doc_ref = db.collection('recipes').document(recipe_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'Recipe not found'}), 404
            
        recipe = doc.to_dict()
        if recipe.get('userId') != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        # Update fields
        update_data = {
            'title': data.get('title', recipe.get('title')),
            'description': data.get('description', recipe.get('description', '')),
            'ingredients': data.get('ingredients', recipe.get('ingredients', [])),
            'instructions': data.get('instructions', recipe.get('instructions', [])),
            'prepTime': data.get('prepTime', recipe.get('prepTime')),
            'cookTime': data.get('cookTime', recipe.get('cookTime')),
            'servings': data.get('servings', recipe.get('servings')),
            'difficulty': data.get('difficulty', recipe.get('difficulty')),
            'cuisine': data.get('cuisine', recipe.get('cuisine')),
            'tags': data.get('tags', recipe.get('tags', [])),
            'isPublic': data.get('isPublic', recipe.get('isPublic', False)),
            'nutrition': data.get('nutrition', recipe.get('nutrition', {})),
            'updatedAt': firestore.SERVER_TIMESTAMP,
            'needsReview': False  # Clear the review flag when edited
        }
        
        # Handle recipe image if provided as base64
        image_base64 = data.get('imageBase64')
        if image_base64:
            # Delete old image if exists
            old_path = recipe.get('imageStoragePath')
            if old_path:
                try:
                    old_blob = bucket.blob(old_path)
                    old_blob.delete()
                except Exception:
                    pass  # Continue even if deletion fails
                    
            # Upload new image
            image_data = base64.b64decode(image_base64)
            image_path = f"recipes/{user_id}/{uuid.uuid4()}.jpg"
            blob = bucket.blob(image_path)
            blob.upload_from_string(image_data, content_type='image/jpeg')
            update_data['imageStoragePath'] = image_path
            update_data['imageUrl'] = blob.public_url
            
        # Update in Firestore
        doc_ref.update(update_data)
        
        # Return updated recipe
        updated_recipe = recipe.copy()
        updated_recipe.update(update_data)
        updated_recipe['id'] = recipe_id
        
        return jsonify(updated_recipe)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipes_bp.route('/<recipe_id>', methods=['DELETE'])
@auth_required
def delete_recipe(user_id, recipe_id):
    try:
        # Get the recipe and verify ownership
        doc_ref = db.collection('recipes').document(recipe_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'Recipe not found'}), 404
            
        recipe = doc.to_dict()
        if recipe.get('userId') != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        # Delete image if exists
        image_path = recipe.get('imageStoragePath')
        if image_path:
            try:
                blob = bucket.blob(image_path)
                blob.delete()
            except Exception:
                pass  # Continue even if image deletion fails
                
        # Delete recipe
        doc_ref.delete()
        
        return jsonify({'message': 'Recipe deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipes_bp.route('/search', methods=['GET'])
@auth_required
def search_recipes(user_id):
    query = request.args.get('q', '')
    tags = request.args.get('tags', '').split(',') if request.args.get('tags') else []
    cuisine = request.args.get('cuisine')
    difficulty = request.args.get('difficulty')
    include_public = request.args.get('includePublic', 'true').lower() == 'true'
    limit = int(request.args.get('limit', 20))
    offset = int(request.args.get('offset', 0))
    
    try:
        # Base query for user's recipes
        db_query = db.collection('recipes').where('userId', '==', user_id)
        
        # Add filters if provided
        if query:
            # Firebase doesn't support native text search, so we'll filter in memory
            # In production, consider using Algolia or a similar search service
            pass
            
        if cuisine:
            db_query = db_query.where('cuisine', '==', cuisine)
            
        if difficulty:
            db_query = db_query.where('difficulty', '==', difficulty)
            
        if tags:
            # We can only filter on one array-contains at a time
            if len(tags) > 0:
                db_query = db_query.where('tags', 'array_contains', tags[0])
                
        # Get results
        results = []
        for doc in db_query.stream():
            recipe = doc.to_dict()
            recipe['id'] = doc.id
            
            # Apply text search filter in memory
            if query and query.lower() not in recipe.get('title', '').lower() and query.lower() not in recipe.get('description', '').lower():
                continue
                
            # Apply additional tag filters in memory
            if len(tags) > 1 and not all(tag in recipe.get('tags', []) for tag in tags[1:]):
                continue
                
            results.append(recipe)
            
        # If requested, also get public recipes from other users
        if include_public:
            public_query = db.collection('recipes').where('isPublic', '==', True).where('userId', '!=', user_id)
            
            # Apply same filters
            if cuisine:
                public_query = public_query.where('cuisine', '==', cuisine)
                
            if difficulty:
                public_query = public_query.where('difficulty', '==', difficulty)
                
            if tags and len(tags) > 0:
                public_query = public_query.where('tags', 'array_contains', tags[0])
                
            # Get public results
            for doc in public_query.stream():
                recipe = doc.to_dict()
                recipe['id'] = doc.id
                
                # Apply text search filter in memory
                if query and query.lower() not in recipe.get('title', '').lower() and query.lower() not in recipe.get('description', '').lower():
                    continue
                    
                # Apply additional tag filters in memory
                if len(tags) > 1 and not all(tag in recipe.get('tags', []) for tag in tags[1:]):
                    continue
                    
                results.append(recipe)
                
        # Sort by recency
        results.sort(key=lambda x: x.get('createdAt', 0), reverse=True)
        
        # Apply pagination
        paginated_results = results[offset:offset + limit] if offset < len(results) else []
        
        return jsonify({
            'recipes': paginated_results,
            'pagination': {
                'total': len(results),
                'limit': limit,
                'offset': offset
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipes_bp.route('/share/<recipe_id>', methods=['POST'])
@auth_required
def share_recipe(user_id, recipe_id):
    try:
        # Get the recipe and verify ownership
        doc_ref = db.collection('recipes').document(recipe_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'Recipe not found'}), 404
            
        recipe = doc.to_dict()
        if recipe.get('userId') != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        # Make it public
        doc_ref.update({
            'isPublic': True,
            'updatedAt': firestore.SERVER_TIMESTAMP
        })
        
        return jsonify({'message': 'Recipe shared successfully', 'isPublic': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipes_bp.route('/unshare/<recipe_id>', methods=['POST'])
@auth_required
def unshare_recipe(user_id, recipe_id):
    try:
        # Get the recipe and verify ownership
        doc_ref = db.collection('recipes').document(recipe_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'Recipe not found'}), 404
            
        recipe = doc.to_dict()
        if recipe.get('userId') != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        # Make it private
        doc_ref.update({
            'isPublic': False,
            'updatedAt': firestore.SERVER_TIMESTAMP
        })
        
        return jsonify({'message': 'Recipe is now private', 'isPublic': False})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipes_bp.route('/nutritional-analysis', methods=['POST'])
@auth_required
def analyze_recipe_nutrition(user_id):
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    
    if not ingredients:
        return jsonify({'error': 'Ingredients are required'}), 400
        
    try:
        # This is a simplified approach
        # In a production environment, you'd likely use a more robust nutrition API
        
        # For each ingredient, make a call to the USDA API
        estimated_nutrition = {
            'calories': 0,
            'protein': 0,
            'fat': 0,
            'carbs': 0,
            'fiber': 0,
            'sugar': 0
        }
        
        breakdown = []
        
        for ingredient in ingredients:
            # Clean up ingredient text for better search results
            search_term = re.sub(r'^\d+\s+\w+\s+', '', ingredient)  # Remove amount and unit
            search_term = re.sub(r'\(.*?\)', '', search_term)  # Remove content in parentheses
            
            # Search USDA for this ingredient
            response = requests.get(
                f"{Config.USDA_API_BASE_URL}/foods/search",
                params={
                    'api_key': Config.USDA_API_KEY,
                    'query': search_term,
                    'pageSize': 1
                }
            )
            
            if response.status_code == 200:
                results = response.json()
                if results.get('foods') and len(results['foods']) > 0:
                    food = results['foods'][0]
                    
                    item_nutrition = {
                        'ingredient': ingredient,
                        'fdcId': food.get('fdcId'),
                        'description': food.get('description'),
                        'calories': next((n.get('value', 0) for n in food.get('foodNutrients', []) 
                                        if n.get('nutrientName', '').lower() == 'energy' and n.get('unitName', '').lower() == 'kcal'), 0),
                        'protein': next((n.get('value', 0) for n in food.get('foodNutrients', []) 
                                      if n.get('nutrientName', '').lower() == 'protein'), 0),
                        'fat': next((n.get('value', 0) for n in food.get('foodNutrients', []) 
                                   if n.get('nutrientName', '').lower() == 'total lipid (fat)'), 0),
                        'carbs': next((n.get('value', 0) for n in food.get('foodNutrients', []) 
                                     if n.get('nutrientName', '').lower() == 'carbohydrate, by difference'), 0),
                        'fiber': next((n.get('value', 0) for n in food.get('foodNutrients', []) 
                                     if n.get('nutrientName', '').lower() == 'fiber, total dietary'), 0),
                        'sugar': next((n.get('value', 0) for n in food.get('foodNutrients', []) 
                                     if n.get('nutrientName', '').lower() == 'sugars, total including nlea'), 0)
                    }
                    
                    # Add to totals
                    estimated_nutrition['calories'] += item_nutrition['calories']
                    estimated_nutrition['protein'] += item_nutrition['protein']
                    estimated_nutrition['fat'] += item_nutrition['fat']
                    estimated_nutrition['carbs'] += item_nutrition['carbs']
                    estimated_nutrition['fiber'] += item_nutrition['fiber']
                    estimated_nutrition['sugar'] += item_nutrition['sugar']
                    
                    breakdown.append(item_nutrition)
        
        # Divide by number of servings if provided
        servings = data.get('servings', 1)
        if servings > 1:
            for key in estimated_nutrition:
                estimated_nutrition[key] = round(estimated_nutrition[key] / servings, 1)
        
        return jsonify({
            'totalNutrition': estimated_nutrition,
            'perServing': estimated_nutrition,
            'servings': servings,
            'ingredientBreakdown': breakdown
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500