from flask import Blueprint, jsonify, request
from utils.firebase_admin import auth_required
import firebase_admin
from firebase_admin import firestore
from datetime import datetime, timedelta
from nutrition.models import FoodItem, MealLog

# Create blueprint
nutrition_bp = Blueprint('nutrition', __name__)
db = firebase_admin.firestore.client()

# Food Items Routes
@nutrition_bp.route('/food-items', methods=['POST'])
@auth_required
def create_food_item(user_id):
    """Create a new food item in the database"""
    try:
        data = request.get_json()
        food_item_service = FoodItem(db)
        result = food_item_service.create(user_id, data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to create food item: {str(e)}"}), 500

@nutrition_bp.route('/food-items/<item_id>', methods=['GET'])
@auth_required
def get_food_item(user_id, item_id):
    """Get a specific food item by ID"""
    try:
        food_item_service = FoodItem(db)
        result = food_item_service.get(item_id, user_id)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f"Failed to retrieve food item: {str(e)}"}), 500

@nutrition_bp.route('/food-items', methods=['GET'])
@auth_required
def list_food_items(user_id):
    """List food items with filtering and pagination"""
    try:
        # Get query parameters
        query_params = {
            'limit': request.args.get('limit', 20, type=int),
            'offset': request.args.get('offset', 0, type=int),
            'q': request.args.get('q', ''),
            'is_favorite': request.args.get('is_favorite') == 'true',
            'is_custom': request.args.get('is_custom') == 'true',
            'sort_by': request.args.get('sort_by', 'created_at'),
            'sort_dir': request.args.get('sort_dir', 'desc')
        }
        
        food_item_service = FoodItem(db)
        result = food_item_service.list(user_id, query_params)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f"Failed to list food items: {str(e)}"}), 500

@nutrition_bp.route('/food-items/<item_id>', methods=['PUT'])
@auth_required
def update_food_item(user_id, item_id):
    """Update a food item"""
    try:
        data = request.get_json()
        food_item_service = FoodItem(db)
        result = food_item_service.update(item_id, user_id, data)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to update food item: {str(e)}"}), 500

@nutrition_bp.route('/food-items/<item_id>', methods=['DELETE'])
@auth_required
def delete_food_item(user_id, item_id):
    """Delete a food item"""
    try:
        food_item_service = FoodItem(db)
        food_item_service.delete(item_id, user_id)
        return jsonify({'message': 'Food item deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to delete food item: {str(e)}"}), 500

@nutrition_bp.route('/food-items/<item_id>/favorite', methods=['POST'])
@auth_required
def toggle_favorite(user_id, item_id):
    """Toggle favorite status for a food item"""
    try:
        data = request.get_json()
        is_favorite = data.get('is_favorite', True)
        
        food_item_service = FoodItem(db)
        result = food_item_service.update(item_id, user_id, {'is_favorite': is_favorite})
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to update favorite status: {str(e)}"}), 500

# Meal Logging Routes
@nutrition_bp.route('/meals', methods=['POST'])
@auth_required
def create_meal(user_id):
    """Log a new meal"""
    try:
        data = request.get_json()
        meal_service = MealLog(db)
        result = meal_service.create(user_id, data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to log meal: {str(e)}"}), 500

@nutrition_bp.route('/meals/<meal_id>', methods=['GET'])
@auth_required
def get_meal(user_id, meal_id):
    """Get a specific meal log by ID"""
    try:
        meal_service = MealLog(db)
        result = meal_service.get(meal_id, user_id)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f"Failed to retrieve meal: {str(e)}"}), 500

@nutrition_bp.route('/meals', methods=['GET'])
@auth_required
def list_meals(user_id):
    """List meal logs with filtering and pagination"""
    try:
        # Get query parameters
        query_params = {
            'limit': request.args.get('limit', 20, type=int),
            'offset': request.args.get('offset', 0, type=int),
            'date': request.args.get('date'),
            'meal_type': request.args.get('meal_type'),
            'sort_by': request.args.get('sort_by', 'meal_time'),
            'sort_dir': request.args.get('sort_dir', 'desc')
        }
        
        meal_service = MealLog(db)
        result = meal_service.list(user_id, query_params)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f"Failed to list meals: {str(e)}"}), 500

@nutrition_bp.route('/meals/<meal_id>', methods=['PUT'])
@auth_required
def update_meal(user_id, meal_id):
    """Update a meal log"""
    try:
        data = request.get_json()
        meal_service = MealLog(db)
        result = meal_service.update(meal_id, user_id, data)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to update meal: {str(e)}"}), 500

@nutrition_bp.route('/meals/<meal_id>', methods=['DELETE'])
@auth_required
def delete_meal(user_id, meal_id):
    """Delete a meal log"""
    try:
        meal_service = MealLog(db)
        meal_service.delete(meal_id, user_id)
        return jsonify({'message': 'Meal deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to delete meal: {str(e)}"}), 500

# Nutrition Summary and Analytics
@nutrition_bp.route('/summary/daily', methods=['GET'])
@auth_required
def get_daily_summary(user_id):
    """Get nutrition summary for a specific day"""
    try:
        date_str = request.args.get('date')
        if not date_str:
            # Default to today
            date = datetime.now().strftime('%Y-%m-%d')
        else:
            date = date_str
            
        # Get all meals for the specified day
        query_params = {
            'date': date,
            'limit': 100,  # High limit to get all meals for the day
            'offset': 0
        }
        
        meal_service = MealLog(db)
        meals_result = meal_service.list(user_id, query_params)
        meals = meals_result.get('meals', [])
        
        # Calculate nutrition totals
        nutrition_totals = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'sugar': 0
        }
        
        meal_breakdown = []
        
        for meal in meals:
            meal_nutrition = meal.get('nutrition_totals', {})
            meal_summary = {
                'id': meal.get('id'),
                'name': meal.get('name'),
                'meal_type': meal.get('meal_type'),
                'meal_time': meal.get('meal_time'),
                'nutrition': meal_nutrition
            }
            meal_breakdown.append(meal_summary)
            
            # Add to totals
            for key in nutrition_totals:
                if key in meal_nutrition:
                    nutrition_totals[key] += meal_nutrition.get(key, 0)
        
        # Round values for display
        for key in nutrition_totals:
            nutrition_totals[key] = round(nutrition_totals[key], 1)
            
        return jsonify({
            'date': date,
            'nutrition_totals': nutrition_totals,
            'meal_breakdown': meal_breakdown
        })
    except Exception as e:
        return jsonify({'error': f"Failed to get daily summary: {str(e)}"}), 500

@nutrition_bp.route('/summary/weekly', methods=['GET'])
@auth_required
def get_weekly_summary(user_id):
    """Get nutrition summary for the past week"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Format dates for queries
        end_date_str = end_date.strftime('%Y-%m-%d')
        start_date_str = start_date.strftime('%Y-%m-%d')
        
        # Create daily summaries
        daily_data = []
        
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Get meals for this day
            query_params = {
                'date': date_str,
                'limit': 100,
                'offset': 0
            }
            
            meal_service = MealLog(db)
            meals_result = meal_service.list(user_id, query_params)
            meals = meals_result.get('meals', [])
            
            # Calculate nutrition totals for the day
            nutrition_totals = {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0
            }
            
            for meal in meals:
                meal_nutrition = meal.get('nutrition_totals', {})
                for key in nutrition_totals:
                    if key in meal_nutrition:
                        nutrition_totals[key] += meal_nutrition.get(key, 0)
            
            # Round values
            for key in nutrition_totals:
                nutrition_totals[key] = round(nutrition_totals[key], 1)
                
            daily_data.append({
                'date': date_str,
                'nutrition': nutrition_totals,
                'meal_count': len(meals)
            })
            
            # Move to next day
            current_date += timedelta(days=1)
        
        # Calculate weekly averages
        week_totals = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0
        }
        
        for day in daily_data:
            for key in week_totals:
                week_totals[key] += day['nutrition'].get(key, 0)
        
        # Calculate averages
        week_averages = {}
        for key in week_totals:
            week_averages[key] = round(week_totals[key] / 7, 1)
            
        return jsonify({
            'start_date': start_date_str,
            'end_date': end_date_str,
            'daily_data': daily_data,
            'week_totals': week_totals,
            'week_averages': week_averages
        })
    except Exception as e:
        return jsonify({'error': f"Failed to get weekly summary: {str(e)}"}), 500

# USDA Food Database Search
@nutrition_bp.route('/food-database/search', methods=['GET'])
@auth_required
def search_food_database(user_id):
    """Search the USDA food database"""
    from utils.api_clients import USDAClient
    from config import Config
    
    try:
        query = request.args.get('q', '')
        page_size = request.args.get('pageSize', 25, type=int)
        page_number = request.args.get('pageNumber', 1, type=int)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
            
        # Initialize USDA client
        usda_client = USDAClient(Config.USDA_API_KEY, Config.USDA_API_BASE_URL)
        
        # Search for foods
        result = usda_client.search_foods(query, page_size, page_number)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f"Failed to search food database: {str(e)}"}), 500

@nutrition_bp.route('/food-database/food/<fdc_id>', methods=['GET'])
@auth_required
def get_food_details(user_id, fdc_id):
    """Get detailed information for a specific food item from USDA database"""
    from utils.api_clients import USDAClient
    from config import Config
    
    try:
        # Initialize USDA client
        usda_client = USDAClient(Config.USDA_API_KEY, Config.USDA_API_BASE_URL)
        
        # Get food details
        result = usda_client.get_food_details(fdc_id)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f"Failed to get food details: {str(e)}"}), 500

@nutrition_bp.route('/food-database/import', methods=['POST'])
@auth_required
def import_from_usda(user_id):
    """Import a food item from USDA database to user's collection"""
    from utils.api_clients import USDAClient
    from config import Config
    
    try:
        data = request.get_json()
        fdc_id = data.get('fdc_id')
        
        if not fdc_id:
            return jsonify({'error': 'FDC ID is required'}), 400
            
        # Initialize USDA client
        usda_client = USDAClient(Config.USDA_API_KEY, Config.USDA_API_BASE_URL)
        
        # Get food details from USDA
        food_details = usda_client.get_food_details(fdc_id)
        
        # Convert to our food item format
        food_item_data = {
            'name': food_details.get('description', ''),
            'brand': food_details.get('brandName', ''),
            'fdcId': fdc_id,
            'serving_size': 100,  # Default to 100g
            'serving_unit': 'g',
            'is_custom': False,
            'nutrition': {}
        }
        
        # Extract nutrients
        nutrients = food_details.get('foodNutrients', [])
        for nutrient in nutrients:
            nutrient_name = nutrient.get('nutrient', {}).get('name', '').lower()
            value = nutrient.get('amount', 0)
            
            if 'energy' in nutrient_name and 'kcal' in nutrient.get('nutrient', {}).get('unitName', '').lower():
                food_item_data['nutrition']['calories'] = value
            elif 'protein' in nutrient_name:
                food_item_data['nutrition']['protein'] = value
            elif 'carbohydrate' in nutrient_name and 'by difference' in nutrient_name:
                food_item_data['nutrition']['carbs'] = value
            elif 'total lipid (fat)' in nutrient_name:
                food_item_data['nutrition']['fat'] = value
            elif 'fiber' in nutrient_name:
                food_item_data['nutrition']['fiber'] = value
            elif 'sugars' in nutrient_name:
                food_item_data['nutrition']['sugar'] = value
            elif 'sodium' in nutrient_name:
                food_item_data['nutrition']['sodium'] = value
            elif 'cholesterol' in nutrient_name:
                food_item_data['nutrition']['cholesterol'] = value
        
        # Create food item
        food_item_service = FoodItem(db)
        result = food_item_service.create(user_id, food_item_data)
        
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to import food item: {str(e)}"}), 500