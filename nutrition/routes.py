from flask import Blueprint, jsonify, request
from utils.firebase_admin import auth_required
import firebase_admin
from firebase_admin import firestore
from datetime import datetime
import uuid
import requests
from nutrition.models import FoodItem, MealLog
from config import Config

# Create blueprint
nutrition_bp = Blueprint('nutrition', __name__)

# Initialize Firebase and models
db = firebase_admin.firestore.client()
food_item_model = FoodItem(db)
meal_log_model = MealLog(db)


@nutrition_bp.route('/foods', methods=['POST'])
@auth_required
def create_food_item(user_id):
    """Create a new food item"""
    try:
        data = request.get_json()
        food_item = food_item_model.create(user_id, data)
        return jsonify(food_item), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to create food item: {str(e)}"}), 500


@nutrition_bp.route('/foods', methods=['GET'])
@auth_required
def get_food_items(user_id):
    """List food items with filtering and pagination"""
    try:
        # Extract query parameters
        query_params = {
            'limit': request.args.get('limit', 20),
            'offset': request.args.get('offset', 0),
            'is_favorite': request.args.get('is_favorite') == 'true',
            'is_custom': request.args.get('is_custom') == 'true',
            'q': request.args.get('q', ''),
            'sort_by': request.args.get('sort_by', 'created_at'),
            'sort_dir': request.args.get('sort_dir', 'desc')
        }
        
        # Get food items using model
        result = food_item_model.list(user_id, query_params)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f"Failed to get food items: {str(e)}"}), 500


@nutrition_bp.route('/foods/<food_id>', methods=['GET'])
@auth_required
def get_food_item(user_id, food_id):
    """Get a specific food item by ID"""
    try:
        food_item = food_item_model.get(food_id, user_id)
        return jsonify(food_item)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f"Failed to get food item: {str(e)}"}), 500


@nutrition_bp.route('/foods/<food_id>', methods=['PUT'])
@auth_required
def update_food_item(user_id, food_id):
    """Update a food item"""
    try:
        data = request.get_json()
        updated_item = food_item_model.update(food_id, user_id, data)
        return jsonify(updated_item)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to update food item: {str(e)}"}), 500


@nutrition_bp.route('/foods/<food_id>', methods=['DELETE'])
@auth_required
def delete_food_item(user_id, food_id):
    """Delete a food item"""
    try:
        food_item_model.delete(food_id, user_id)
        return jsonify({'message': 'Food item deleted successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to delete food item: {str(e)}"}), 500


@nutrition_bp.route('/foods/<food_id>/favorite', methods=['POST'])
@auth_required
def toggle_favorite(user_id, food_id):
    """Toggle favorite status for a food item"""
    try:
        # Get current item
        food_item = food_item_model.get(food_id, user_id)
        
        # Toggle favorite status
        is_favorite = not food_item.get('is_favorite', False)
        
        # Update item
        updated_item = food_item_model.update(food_id, user_id, {'is_favorite': is_favorite})
        
        return jsonify({'is_favorite': is_favorite})
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to toggle favorite status: {str(e)}"}), 500


@nutrition_bp.route('/foods/search', methods=['GET'])
@auth_required
def search_food_database(user_id):
    """Search for food items in USDA database"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
            
        # Make request to USDA API
        response = requests.get(
            f"{Config.USDA_API_BASE_URL}/foods/search",
            params={
                'api_key': Config.USDA_API_KEY,
                'query': query,
                'pageSize': 25
            }
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to search USDA database'}), 500
            
        results = response.json()
        
        # Format results
        foods = []
        for food in results.get('foods', []):
            formatted_food = {
                'fdcId': food.get('fdcId'),
                'name': food.get('description'),
                'brand': food.get('brandName', ''),
                'serving_size': food.get('servingSize', 100),
                'serving_unit': food.get('servingSizeUnit', 'g'),
                'nutrition': {
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
                                 if n.get('nutrientName', '').lower() == 'sugars, total including nlea'), 0),
                    'sodium': next((n.get('value', 0) for n in food.get('foodNutrients', []) 
                                  if n.get('nutrientName', '').lower() == 'sodium, na'), 0),
                    'cholesterol': next((n.get('value', 0) for n in food.get('foodNutrients', []) 
                                       if n.get('nutrientName', '').lower() == 'cholesterol'), 0)
                }
            }
            foods.append(formatted_food)
            
        return jsonify({
            'foods': foods,
            'totalHits': results.get('totalHits', 0)
        })
        
    except Exception as e:
        return jsonify({'error': f"Failed to search food database: {str(e)}"}), 500


@nutrition_bp.route('/foods/details/<fdc_id>', methods=['GET'])
@auth_required
def get_food_details(user_id, fdc_id):
    """Get detailed information about a food from USDA database"""
    try:
        # Make request to USDA API
        response = requests.get(
            f"{Config.USDA_API_BASE_URL}/food/{fdc_id}",
            params={
                'api_key': Config.USDA_API_KEY
            }
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to get food details from USDA database'}), 500
            
        food_data = response.json()
        
        # Format detailed food data
        food_details = {
            'fdcId': food_data.get('fdcId'),
            'name': food_data.get('description'),
            'brand': food_data.get('brandName', ''),
            'ingredients': food_data.get('ingredients', ''),
            'serving_size': food_data.get('servingSize', 100),
            'serving_unit': food_data.get('servingSizeUnit', 'g'),
            'category': food_data.get('foodCategory', {}).get('description', ''),
            'nutrition': {},
            'nutrients': []
        }
        
        # Extract all nutrients
        for nutrient in food_data.get('foodNutrients', []):
            if 'nutrient' in nutrient and 'amount' in nutrient:
                n = nutrient['nutrient']
                nutrient_info = {
                    'id': n.get('id'),
                    'name': n.get('name'),
                    'amount': nutrient.get('amount', 0),
                    'unit': n.get('unitName'),
                    'category': n.get('nutrientCategory', {}).get('name', '')
                }
                food_details['nutrients'].append(nutrient_info)
                
                # Add common nutrients to the nutrition object
                if n.get('name', '').lower() == 'energy' and n.get('unitName', '').lower() == 'kcal':
                    food_details['nutrition']['calories'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'protein':
                    food_details['nutrition']['protein'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'total lipid (fat)':
                    food_details['nutrition']['fat'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'carbohydrate, by difference':
                    food_details['nutrition']['carbs'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'fiber, total dietary':
                    food_details['nutrition']['fiber'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'sugars, total including nlea':
                    food_details['nutrition']['sugar'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'sodium, na':
                    food_details['nutrition']['sodium'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'cholesterol':
                    food_details['nutrition']['cholesterol'] = nutrient.get('amount', 0)
        
        return jsonify(food_details)
        
    except Exception as e:
        return jsonify({'error': f"Failed to get food details: {str(e)}"}), 500


@nutrition_bp.route('/foods/import', methods=['POST'])
@auth_required
def import_food_from_usda(user_id):
    """Import a food item from USDA database to user's food items"""
    try:
        data = request.get_json()
        fdc_id = data.get('fdcId')
        
        if not fdc_id:
            return jsonify({'error': 'FDC ID is required'}), 400
            
        # Get food details from USDA
        response = requests.get(
            f"{Config.USDA_API_BASE_URL}/food/{fdc_id}",
            params={
                'api_key': Config.USDA_API_KEY
            }
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to get food details from USDA database'}), 500
            
        food_data = response.json()
        
        # Prepare food item data
        food_item_data = {
            'name': food_data.get('description'),
            'brand': food_data.get('brandName', ''),
            'fdcId': food_data.get('fdcId'),
            'serving_size': food_data.get('servingSize', 100),
            'serving_unit': food_data.get('servingSizeUnit', 'g'),
            'is_custom': False,
            'nutrition': {}
        }
        
        # Extract nutrition data
        for nutrient in food_data.get('foodNutrients', []):
            if 'nutrient' in nutrient and 'amount' in nutrient:
                n = nutrient['nutrient']
                if n.get('name', '').lower() == 'energy' and n.get('unitName', '').lower() == 'kcal':
                    food_item_data['nutrition']['calories'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'protein':
                    food_item_data['nutrition']['protein'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'total lipid (fat)':
                    food_item_data['nutrition']['fat'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'carbohydrate, by difference':
                    food_item_data['nutrition']['carbs'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'fiber, total dietary':
                    food_item_data['nutrition']['fiber'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'sugars, total including nlea':
                    food_item_data['nutrition']['sugar'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'sodium, na':
                    food_item_data['nutrition']['sodium'] = nutrient.get('amount', 0)
                elif n.get('name', '').lower() == 'cholesterol':
                    food_item_data['nutrition']['cholesterol'] = nutrient.get('amount', 0)
        
        # Update with any user-provided data
        if 'name' in data:
            food_item_data['name'] = data['name']
        if 'serving_size' in data:
            food_item_data['serving_size'] = data['serving_size']
        if 'serving_unit' in data:
            food_item_data['serving_unit'] = data['serving_unit']
        if 'is_favorite' in data:
            food_item_data['is_favorite'] = data['is_favorite']
        
        # Create food item
        food_item = food_item_model.create(user_id, food_item_data)
        return jsonify(food_item), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to import food item: {str(e)}"}), 500


@nutrition_bp.route('/meals', methods=['POST'])
@auth_required
def create_meal(user_id):
    """Create a new meal log"""
    try:
        data = request.get_json()
        meal = meal_log_model.create(user_id, data)
        return jsonify(meal), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to create meal: {str(e)}"}), 500


@nutrition_bp.route('/meals', methods=['GET'])
@auth_required
def get_meals(user_id):
    """List meals with filtering and pagination"""
    try:
        # Extract query parameters
        query_params = {
            'limit': request.args.get('limit', 20),
            'offset': request.args.get('offset', 0),
            'date': request.args.get('date'),
            'meal_type': request.args.get('meal_type'),
            'sort_by': request.args.get('sort_by', 'meal_time'),
            'sort_dir': request.args.get('sort_dir', 'desc')
        }
        
        # Get meals using model
        result = meal_log_model.list(user_id, query_params)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f"Failed to get meals: {str(e)}"}), 500


@nutrition_bp.route('/meals/<meal_id>', methods=['GET'])
@auth_required
def get_meal(user_id, meal_id):
    """Get a specific meal by ID"""
    try:
        meal = meal_log_model.get(meal_id, user_id)
        return jsonify(meal)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f"Failed to get meal: {str(e)}"}), 500


@nutrition_bp.route('/meals/<meal_id>', methods=['PUT'])
@auth_required
def update_meal(user_id, meal_id):
    """Update a meal"""
    try:
        data = request.get_json()
        updated_meal = meal_log_model.update(meal_id, user_id, data)
        return jsonify(updated_meal)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to update meal: {str(e)}"}), 500


@nutrition_bp.route('/meals/<meal_id>', methods=['DELETE'])
@auth_required
def delete_meal(user_id, meal_id):
    """Delete a meal"""
    try:
        meal_log_model.delete(meal_id, user_id)
        return jsonify({'message': 'Meal deleted successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to delete meal: {str(e)}"}), 500


@nutrition_bp.route('/stats/daily', methods=['GET'])
@auth_required
def get_daily_nutrition_stats(user_id):
    """Get daily nutrition statistics"""
    try:
        # Get date parameter
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({'error': 'Date parameter is required'}), 400
            
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
        # Get all meals for the day
        query_params = {
            'date': date_str,
            'limit': 100,  # High limit to get all meals for the day
            'offset': 0
        }
        
        meals_result = meal_log_model.list(user_id, query_params)
        meals = meals_result['meals']
        
        # Initialize stats
        stats = {
            'date': date_str,
            'total': {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'fiber': 0,
                'sugar': 0,
                'sodium': 0,
                'cholesterol': 0
            },
            'by_meal_type': {},
            'meal_count': len(meals)
        }
        
        # Calculate totals
        for meal in meals:
            # Add to total
            nutrition = meal.get('nutrition_totals', {})
            for key in stats['total']:
                if key in nutrition:
                    stats['total'][key] += float(nutrition[key])
            
            # Add to meal type breakdown
            meal_type = meal.get('meal_type', 'other')
            if meal_type not in stats['by_meal_type']:
                stats['by_meal_type'][meal_type] = {
                    'calories': 0,
                    'protein': 0,
                    'carbs': 0,
                    'fat': 0,
                    'meal_count': 0
                }
                
            stats['by_meal_type'][meal_type]['meal_count'] += 1
            for key in ['calories', 'protein', 'carbs', 'fat']:
                if key in nutrition:
                    stats['by_meal_type'][meal_type][key] += float(nutrition[key])
        
        # Round values for better display
        for key in stats['total']:
            stats['total'][key] = round(stats['total'][key], 1)
            
        for meal_type in stats['by_meal_type']:
            for key in stats['by_meal_type'][meal_type]:
                if key != 'meal_count':
                    stats['by_meal_type'][meal_type][key] = round(stats['by_meal_type'][meal_type][key], 1)
        
        # Calculate macronutrient percentages
        total_calories = stats['total']['calories']
        if total_calories > 0:
            stats['macro_percentages'] = {
                'protein': round((stats['total']['protein'] * 4 / total_calories) * 100, 1) if stats['total']['protein'] > 0 else 0,
                'carbs': round((stats['total']['carbs'] * 4 / total_calories) * 100, 1) if stats['total']['carbs'] > 0 else 0,
                'fat': round((stats['total']['fat'] * 9 / total_calories) * 100, 1) if stats['total']['fat'] > 0 else 0
            }
        else:
            stats['macro_percentages'] = {'protein': 0, 'carbs': 0, 'fat': 0}
            
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': f"Failed to get daily nutrition stats: {str(e)}"}), 500


@nutrition_bp.route('/stats/weekly', methods=['GET'])
@auth_required
def get_weekly_nutrition_stats(user_id):
    """Get weekly nutrition statistics"""
    try:
        # Get start and end date parameters
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        if not start_date_str or not end_date_str:
            return jsonify({'error': 'Both start_date and end_date parameters are required'}), 400
            
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
        # Create Firestore reference
        db = firebase_admin.firestore.client()
        
        # Get all meals within date range
        meals_ref = db.collection('meals').where('userId', '==', user_id)
        meals_ref = meals_ref.where('meal_time', '>=', start_date)
        meals_ref = meals_ref.where('meal_time', '<=', end_date)
        
        # Execute query
        meal_docs = meals_ref.stream()
        meals = []
        for doc in meal_docs:
            meal = doc.to_dict()
            meal['id'] = doc.id
            meals.append(meal)
            
        # Group by day
        daily_stats = {}
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            daily_stats[date_str] = {
                'date': date_str,
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'meal_count': 0
            }
            current_date = current_date.replace(day=current_date.day + 1)
            
        # Calculate daily totals
        for meal in meals:
            meal_time = meal.get('meal_time')
            if hasattr(meal_time, 'strftime'):
                day_str = meal_time.strftime('%Y-%m-%d')
            else:
                # Handle Firestore timestamps
                day_str = datetime.fromtimestamp(meal_time.seconds).strftime('%Y-%m-%d')
                
            if day_str in daily_stats:
                daily_stats[day_str]['meal_count'] += 1
                nutrition = meal.get('nutrition_totals', {})
                for key in ['calories', 'protein', 'carbs', 'fat']:
                    if key in nutrition:
                        daily_stats[day_str][key] += float(nutrition[key])
                        
        # Calculate weekly averages
        days_with_data = sum(1 for day in daily_stats.values() if day['meal_count'] > 0)
        
        weekly_summary = {
            'start_date': start_date_str,
            'end_date': end_date_str,
            'days_with_data': days_with_data,
            'total_meals': sum(day['meal_count'] for day in daily_stats.values()),
            'daily_average': {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0
            },
            'daily_breakdown': [daily_stats[date] for date in sorted(daily_stats.keys())]
        }
        
        if days_with_data > 0:
            for key in ['calories', 'protein', 'carbs', 'fat']:
                total = sum(day[key] for day in daily_stats.values())
                weekly_summary['daily_average'][key] = round(total / days_with_data, 1)
        
        return jsonify(weekly_summary)
        
    except Exception as e:
        return jsonify({'error': f"Failed to get weekly nutrition stats: {str(e)}"}), 500


@nutrition_bp.route('/barcode/lookup', methods=['GET'])
@auth_required
def lookup_barcode(user_id):
    """Look up food by barcode"""
    try:
        barcode = request.args.get('code')
        
        if not barcode:
            return jsonify({'error': 'Barcode is required'}), 400
            
        # First check if it exists in our database
        db = firebase_admin.firestore.client()
        food_items = db.collection('food_items').where('barcode', '==', barcode).limit(1).stream()
        
        food_item = None
        for doc in food_items:
            food_item = doc.to_dict()
            food_item['id'] = doc.id
            break
            
        if food_item:
            return jsonify({'food': food_item, 'source': 'database'})
            
        # If not found, use an external service
        # This is a placeholder - in production, you'd implement a real barcode lookup API
        # like Open Food Facts or USDA Global Branded Food Products Database
        
        # Simulate response from external API
        return jsonify({
            'error': 'Barcode lookup not implemented',
            'message': 'Please add this item manually'
        }), 501
        
    except Exception as e:
        return jsonify({'error': f"Failed to look up barcode: {str(e)}"}), 500