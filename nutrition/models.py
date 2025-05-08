# nutrition/models.py
from datetime import datetime
from typing import List, Dict, Any, Optional

class NutritionModel:
    """Base class for nutrition models with common methods"""
    @staticmethod
    def validate_nutrition_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validates and standardizes nutrition data"""
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
        """Calculate nutrition totals from a list of items"""
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
    """Model for food items"""
    def __init__(self, db_ref):
        self.db = db_ref
        self.collection = "food_items"
    
    def create(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new food item"""
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
            'created_at': datetime.utcnow()
        }
        
        # Save to database
        doc_ref = self.db.collection(self.collection).document()
        doc_ref.set(food_item)
        
        # Return with ID
        food_item['id'] = doc_ref.id
        return food_item
    
    def get(self, item_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a food item by ID"""
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
        """List food items with filtering and pagination"""
        # Start with base query for user's items
        query = self.db.collection(self.collection).where('userId', '==', user_id)
        
        # Apply filters
        if query_params.get('is_favorite'):
            query = query.where('is_favorite', '==', True)
            
        if query_params.get('is_custom'):
            query = query.where('is_custom', '==', True)
            
        # Search by name
        search_term = query_params.get('q', '').lower()
            
        # Apply sorting
        sort_by = query_params.get('sort_by', 'created_at')
        sort_dir = query_params.get('sort_dir', 'desc')
        direction = self.db.Query.DESCENDING if sort_dir == 'desc' else self.db.Query.ASCENDING
        query = query.order_by(sort_by, direction=direction)
        
        # Pagination
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Execute query
        items = []
        # Get total first for pagination
        all_items = [doc for doc in query.stream()]
        total = len(all_items)
        
        # Apply pagination in memory
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
        """Update a food item"""
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
        
        # Update the document
        update_data = {k: v for k, v in data.items() if k != 'id' and k != 'userId'}
        doc_ref.update(update_data)
        
        # Return updated item
        updated_item = item.copy()
        updated_item.update(update_data)
        updated_item['id'] = item_id
        
        return updated_item
    
    def delete(self, item_id: str, user_id: str) -> bool:
        """Delete a food item"""
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

class MealLog(NutritionModel):
    """Model for meal logging"""
    def __init__(self, db_ref):
        self.db = db_ref
        self.collection = "meals"
        self.food_item = FoodItem(db_ref)
    
    def create(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new meal log"""
        if not data.get('name'):
            raise ValueError("Meal name is required")
            
        if not data.get('meal_type'):
            raise ValueError("Meal type is required")
            
        # Process food items
        food_items = []
        nutrition_totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        for item in data.get('food_items', []):
            # If just an ID is provided, fetch the complete item
            if isinstance(item, str):
                try:
                    food_item = self.food_item.get(item, user_id)
                    # Calculate nutrition based on default serving
                    food_items.append({
                        'food_item_id': item,
                        'servings': 1,
                        'nutrition': food_item.get('nutrition', {})
                    })
                    # Add to totals
                    for key in nutrition_totals:
                        if key in food_item:
                            nutrition_totals[key] += float(food_item[key])
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
                        'food_item_name': food_item.get('name'),
                        'servings': servings,
                        'nutrition': item_nutrition
                    })
                    
                    # Add to totals
                    for key in nutrition_totals:
                        if key in food_item:
                            nutrition_totals[key] += float(food_item[key]) * servings
                except ValueError:
                    # Skip invalid items
                    continue
        
        # Create meal document
        meal = {
            'userId': user_id,
            'name': data['name'],
            'meal_type': data['meal_type'],
            'meal_time': data.get('meal_time', datetime.utcnow()),
            'food_items': food_items,
            'nutrition_totals': nutrition_totals,
            'created_at': datetime.utcnow()
        }
        
        # Save to database
        doc_ref = self.db.collection(self.collection).document()
        doc_ref.set(meal)
        
        # Return with ID
        meal['id'] = doc_ref.id
        return meal
    
    def get(self, meal_id: str, user_id: str) -> Dict[str, Any]:
        """Get a meal by ID"""
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
        """List meals with filtering and pagination"""
        # Start with base query for user's meals
        query = self.db.collection(self.collection).where('userId', '==', user_id)
        
        # Apply date filter if provided
        if query_params.get('date'):
            date = datetime.strptime(query_params['date'], '%Y-%m-%d')
            next_day = datetime(date.year, date.month, date.day, 23, 59, 59)
            query = query.where('meal_time', '>=', date).where('meal_time', '<=', next_day)
            
        # Apply meal type filter
        if query_params.get('meal_type'):
            query = query.where('meal_type', '==', query_params['meal_type'])
            
        # Apply sorting
        sort_by = query_params.get('sort_by', 'meal_time')
        sort_dir = query_params.get('sort_dir', 'desc')
        direction = self.db.Query.DESCENDING if sort_dir == 'desc' else self.db.Query.ASCENDING
        query = query.order_by(sort_by, direction=direction)
        
        # Pagination
        limit = int(query_params.get('limit', 20))
        offset = int(query_params.get('offset', 0))
        
        # Execute query
        meals = []
        # Get total first for pagination
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
        """Update a meal"""
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
            nutrition_totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
            
            for item in data['food_items']:
                # Process each food item similar to create method
                if isinstance(item, str):
                    try:
                        food_item = self.food_item.get(item, user_id)
                        food_items.append({
                            'food_item_id': item,
                            'servings': 1,
                            'nutrition': food_item.get('nutrition', {})
                        })
                        for key in nutrition_totals:
                            if key in food_item:
                                nutrition_totals[key] += float(food_item[key])
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
                            'food_item_name': food_item.get('name'),
                            'servings': servings,
                            'nutrition': item_nutrition
                        })
                        
                        for key in nutrition_totals:
                            if key in food_item:
                                nutrition_totals[key] += float(food_item[key]) * servings
                    except ValueError:
                        continue
            
            data['food_items'] = food_items
            data['nutrition_totals'] = nutrition_totals
        
        # Update the document
        update_data = {k: v for k, v in data.items() if k != 'id' and k != 'userId'}
        doc_ref.update(update_data)
        
        # Return updated meal
        updated_meal = meal.copy()
        updated_meal.update(update_data)
        updated_meal['id'] = meal_id
        
        return updated_meal
    
    def delete(self, meal_id: str, user_id: str) -> bool:
        """Delete a meal"""
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