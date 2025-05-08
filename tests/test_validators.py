import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os
from datetime import datetime
from flask import Flask, request, jsonify

# Add the parent directory to the path so we can import our app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.validators import (
    validate_string, validate_number, validate_date, validate_email,
    validate_url, validate_phone, validate_barcode, validate_enum,
    validate_array, validate_base64, validate_json,
    validate_request_body, validate_query_params
)


class TestValidators(unittest.TestCase):
    """Test cases for individual validator functions"""

    def test_validate_string(self):
        """Test string validation"""
        # Valid strings
        self.assertEqual(validate_string("test"), (True, None))
        self.assertEqual(validate_string("test", min_length=1, max_length=10), (True, None))
        self.assertEqual(validate_string("test", pattern=r'^[a-z]+$'), (True, None))
        
        # Invalid strings
        self.assertEqual(validate_string(""), (False, "Field is required"))
        self.assertEqual(validate_string("", required=False), (True, None))
        self.assertEqual(validate_string("a", min_length=2), (False, "Field must be at least 2 characters"))
        self.assertEqual(validate_string("toolong", max_length=5), (False, "Field must be at most 5 characters"))
        self.assertEqual(validate_string("test123", pattern=r'^[a-z]+$'), (False, "Field has an invalid format"))
        self.assertEqual(validate_string(123), (False, "Field must be a string"))
        
        # With field name
        self.assertEqual(validate_string("", field_name="Username"), (False, "Username is required"))
        
    def test_validate_number(self):
        """Test number validation"""
        # Valid numbers
        self.assertEqual(validate_number(10), (True, None))
        self.assertEqual(validate_number("10"), (True, None))  # String conversion
        self.assertEqual(validate_number(10.5), (True, None))
        self.assertEqual(validate_number(0), (True, None))
        self.assertEqual(validate_number(10, min_value=5, max_value=15), (True, None))
        
        # Invalid numbers
        self.assertEqual(validate_number(None), (False, "Field is required"))
        self.assertEqual(validate_number(None, required=False), (True, None))
        self.assertEqual(validate_number("abc"), (False, "Field must be a number"))
        self.assertEqual(validate_number(3, min_value=5), (False, "Field must be at least 5"))
        self.assertEqual(validate_number(20, max_value=15), (False, "Field must be at most 15"))
        self.assertEqual(validate_number(0, allow_zero=False), (False, "Field cannot be zero"))
        
        # With field name
        self.assertEqual(validate_number(None, field_name="Age"), (False, "Age is required"))
        
    def test_validate_date(self):
        """Test date validation"""
        # Valid dates
        self.assertEqual(validate_date("2021-01-01")[0:2], (True, None))
        self.assertEqual(validate_date("01/01/2021", format_str="%m/%d/%Y")[0:2], (True, None))
        
        min_date = datetime(2021, 1, 1)
        max_date = datetime(2021, 12, 31)
        self.assertEqual(validate_date("2021-06-15", min_date=min_date, max_date=max_date)[0:2], (True, None))
        
        # Invalid dates
        self.assertEqual(validate_date("")[0:2], (False, "Date is required"))
        self.assertEqual(validate_date("", required=False)[0:2], (True, None))
        self.assertEqual(validate_date("not-a-date")[0:2], (False, "Date must be in format %Y-%m-%d"))
        self.assertEqual(validate_date("2020-12-31", min_date=min_date)[0:2], 
                        (False, f"Date must be on or after {min_date.strftime('%Y-%m-%d')}"))
        self.assertEqual(validate_date("2022-01-01", max_date=max_date)[0:2],
                        (False, f"Date must be on or before {max_date.strftime('%Y-%m-%d')}"))
        
        # With field name
        self.assertEqual(validate_date("", field_name="Birth date")[0:2], 
                        (False, "Birth date is required"))
        
    def test_validate_email(self):
        """Test email validation"""
        # Valid emails
        self.assertEqual(validate_email("user@example.com"), (True, None))
        self.assertEqual(validate_email("user.name+tag@example.co.uk"), (True, None))
        
        # Invalid emails
        self.assertEqual(validate_email(""), (False, "Email is required"))
        self.assertEqual(validate_email("notanemail"), (False, "Email has an invalid format"))
        self.assertEqual(validate_email("user@"), (False, "Email has an invalid format"))
        self.assertEqual(validate_email("user@.com"), (False, "Email has an invalid format"))
        
    def test_validate_url(self):
        """Test URL validation"""
        # Valid URLs
        self.assertEqual(validate_url("https://example.com"), (True, None))
        self.assertEqual(validate_url("http://sub.example.co.uk/path"), (True, None))
        self.assertEqual(validate_url("example.com"), (True, None))  # Domain only
        
        # Invalid URLs
        self.assertEqual(validate_url(""), (False, "URL is required"))
        self.assertEqual(validate_url("not a url"), (False, "URL has an invalid format"))
        self.assertEqual(validate_url("http://"), (False, "URL has an invalid format"))
        
    def test_validate_phone(self):
        """Test phone number validation"""
        # Valid phone numbers
        self.assertEqual(validate_phone("1234567890"), (True, None))
        self.assertEqual(validate_phone("+11234567890"), (True, None))
        
        # Invalid phone numbers
        self.assertEqual(validate_phone(""), (False, "Phone number is required"))
        self.assertEqual(validate_phone("123"), (False, "Phone number has an invalid format"))
        self.assertEqual(validate_phone("123abc4567"), (False, "Phone number has an invalid format"))
        
    def test_validate_barcode(self):
        """Test barcode validation"""
        # Valid barcodes
        self.assertEqual(validate_barcode("12345678"), (True, None))        # UPC-8
        self.assertEqual(validate_barcode("123456789012"), (True, None))    # UPC-12
        self.assertEqual(validate_barcode("1234567890123"), (True, None))   # EAN-13
        self.assertEqual(validate_barcode("12345678901234"), (True, None))  # EAN-14
        
        # Invalid barcodes
        self.assertEqual(validate_barcode(""), (False, "Barcode is required"))
        self.assertEqual(validate_barcode("123"), (False, "Barcode has an invalid format"))
        self.assertEqual(validate_barcode("12345ABC"), (False, "Barcode has an invalid format"))
        
    def test_validate_enum(self):
        """Test enum validation"""
        allowed_values = ["apple", "banana", "orange"]
        
        # Valid enum values
        self.assertEqual(validate_enum("apple", allowed_values), (True, None))
        self.assertEqual(validate_enum("banana", allowed_values), (True, None))
        
        # Invalid enum values
        self.assertEqual(validate_enum(None, allowed_values), (False, "Field is required"))
        self.assertEqual(validate_enum("grape", allowed_values), 
                        (False, "Field must be one of: apple, banana, orange"))
        
        # With field name
        self.assertEqual(validate_enum("grape", allowed_values, field_name="Fruit"), 
                        (False, "Fruit must be one of: apple, banana, orange"))
        
    def test_validate_array(self):
        """Test array validation"""
        # Valid arrays
        self.assertEqual(validate_array([1, 2, 3]), (True, None))
        self.assertEqual(validate_array([1, 2, 3], min_length=2, max_length=5), (True, None))
        
        # With item validator
        def validate_item(item):
            if isinstance(item, int) and item > 0:
                return True, None
            return False, "Item must be a positive integer"
            
        self.assertEqual(validate_array([1, 2, 3], item_validator=validate_item), (True, None))
        
        # Invalid arrays
        self.assertEqual(validate_array(None), (False, "Array is required"))
        self.assertEqual(validate_array("not-an-array"), (False, "Field must be an array"))
        self.assertEqual(validate_array([1], min_length=2), (False, "Array must have at least 2 items"))
        self.assertEqual(validate_array([1, 2, 3, 4], max_length=3), (False, "Array must have at most 3 items"))
        self.assertEqual(validate_array([1, 2, 0, 4], item_validator=validate_item), 
                        (False, "Item 2 in array: Item must be a positive integer"))
        
    def test_validate_base64(self):
        """Test base64 validation"""
        # Valid base64 strings
        valid_base64 = "SGVsbG8gV29ybGQ="  # "Hello World" in base64
        self.assertEqual(validate_base64(valid_base64), (True, None))
        self.assertEqual(validate_base64(f"data:image/jpeg;base64,{valid_base64}"), (True, None))
        
        # Invalid base64 strings
        self.assertEqual(validate_base64(""), (False, "Base64 string is required"))
        self.assertEqual(validate_base64("not-base64!"), (False, "Base64 string is not valid base64 encoded data"))
        
    def test_validate_json(self):
        """Test JSON validation"""
        # Valid JSON
        valid_json = '{"name": "Test", "value": 123}'
        is_valid, error, parsed = validate_json(valid_json)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        self.assertEqual(parsed['name'], "Test")
        self.assertEqual(parsed['value'], 123)
        
        # Already parsed JSON
        is_valid, error, parsed = validate_json({"name": "Test", "value": 123})
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        self.assertEqual(parsed['name'], "Test")
        
        # With schema validation
        schema = {
            'name': {'type': 'string', 'required': True},
            'age': {'type': 'number', 'required': True}
        }
        
        valid_schema_json = '{"name": "Test", "age": 30}'
        is_valid, error, parsed = validate_json(valid_schema_json, schema)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        invalid_schema_json = '{"name": "Test"}'
        is_valid, error, parsed = validate_json(invalid_schema_json, schema)
        self.assertFalse(is_valid)
        self.assertIn("Missing required field: age", error)
        
        invalid_type_json = '{"name": 123, "age": 30}'
        is_valid, error, parsed = validate_json(invalid_type_json, schema)
        self.assertFalse(is_valid)
        self.assertIn("Field name must be a string", error)
        
        # Invalid JSON
        self.assertEqual(validate_json("")[0:2], (False, "JSON string is required"))
        self.assertEqual(validate_json("not-json")[0:2], (False, "JSON is not valid JSON"))


class TestDecorators(unittest.TestCase):
    """Test cases for validator decorators"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        
        # Define schemas for testing
        self.body_schema = {
            'name': {'type': 'string', 'required': True, 'min_length': 2},
            'age': {'type': 'number', 'required': True, 'min_value': 0},
            'email': {'type': 'email', 'required': False}
        }
        
        self.query_schema = {
            'page': {'type': 'number', 'required': False, 'min_value': 1},
            'limit': {'type': 'number', 'required': False, 'min_value': 1, 'max_value': 100},
            'sort': {'type': 'enum', 'required': False, 'values': ['asc', 'desc']}
        }
        
        # Set up test routes
        @self.app.route('/test-body', methods=['POST'])
        @validate_request_body(self.body_schema)
        def test_body_route():
            data = request.get_json()
            return jsonify({'success': True, 'data': data})
            
        @self.app.route('/test-query', methods=['GET'])
        @validate_query_params(self.query_schema)
        def test_query_route():
            params = request.args.to_dict()
            return jsonify({'success': True, 'params': params})
    
    def test_validate_request_body_decorator(self):
        """Test validate_request_body decorator"""
        # Valid request body
        response = self.client.post('/test-body', 
                                   json={'name': 'Test User', 'age': 30, 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Invalid request body - missing required field
        response = self.client.post('/test-body', 
                                   json={'name': 'Test User'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Validation failed')
        self.assertIn('age', data['details'])
        
        # Invalid request body - validation error
        response = self.client.post('/test-body', 
                                   json={'name': 'T', 'age': 30})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Validation failed')
        self.assertIn('name', data['details'])
        
        # Invalid JSON
        response = self.client.post('/test-body', 
                                   data='not-json',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid JSON in request body')
        
    def test_validate_query_params_decorator(self):
        """Test validate_query_params decorator"""
        # Valid query parameters
        response = self.client.get('/test-query?page=1&limit=20&sort=asc')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Empty query parameters (defaults)
        response = self.client.get('/test-query')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Invalid query parameter - validation error
        response = self.client.get('/test-query?page=0&limit=20')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Validation failed')
        self.assertIn('page', data['details'])
        
        # Invalid query parameter - enum value
        response = self.client.get('/test-query?sort=invalid')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Validation failed')
        self.assertIn('sort', data['details'])


if __name__ == '__main__':
    unittest.main()