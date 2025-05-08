from typing import Dict, Any, List, Callable, Optional, Tuple, Union
import re
from datetime import datetime
import json
import base64
from functools import wraps
from flask import request, jsonify

# Regular expression patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
BARCODE_PATTERN = r'^[0-9]{8,14}$'  # UPC/EAN barcodes are 8, 12, 13, or 14 digits
URL_PATTERN = r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
PHONE_PATTERN = r'^\+?[0-9]{10,15}$'


def validate_string(value: Any, min_length: int = 0, max_length: int = None, 
                    pattern: str = None, required: bool = True, field_name: str = None) -> Tuple[bool, Optional[str]]:
    """Validate a string value
    
    Args:
        value: The value to validate
        min_length: Minimum length of the string
        max_length: Maximum length of the string
        pattern: Regex pattern for validation
        required: Whether the field is required
        field_name: Name of the field for error messages
        
    Returns:
        Tuple containing (is_valid, error_message)
    """
    # Check if required
    if value is None or value == '':
        if required:
            return False, f"{field_name or 'Field'} is required"
        return True, None
        
    # Check type
    if not isinstance(value, str):
        return False, f"{field_name or 'Field'} must be a string"
        
    # Check length
    if min_length > 0 and len(value) < min_length:
        return False, f"{field_name or 'Field'} must be at least {min_length} characters"
        
    if max_length and len(value) > max_length:
        return False, f"{field_name or 'Field'} must be at most {max_length} characters"
        
    # Check pattern
    if pattern and not re.match(pattern, value):
        return False, f"{field_name or 'Field'} has an invalid format"
        
    return True, None


def validate_number(value: Any, min_value: Union[int, float] = None, max_value: Union[int, float] = None, 
                   required: bool = True, field_name: str = None, allow_zero: bool = True) -> Tuple[bool, Optional[str]]:
    """Validate a numeric value
    
    Args:
        value: The value to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        required: Whether the field is required
        field_name: Name of the field for error messages
        allow_zero: Whether zero is allowed
        
    Returns:
        Tuple containing (is_valid, error_message)
    """
    # Check if required
    if value is None:
        if required:
            return False, f"{field_name or 'Field'} is required"
        return True, None
        
    # Check type and convert
    try:
        num_value = float(value)
    except (ValueError, TypeError):
        return False, f"{field_name or 'Field'} must be a number"
        
    # Check zero
    if num_value == 0 and not allow_zero:
        return False, f"{field_name or 'Field'} cannot be zero"
        
    # Check range
    if min_value is not None and num_value < min_value:
        return False, f"{field_name or 'Field'} must be at least {min_value}"
        
    if max_value is not None and num_value > max_value:
        return False, f"{field_name or 'Field'} must be at most {max_value}"
        
    return True, None


def validate_date(value: Any, format_str: str = '%Y-%m-%d', 
                 min_date: datetime = None, max_date: datetime = None,
                 required: bool = True, field_name: str = None) -> Tuple[bool, Optional[str], Optional[datetime]]:
    """Validate a date string
    
    Args:
        value: The date string to validate
        format_str: Expected date format
        min_date: Minimum allowed date
        max_date: Maximum allowed date
        required: Whether the field is required
        field_name: Name of the field for error messages
        
    Returns:
        Tuple containing (is_valid, error_message, parsed_date)
    """
    # Check if required
    if not value:
        if required:
            return False, f"{field_name or 'Date'} is required", None
        return True, None, None
        
    # Parse date
    try:
        date = datetime.strptime(value, format_str)
    except (ValueError, TypeError):
        return False, f"{field_name or 'Date'} must be in format {format_str}", None
        
    # Check range
    if min_date and date < min_date:
        return False, f"{field_name or 'Date'} must be on or after {min_date.strftime(format_str)}", None
        
    if max_date and date > max_date:
        return False, f"{field_name or 'Date'} must be on or before {max_date.strftime(format_str)}", None
        
    return True, None, date


def validate_email(value: str, required: bool = True, field_name: str = "Email") -> Tuple[bool, Optional[str]]:
    """Validate an email address
    
    Args:
        value: The email to validate
        required: Whether the field is required
        field_name: Name of the field for error messages
        
    Returns:
        Tuple containing (is_valid, error_message)
    """
    return validate_string(value, pattern=EMAIL_PATTERN, required=required, field_name=field_name)


def validate_url(value: str, required: bool = True, field_name: str = "URL") -> Tuple[bool, Optional[str]]:
    """Validate a URL
    
    Args:
        value: The URL to validate
        required: Whether the field is required
        field_name: Name of the field for error messages
        
    Returns:
        Tuple containing (is_valid, error_message)
    """
    return validate_string(value, pattern=URL_PATTERN, required=required, field_name=field_name)


def validate_phone(value: str, required: bool = True, field_name: str = "Phone number") -> Tuple[bool, Optional[str]]:
    """Validate a phone number
    
    Args:
        value: The phone number to validate
        required: Whether the field is required
        field_name: Name of the field for error messages
        
    Returns:
        Tuple containing (is_valid, error_message)
    """
    return validate_string(value, pattern=PHONE_PATTERN, required=required, field_name=field_name)


def validate_barcode(value: str, required: bool = True, field_name: str = "Barcode") -> Tuple[bool, Optional[str]]:
    """Validate a product barcode
    
    Args:
        value: The barcode to validate
        required: Whether the field is required
        field_name: Name of the field for error messages
        
    Returns:
        Tuple containing (is_valid, error_message)
    """
    return validate_string(value, pattern=BARCODE_PATTERN, required=required, field_name=field_name)


def validate_enum(value: Any, allowed_values: List[Any], 
                 required: bool = True, field_name: str = None) -> Tuple[bool, Optional[str]]:
    """Validate that a value is in an allowed set
    
    Args:
        value: The value to validate
        allowed_values: List of allowed values
        required: Whether the field is required
        field_name: Name of the field for error messages
        
    Returns:
        Tuple containing (is_valid, error_message)
    """
    # Check if required
    if value is None:
        if required:
            return False, f"{field_name or 'Field'} is required"
        return True, None
        
    # Check if in allowed values
    if value not in allowed_values:
        values_str = ', '.join([str(v) for v in allowed_values])
        return False, f"{field_name or 'Field'} must be one of: {values_str}"
        
    return True, None


def validate_array(value: Any, min_length: int = 0, max_length: int = None,
                  item_validator: Callable = None, required: bool = True, 
                  field_name: str = None) -> Tuple[bool, Optional[str]]:
    """Validate an array/list
    
    Args:
        value: The array to validate
        min_length: Minimum length of the array
        max_length: Maximum length of the array
        item_validator: Function to validate each item
        required: Whether the field is required
        field_name: Name of the field for error messages
        
    Returns:
        Tuple containing (is_valid, error_message)
    """
    # Check if required
    if value is None:
        if required:
            return False, f"{field_name or 'Array'} is required"
        return True, None
        
    # Check type
    if not isinstance(value, (list, tuple)):
        return False, f"{field_name or 'Field'} must be an array"
        
    # Check length
    if min_length > 0 and len(value) < min_length:
        return False, f"{field_name or 'Array'} must have at least {min_length} items"
        
    if max_length and len(value) > max_length:
        return False, f"{field_name or 'Array'} must have at most {max_length} items"
        
    # Validate items
    if item_validator:
        for idx, item in enumerate(value):
            is_valid, error = item_validator(item)
            if not is_valid:
                return False, f"Item {idx} in {field_name or 'array'}: {error}"
                
    return True, None


def validate_base64(value: str, required: bool = True, field_name: str = None) -> Tuple[bool, Optional[str]]:
    """Validate a base64 encoded string
    
    Args:
        value: The base64 string to validate
        required: Whether the field is required
        field_name: Name of the field for error messages
        
    Returns:
        Tuple containing (is_valid, error_message)
    """
    # Check if required
    if not value:
        if required:
            return False, f"{field_name or 'Base64 string'} is required"
        return True, None
        
    # Check format
    if not isinstance(value, str):
        return False, f"{field_name or 'Base64 string'} must be a string"
        
    # Validate base64
    try:
        # Try to decode
        if ',' in value:
            # Handle data URLs (e.g. data:image/jpeg;base64,/9j/4AAQ...)
            value = value.split(',', 1)[1]
            
        base64.b64decode(value)
        return True, None
    except Exception:
        return False, f"{field_name or 'Base64 string'} is not valid base64 encoded data"


def validate_json(value: str, schema: Dict[str, Any] = None, 
                 required: bool = True, field_name: str = None) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """Validate a JSON string
    
    Args:
        value: The JSON string to validate
        schema: Dictionary defining the expected schema
        required: Whether the field is required
        field_name: Name of the field for error messages
        
    Returns:
        Tuple containing (is_valid, error_message, parsed_json)
    """
    # Check if required
    if not value:
        if required:
            return False, f"{field_name or 'JSON string'} is required", None
        return True, None, None
        
    # Parse JSON
    try:
        if isinstance(value, str):
            parsed = json.loads(value)
        elif isinstance(value, (dict, list)):
            parsed = value
        else:
            return False, f"{field_name or 'JSON'} must be a string or object", None
    except json.JSONDecodeError:
        return False, f"{field_name or 'JSON'} is not valid JSON", None
        
    # Validate against schema
    if schema:
        # Simple schema validation
        if isinstance(parsed, dict) and isinstance(schema, dict):
            for key, specs in schema.items():
                required_field = specs.get('required', True)
                
                if key not in parsed:
                    if required_field:
                        return False, f"Missing required field: {key}", None
                    continue
                    
                field_type = specs.get('type')
                if field_type:
                    if field_type == 'string' and not isinstance(parsed[key], str):
                        return False, f"Field {key} must be a string", None
                    elif field_type == 'number' and not isinstance(parsed[key], (int, float)):
                        return False, f"Field {key} must be a number", None
                    elif field_type == 'boolean' and not isinstance(parsed[key], bool):
                        return False, f"Field {key} must be a boolean", None
                    elif field_type == 'array' and not isinstance(parsed[key], list):
                        return False, f"Field {key} must be an array", None
                    elif field_type == 'object' and not isinstance(parsed[key], dict):
                        return False, f"Field {key} must be an object", None
        
    return True, None, parsed


def validate_request_body(schema: Dict[str, Dict[str, Any]]):
    """Decorator to validate request JSON body against a schema
    
    Args:
        schema: Dictionary defining field validation rules
        
    Example schema:
    {
        'name': {'type': 'string', 'required': True, 'min_length': 2, 'max_length': 100},
        'email': {'type': 'email', 'required': True},
        'age': {'type': 'number', 'required': False, 'min_value': 0, 'max_value': 120}
    }
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get request data
            data = request.get_json(silent=True)
            if not data:
                return jsonify({'error': 'Invalid JSON in request body'}), 400
                
            errors = {}
            
            # Validate each field
            for field_name, rules in schema.items():
                field_type = rules.get('type', 'string')
                required = rules.get('required', True)
                
                # Get field value
                value = data.get(field_name)
                
                # Apply validation based on type
                if field_type == 'string':
                    is_valid, error = validate_string(
                        value, 
                        min_length=rules.get('min_length', 0),
                        max_length=rules.get('max_length'),
                        pattern=rules.get('pattern'),
                        required=required,
                        field_name=field_name
                    )
                elif field_type == 'number':
                    is_valid, error = validate_number(
                        value,
                        min_value=rules.get('min_value'),
                        max_value=rules.get('max_value'),
                        required=required,
                        field_name=field_name,
                        allow_zero=rules.get('allow_zero', True)
                    )
                elif field_type == 'date':
                    is_valid, error, _ = validate_date(
                        value,
                        format_str=rules.get('format', '%Y-%m-%d'),
                        required=required,
                        field_name=field_name
                    )
                elif field_type == 'email':
                    is_valid, error = validate_email(
                        value,
                        required=required,
                        field_name=field_name
                    )
                elif field_type == 'url':
                    is_valid, error = validate_url(
                        value,
                        required=required,
                        field_name=field_name
                    )
                elif field_type == 'enum':
                    is_valid, error = validate_enum(
                        value,
                        allowed_values=rules.get('values', []),
                        required=required,
                        field_name=field_name
                    )
                elif field_type == 'array':
                    is_valid, error = validate_array(
                        value,
                        min_length=rules.get('min_length', 0),
                        max_length=rules.get('max_length'),
                        required=required,
                        field_name=field_name
                    )
                elif field_type == 'base64':
                    is_valid, error = validate_base64(
                        value,
                        required=required,
                        field_name=field_name
                    )
                else:
                    # Default to string validation
                    is_valid, error = validate_string(
                        value,
                        required=required,
                        field_name=field_name
                    )
                    
                # Add error if validation failed
                if not is_valid:
                    errors[field_name] = error
                    
            # Return errors if any
            if errors:
                return jsonify({'error': 'Validation failed', 'details': errors}), 400
                
            # Call the original function
            return f(*args, **kwargs)
            
        return decorated_function
    return decorator


def validate_query_params(schema: Dict[str, Dict[str, Any]]):
    """Decorator to validate request query parameters against a schema
    
    Args:
        schema: Dictionary defining field validation rules
        
    Example schema:
    {
        'page': {'type': 'number', 'required': False, 'min_value': 1},
        'limit': {'type': 'number', 'required': False, 'min_value': 1, 'max_value': 100},
        'sort': {'type': 'enum', 'required': False, 'values': ['asc', 'desc']}
    }
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            errors = {}
            
            # Validate each parameter
            for param_name, rules in schema.items():
                field_type = rules.get('type', 'string')
                required = rules.get('required', False)  # Default to not required for query params
                
                # Get parameter value
                value = request.args.get(param_name)
                
                # Skip validation if not required and not present
                if not required and not value:
                    continue
                    
                # Apply validation based on type
                if field_type == 'number':
                    try:
                        if value is not None:
                            value = int(value)
                    except ValueError:
                        errors[param_name] = f"{param_name} must be a number"
                        continue
                        
                    is_valid, error = validate_number(
                        value,
                        min_value=rules.get('min_value'),
                        max_value=rules.get('max_value'),
                        required=required,
                        field_name=param_name
                    )
                elif field_type == 'date':
                    is_valid, error, _ = validate_date(
                        value,
                        format_str=rules.get('format', '%Y-%m-%d'),
                        required=required,
                        field_name=param_name
                    )
                elif field_type == 'boolean':
                    if value is not None:
                        is_valid = value.lower() in ('true', 'false', '1', '0', 'yes', 'no')
                        error = f"{param_name} must be a boolean value" if not is_valid else None
                    else:
                        is_valid = not required
                        error = f"{param_name} is required" if not is_valid else None
                elif field_type == 'enum':
                    is_valid, error = validate_enum(
                        value,
                        allowed_values=rules.get('values', []),
                        required=required,
                        field_name=param_name
                    )
                else:
                    # Default to string validation
                    is_valid, error = validate_string(
                        value,
                        min_length=rules.get('min_length', 0),
                        max_length=rules.get('max_length'),
                        pattern=rules.get('pattern'),
                        required=required,
                        field_name=param_name
                    )
                    
                # Add error if validation failed
                if not is_valid:
                    errors[param_name] = error
                    
            # Return errors if any
            if errors:
                return jsonify({'error': 'Validation failed', 'details': errors}), 400
                
            # Call the original function
            return f(*args, **kwargs)
            
        return decorated_function
    return decorator


# Common schemas for reuse in API routes

USER_PROFILE_SCHEMA = {
    'name': {'type': 'string', 'required': True, 'min_length': 2, 'max_length': 100},
    'profile_image_base64': {'type': 'base64', 'required': False}
}

FOOD_ITEM_SCHEMA = {
    'name': {'type': 'string', 'required': True, 'min_length': 2, 'max_length': 100},
    'brand': {'type': 'string', 'required': False, 'max_length': 100},
    'serving_size': {'type': 'number', 'required': False, 'min_value': 0},
    'serving_unit': {'type': 'string', 'required': False, 'max_length': 20},
    'nutrition': {'type': 'object', 'required': False},
    'barcode': {'type': 'string', 'required': False, 'pattern': BARCODE_PATTERN},
    'is_favorite': {'type': 'boolean', 'required': False}
}

MEAL_SCHEMA = {
    'name': {'type': 'string', 'required': True, 'min_length': 2, 'max_length': 100},
    'meal_type': {'type': 'string', 'required': True},
    'meal_time': {'type': 'date', 'required': False, 'format': '%Y-%m-%dT%H:%M:%S'},
    'food_items': {'type': 'array', 'required': True, 'min_length': 1},
    'notes': {'type': 'string', 'required': False, 'max_length': 500},
    'tags': {'type': 'array', 'required': False}
}

RECIPE_SCHEMA = {
    'title': {'type': 'string', 'required': True, 'min_length': 2, 'max_length': 200},
    'description': {'type': 'string', 'required': False, 'max_length': 1000},
    'ingredients': {'type': 'array', 'required': True, 'min_length': 1},
    'instructions': {'type': 'array', 'required': True, 'min_length': 1},
    'prepTime': {'type': 'number', 'required': False, 'min_value': 0},
    'cookTime': {'type': 'number', 'required': False, 'min_value': 0},
    'servings': {'type': 'number', 'required': False, 'min_value': 1},
    'difficulty': {'type': 'string', 'required': False},
    'cuisine': {'type': 'string', 'required': False},
    'tags': {'type': 'array', 'required': False},
    'isPublic': {'type': 'boolean', 'required': False},
    'imageBase64': {'type': 'base64', 'required': False}
}

SOCIAL_POST_SCHEMA = {
    'content': {'type': 'string', 'required': True, 'min_length': 1, 'max_length': 2000},
    'imageBase64': {'type': 'base64', 'required': False},
    'recipeId': {'type': 'string', 'required': False},
    'mealId': {'type': 'string', 'required': False},
    'tags': {'type': 'array', 'required': False}
}

COMMENT_SCHEMA = {
    'content': {'type': 'string', 'required': True, 'min_length': 1, 'max_length': 500},
    'postId': {'type': 'string', 'required': True}
}

# Common query parameter schemas

PAGINATION_SCHEMA = {
    'limit': {'type': 'number', 'required': False, 'min_value': 1, 'max_value': 100},
    'offset': {'type': 'number', 'required': False, 'min_value': 0}
}

FOOD_QUERY_SCHEMA = {
    'limit': {'type': 'number', 'required': False, 'min_value': 1, 'max_value': 100},
    'offset': {'type': 'number', 'required': False, 'min_value': 0},
    'q': {'type': 'string', 'required': False},
    'is_favorite': {'type': 'boolean', 'required': False},
    'is_custom': {'type': 'boolean', 'required': False},
    'sort_by': {'type': 'enum', 'required': False, 'values': ['created_at', 'name', 'calories']},
    'sort_dir': {'type': 'enum', 'required': False, 'values': ['asc', 'desc']}
}

MEAL_QUERY_SCHEMA = {
    'limit': {'type': 'number', 'required': False, 'min_value': 1, 'max_value': 100},
    'offset': {'type': 'number', 'required': False, 'min_value': 0},
    'date': {'type': 'date', 'required': False},
    'meal_type': {'type': 'string', 'required': False},
    'tag': {'type': 'string', 'required': False},
    'sort_by': {'type': 'enum', 'required': False, 'values': ['meal_time', 'created_at']},
    'sort_dir': {'type': 'enum', 'required': False, 'values': ['asc', 'desc']}
}

RECIPE_QUERY_SCHEMA = {
    'limit': {'type': 'number', 'required': False, 'min_value': 1, 'max_value': 100},
    'offset': {'type': 'number', 'required': False, 'min_value': 0},
    'q': {'type': 'string', 'required': False},
    'tags': {'type': 'string', 'required': False},
    'cuisine': {'type': 'string', 'required': False},
    'difficulty': {'type': 'string', 'required': False},
    'includePublic': {'type': 'boolean', 'required': False}
}

SOCIAL_QUERY_SCHEMA = {
    'limit': {'type': 'number', 'required': False, 'min_value': 1, 'max_value': 100},
    'offset': {'type': 'number', 'required': False, 'min_value': 0},
    'userId': {'type': 'string', 'required': False},
    'tag': {'type': 'string', 'required': False},
    'recipeId': {'type': 'string', 'required': False},
    'mealId': {'type': 'string', 'required': False},
    'feed': {'type': 'enum', 'required': False, 'values': ['all', 'profile', 'following']}
}