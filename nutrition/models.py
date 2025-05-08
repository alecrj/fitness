# nutrition/models.py
from datetime import datetime
from typing import List, Dict, Any, Optional
import firebase_admin
from firebase_admin import firestore

class NutritionModel:
    """Base class for nutrition models with common methods"""
    @staticmethod
    def validate_nutrition_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validates and standardizes nutrition data
        
        Args:
            data: Dict containing nutrition information
            
        Returns:
            Dict containing validated nutrition data with consistent format
        """
        nutrition = {}
        
        # Required fields with default values
        if 'calories' in data:
            nutrition['calories'] = max(0, float(data['calories']))
        else:
            nutrition['calories'] = 0
            
        # Macronutrients
        for macro in ['protein', 'carbs', 'fat']:
            if macro in data:
                nutrition[macro] = max(0, float(data[macro]))
            else:
                nutrition[macro] = 0
                
        # Optional micronutrients
        for micro in ['fiber', 'sugar', 'sodium', 'cholesterol']:
            if micro in data:
                nutrition[micro] = max(0, float(data[micro]))
                
        return nutrition

    @staticmethod
    def calculate_totals(items: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate nutrition totals from a list of items
        
        Args:
            items: List of items with nutrition data
            
        Returns:
            Dict containing totals for each nutrient
        """
        totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 
                  'fiber': 0, 'sugar': 0, 'sodium': 0, 'cholesterol': 0}
        
        for item in items:
            nutrition = item.get('nutrition', {})
            for key in totals:
                if key in nutrition:
                    totals[key] += float(nutrition[key])
        
        # Round values for display
        for key in totals:
            totals[key] = round(totals[key], 1)
            
        return totals

class FoodItem(NutritionModel):
    """Model for food items in the nutrition database"""
    
    def __init__(self, db=None):
        """Initialize the FoodItem model with database reference
        
        Args:
            db: Firestore database reference (optional)
        """
        self.db = db or firebase_admin.firestore.client()
        self.collection = "food_items"
    
    def create(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new food item
        
        Args:
            user_id: ID of the user creating the food item
            data: Food item data including name and nutrition
            
        Returns:
            Dict containing the created food item
            
        Raises:
            ValueError: If required fields are missing
        """
        # Validate required fields
        if not data.get('name'):
            raise ValueError("Food item name is required")
            
        # Process nutrition data
        nutrition = self.validate_nutrition_data(data.get('nutrition', {}))
        
        # Create food item document
        food_item = {
            'userId': user_id,
            'name': data['name'],
            'brand': data.get('brand', ''),
            'barcode': data.get('barcode'),
            'fdcId': data.get('fdcId'),
            'serving_size': float(data.get('serving_size', 100)),
            'serving_unit': data.get('serving_unit', 'g'),
            'calories': nutrition.get('calories', 0),
            'protein': nutrition.get('protein', 0),
            'carbs': nutrition.get('carbs', 0),
            'fat': nutrition.get('fat', 0),
            'nutrition': nutrition,
            'is_custom': data.get('is_custom', True),
            'is_favorite': data.get('is_favorite', False),
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        # Save to database
        doc_ref = self.db.collection(self.collection).document()
        doc_ref.set(food_item)
        
        # Return with ID
        food_item['id'] = doc_ref.id
        return food_item
    
    def get(self, item_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a food item by ID
        
        Args:
            item_id: ID of the food item to retrieve
            user_id: ID of the requesting user (for authorization, optional)
            
        Returns:
            Dict containing the food item data
            
        Raises:
            ValueError: If food item not found or user not authorized
        """
        doc = self.db.collection(self.collection).document(item_id).get()
        
        if not doc.exists:
            raise ValueError("Food item not found")
            
        item = doc.to_dict()
        
        # Check if item belongs to user or is a public/system item
        if user_id and item.get('userId') != user_id and not item.get('is_public', False):
            raise ValueError("Unauthorized access to food item")
            
        item['id'] = doc.id
        return item
    
    def list(self, user_id: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """List food items with filtering and pagination
        
        Args:
            user_id: ID of the user
            query_params: Dict containing filter and pagination parameters
            
        Returns:
            Dict containing items and pagination info
        """
        # Start with base query for user's items and public items
        query = self.db.collection(self.collection).where(
            filter=firestore.FieldFilter("userId", "==", user_id)
        )
        
        # Apply filters
        if query_params.get('is_favorite') == True:
            query = query.where(
                filter=firestore.FieldFilter("is_favorite", "==", True)
            )
            
        if query_params.get('is_custom') == True:
            query = query.where(
                filter=firestore.FieldFilter("is_custom", "==", True)
            )
            
        # Search by name (will be filtered in memory)
        search_term = query_params.get('q', '').lower()
            
        # Apply sorting
        sort_by = query_params.get('sort_by', 'created_at')
        sort_dir = query_params.get('sort_dir', 'desc')
        direction = firestore.Query.DESCENDING if sort_dir == 'desc' else firestore.Query.ASCENDING
        query = query.order_by(sort_by, direction=direction)
        
        # Pagination
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Execute query
        items = []
        # Get all items for pagination and filtering
        all_items = [doc for doc in query.stream()]
        total = len(all_items)
        
        # Apply pagination and search filter in memory
        for doc in all_items[offset:offset+limit]:
            item = doc.to_dict()
            item['id'] = doc.id
            
            # Apply search filter in memory if provided
            if search_term and search_term not in item.get('name', '').lower():
                continue
                
            items.append(item)
            
        return {
            'items': items,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }
    
    def update(self, item_id: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a food item
        
        Args:
            item_id: ID of the food item to update
            user_id: ID of the user making the update (for authorization)
            data: Updated food item data
            
        Returns:
            Dict containing the updated food item
            
        Raises:
            ValueError: If food item not found or user not authorized
        """
        doc_ref = self.db.collection(self.collection).document(item_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise ValueError("Food item not found")
            
        item = doc.to_dict()
        
        # Check ownership
        if item.get('userId') != user_id:
            raise ValueError("Unauthorized to update this food item")
            
        # Process nutrition data if provided
        if 'nutrition' in data:
            nutrition = self.validate_nutrition_data(data['nutrition'])
            data['nutrition'] = nutrition
            
            # Update main nutrient fields
            for key in ['calories', 'protein', 'carbs', 'fat']:
                if key in nutrition:
                    data[key] = nutrition[key]
        
        # Update timestamp
        data['updated_at'] = firestore.SERVER_TIMESTAMP
        
        # Update the document
        update_data = {k: v for k, v in data.items() if k != 'id' and k != 'userId'}
        doc_ref.update(update_data)
        
        # Return updated item
        updated_item = item.copy()
        updated_item.update(update_data)
        updated_item['id'] = item_id
        
        return updated_item
    
    def delete(self, item_id: str, user_id: str) -> bool:
        """Delete a food item
        
        Args:
            item_id: ID of the food item to delete
            user_id: ID of the user making the deletion (for authorization)
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If food item not found or user not authorized
        """
        doc_ref = self.db.collection(self.collection).document(item_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise ValueError("Food item not found")
            
        item = doc.to_dict()
        
        # Check ownership
        if item.get('userId') != user_id:
            raise ValueError("Unauthorized to delete this food item")
            
        # Delete the document
        doc_ref.delete()
        return True
        
    def search_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """Search for food item by barcode
        
        Args:
            barcode: Product barcode
            
        Returns:
            Dict containing the food item or None if not found
        """
        query = self.db.collection(self.collection).where(
            filter=firestore.FieldFilter("barcode", "==", barcode)
        ).limit(1)
        
        items = query.stream()
        for doc in items:
            item = doc.to_dict()
            item['id'] = doc.id
            return item
            
        return None

class MealLog(NutritionModel):
    """Model for meal logging and tracking"""
    
    def __init__(self, db=None):
        """Initialize the MealLog model with database reference
        
        Args:
            db: Firestore database reference (optional)
        """
        self.db = db or firebase_admin.firestore.client()
        self.collection = "meals"
        self.food_item = FoodItem(db)
    
    def create(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new meal log
        
        Args:
            user_id: ID of the user creating the meal
            data: Meal data including name, type, and food items
            
        Returns:
            Dict containing the created meal
            
        Raises:
            ValueError: If required fields are missing
        """
        if not data.get('name'):
            raise ValueError("Meal name is required")
            
        if not data.get('meal_type'):
            raise ValueError("Meal type is required")
            
        # Process food items
        food_items = []
        nutrition_totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 
                           'fiber': 0, 'sugar': 0, 'sodium': 0, 'cholesterol': 0}
        
        for item in data.get('food_items', []):
            # If just an ID is provided, fetch the complete item
            if isinstance(item, str):
                try:
                    food_item = self.food_item.get(item, user_id)
                    # Calculate nutrition based on default serving
                    food_items.append({
                        'food_item_id': item,
                        'food_item_name': food_item.get('name', 'Unknown Food'),
                        'servings': 1,
                        'nutrition': food_item.get('nutrition', {})
                    })
                    # Add to totals
                    for key in nutrition_totals:
                        if key in food_item.get('nutrition', {}):
                            nutrition_totals[key] += float(food_item['nutrition'][key])
                except ValueError:
                    # Skip invalid items
                    continue
            else:
                # If full item with serving info is provided
                item_id = item.get('food_item_id')
                servings = float(item.get('servings', 1))
                
                try:
                    food_item = self.food_item.get(item_id, user_id)
                    # Calculate nutrition based on servings
                    item_nutrition = {}
                    for key, value in food_item.get('nutrition', {}).items():
                        item_nutrition[key] = float(value) * servings
                        
                    food_items.append({
                        'food_item_id': item_id,
                        'food_item_name': food_item.get('name', 'Unknown Food'),
                        'servings': servings,
                        'nutrition': item_nutrition
                    })
                    
                    # Add to totals
                    for key in nutrition_totals:
                        if key in food_item.get('nutrition', {}):
                            nutrition_totals[key] += float(food_item['nutrition'][key]) * servings
                except ValueError:
                    # Skip invalid items
                    continue
        
        # Create meal document
        meal = {
            'userId': user_id,
            'name': data['name'],
            'meal_type': data['meal_type'],
            'meal_time': data.get('meal_time', firestore.SERVER_TIMESTAMP),
            'food_items': food_items,
            'nutrition_totals': nutrition_totals,
            'notes': data.get('notes', ''),
            'tags': data.get('tags', []),
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        # Save to database
        doc_ref = self.db.collection(self.collection).document()
        doc_ref.set(meal)
        
        # Return with ID
        meal['id'] = doc_ref.id
        return meal
    
    def get(self, meal_id: str, user_id: str) -> Dict[str, Any]:
        """Get a meal by ID
        
        Args:
            meal_id: ID of the meal to retrieve
            user_id: ID of the requesting user (for authorization)
            
        Returns:
            Dict containing the meal data
            
        Raises:
            ValueError: If meal not found or user not authorized
        """
        doc = self.db.collection(self.collection).document(meal_id).get()
        
        if not doc.exists:
            raise ValueError("Meal not found")
            
        meal = doc.to_dict()
        
        # Check ownership
        if meal.get('userId') != user_id:
            raise ValueError("Unauthorized access to meal")
            
        meal['id'] = doc.id
        return meal
    
    def list(self, user_id: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """List meals with filtering and pagination
        
        Args:
            user_id: ID of the user
            query_params: Dict containing filter and pagination parameters
            
        Returns:
            Dict containing meals and pagination info
        """
        # Start with base query for user's meals
        query = self.db.collection(self.collection).where(
            filter=firestore.FieldFilter("userId", "==", user_id)
        )
        
        # Apply date filter if provided
        if query_params.get('date'):
            try:
                date = datetime.strptime(query_params['date'], '%Y-%m-%d')
                next_day = datetime(date.year, date.month, date.day, 23, 59, 59)
                
                # Use Firebase timestamp filtering
                query = query.where(
                    filter=firestore.FieldFilter("meal_time", ">=", date)
                ).where(
                    filter=firestore.FieldFilter("meal_time", "<=", next_day)
                )
            except ValueError:
                # Invalid date format, ignore filter
                pass
            
        # Apply meal type filter
        if query_params.get('meal_type'):
            query = query.where(
                filter=firestore.FieldFilter("meal_type", "==", query_params['meal_type'])
            )
            
        # Apply tag filter if provided
        if query_params.get('tag'):
            query = query.where(
                filter=firestore.FieldFilter("tags", "array_contains", query_params['tag'])
            )
            
        # Apply sorting
        sort_by = query_params.get('sort_by', 'meal_time')
        sort_dir = query_params.get('sort_dir', 'desc')
        direction = firestore.Query.DESCENDING if sort_dir == 'desc' else firestore.Query.ASCENDING
        query = query.order_by(sort_by, direction=direction)
        
        # Pagination
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Execute query
        meals = []
        # Get all meals for accurate pagination
        all_meals = [doc for doc in query.stream()]
        total = len(all_meals)
        
        # Apply pagination in memory
        for doc in all_meals[offset:offset+limit]:
            meal = doc.to_dict()
            meal['id'] = doc.id
            meals.append(meal)
            
        return {
            'meals': meals,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }
    
    def update(self, meal_id: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a meal
        
        Args:
            meal_id: ID of the meal to update
            user_id: ID of the user making the update (for authorization)
            data: Updated meal data
            
        Returns:
            Dict containing the updated meal
            
        Raises:
            ValueError: If meal not found or user not authorized
        """
        doc_ref = self.db.collection(self.collection).document(meal_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise ValueError("Meal not found")
            
        meal = doc.to_dict()
        
        # Check ownership
        if meal.get('userId') != user_id:
            raise ValueError("Unauthorized to update this meal")
            
        # Handle food items updates
        if 'food_items' in data:
            food_items = []
            nutrition_totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 
                               'fiber': 0, 'sugar': 0, 'sodium': 0, 'cholesterol': 0}
            
            for item in data['food_items']:
                # Process each food item similar to create method
                if isinstance(item, str):
                    try:
                        food_item = self.food_item.get(item, user_id)
                        food_items.append({
                            'food_item_id': item,
                            'food_item_name': food_item.get('name', 'Unknown Food'),
                            'servings': 1,
                            'nutrition': food_item.get('nutrition', {})
                        })
                        for key in nutrition_totals:
                            if key in food_item.get('nutrition', {}):
                                nutrition_totals[key] += float(food_item['nutrition'][key])
                    except ValueError:
                        continue
                else:
                    item_id = item.get('food_item_id')
                    servings = float(item.get('servings', 1))
                    
                    try:
                        food_item = self.food_item.get(item_id, user_id)
                        item_nutrition = {}
                        for key, value in food_item.get('nutrition', {}).items():
                            item_nutrition[key] = float(value) * servings
                            
                        food_items.append({
                            'food_item_id': item_id,
                            'food_item_name': food_item.get('name', 'Unknown Food'),
                            'servings': servings,
                            'nutrition': item_nutrition
                        })
                        
                        for key in nutrition_totals:
                            if key in food_item.get('nutrition', {}):
                                nutrition_totals[key] += float(food_item['nutrition'][key]) * servings
                    except ValueError:
                        continue
            
            data['food_items'] = food_items
            data['nutrition_totals'] = nutrition_totals
        
        # Update timestamp
        data['updated_at'] = firestore.SERVER_TIMESTAMP
        
        # Update the document
        update_data = {k: v for k, v in data.items() if k != 'id' and k != 'userId'}
        doc_ref.update(update_data)
        
        # Return updated meal
        updated_meal = meal.copy()
        updated_meal.update(update_data)
        updated_meal['id'] = meal_id
        
        return updated_meal
    
    def delete(self, meal_id: str, user_id: str) -> bool:
        """Delete a meal
        
        Args:
            meal_id: ID of the meal to delete
            user_id: ID of the user making the deletion (for authorization)
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If meal not found or user not authorized
        """
        doc_ref = self.db.collection(self.collection).document(meal_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise ValueError("Meal not found")
            
        meal = doc.to_dict()
        
        # Check ownership
        if meal.get('userId') != user_id:
            raise ValueError("Unauthorized to delete this meal")
            
        # Delete the document
        doc_ref.delete()
        return True
    
    def get_stats(self, user_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get nutrition statistics for a date range
        
        Args:
            user_id: ID of the user
            start_date: Start date for statistics
            end_date: End date for statistics
            
        Returns:
            Dict containing nutrition statistics
        """
        # Query meals within date range
        query = self.db.collection(self.collection).where(
            filter=firestore.FieldFilter("userId", "==", user_id)
        ).where(
            filter=firestore.FieldFilter("meal_time", ">=", start_date)
        ).where(
            filter=firestore.FieldFilter("meal_time", "<=", end_date)
        )
        
        meals = [doc.to_dict() for doc in query.stream()]
        
        # Initialize stats
        stats = {
            'total_meals': len(meals),
            'by_meal_type': {},
            'daily_totals': {},
            'average_daily': {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0
            },
            'nutrition_totals': {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'fiber': 0,
                'sugar': 0,
                'sodium': 0,
                'cholesterol': 0
            }
        }
        
        # Calculate meal type breakdown
        for meal in meals:
            meal_type = meal.get('meal_type', 'other')
            if meal_type not in stats['by_meal_type']:
                stats['by_meal_type'][meal_type] = {
                    'count': 0,
                    'calories': 0,
                    'protein': 0,
                    'carbs': 0,
                    'fat': 0
                }
                
            stats['by_meal_type'][meal_type]['count'] += 1
            
            nutrition = meal.get('nutrition_totals', {})
            for key in ['calories', 'protein', 'carbs', 'fat']:
                if key in nutrition:
                    stats['by_meal_type'][meal_type][key] += float(nutrition[key])
                    stats['nutrition_totals'][key] += float(nutrition[key])
                    
            # Additional nutrients for total only
            for key in ['fiber', 'sugar', 'sodium', 'cholesterol']:
                if key in nutrition:
                    stats['nutrition_totals'][key] += float(nutrition[key])
                    
            # Calculate daily totals
            meal_time = meal.get('meal_time')
            if hasattr(meal_time, 'strftime'):
                day_str = meal_time.strftime('%Y-%m-%d')
            else:
                # Handle Firestore timestamps
                day_str = datetime.fromtimestamp(meal_time.seconds).strftime('%Y-%m-%d')
                
            if day_str not in stats['daily_totals']:
                stats['daily_totals'][day_str] = {
                    'calories': 0,
                    'protein': 0,
                    'carbs': 0,
                    'fat': 0,
                    'meal_count': 0
                }
                
            stats['daily_totals'][day_str]['meal_count'] += 1
            for key in ['calories', 'protein', 'carbs', 'fat']:
                if key in nutrition:
                    stats['daily_totals'][day_str][key] += float(nutrition[key])
        
        # Calculate daily averages
        days_with_data = len(stats['daily_totals'])
        if days_with_data > 0:
            for key in ['calories', 'protein', 'carbs', 'fat']:
                stats['average_daily'][key] = round(stats['nutrition_totals'][key] / days_with_data, 1)
                
        # Round all values for better display
        for key in stats['nutrition_totals']:
            stats['nutrition_totals'][key] = round(stats['nutrition_totals'][key], 1)
            
        for meal_type in stats['by_meal_type']:
            for key in stats['by_meal_type'][meal_type]:
                if key != 'count':
                    stats['by_meal_type'][meal_type][key] = round(stats['by_meal_type'][meal_type][key], 1)
                    
        for day in stats['daily_totals']:
            for key in stats['daily_totals'][day]:
                if key != 'meal_count':
                    stats['daily_totals'][day][key] = round(stats['daily_totals'][day][key], 1)
        
        return stats