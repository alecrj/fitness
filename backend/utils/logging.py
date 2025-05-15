"""Logging utilities for the application"""
import logging
import json
import traceback
import time
import os
from flask import request, g, has_request_context
from functools import wraps

# Configure logging
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create logger
logger = logging.getLogger('fitness_food_app')

class StructuredLogRecord(logging.LogRecord):
    """Extended LogRecord that adds structured data for better log analysis"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add request context if available
        if has_request_context():
            self.request_id = getattr(g, 'request_id', 'unknown')
            self.method = request.method
            self.path = request.path
            self.ip = request.remote_addr
            self.user_agent = request.headers.get('User-Agent', 'unknown')
            # Add user ID if available
            self.user_id = getattr(g, 'user_id', 'anonymous')
        else:
            self.request_id = 'no-request'
            
def configure_logging():
    """Configure advanced logging settings"""
    # Set custom log record factory
    logging.setLogRecordFactory(StructuredLogRecord)
    
    # Add file handler if configured
    log_file = os.environ.get('LOG_FILE')
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)

def log_request_details(include_headers=False, include_body=False):
    """Log detailed information about the request
    
    Args:
        include_headers: Whether to include request headers in the log
        include_body: Whether to include request body in the log
    """
    if not has_request_context():
        return
        
    details = {
        'method': request.method,
        'path': request.path,
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent')
    }
    
    # Add headers if requested (exclude sensitive ones)
    if include_headers:
        sensitive_headers = {'authorization', 'cookie', 'x-api-key'}
        safe_headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in sensitive_headers
        }
        details['headers'] = safe_headers
        
    # Add body if requested (and if it's JSON)
    if include_body and request.is_json:
        try:
            # Make a copy to avoid consuming the request data
            body = request.get_json(silent=True)
            if body:
                # Sanitize any sensitive fields
                sanitized_body = sanitize_sensitive_data(body)
                details['body'] = sanitized_body
        except Exception:
            details['body_error'] = 'Could not parse JSON body'
            
    logger.info(f"Request details: {json.dumps(details)}")

def sanitize_sensitive_data(data, sensitive_fields=None):
    """Remove sensitive data from logs
    
    Args:
        data: Dictionary to sanitize
        sensitive_fields: List of field names to redact
        
    Returns:
        Sanitized dictionary
    """
    if sensitive_fields is None:
        sensitive_fields = {
            'password', 'token', 'api_key', 'secret', 'credit_card',
            'card_number', 'cvv', 'ssn', 'social_security'
        }
        
    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            if key.lower() in sensitive_fields:
                sanitized[key] = '*** REDACTED ***'
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_sensitive_data(value, sensitive_fields)
            else:
                sanitized[key] = value
        return sanitized
    elif isinstance(data, list):
        return [sanitize_sensitive_data(item, sensitive_fields) for item in data]
    else:
        return data

def log_api_call(f):
    """Decorator to log API calls with timing information"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        # Generate request ID if not present
        if not hasattr(g, 'request_id'):
            import uuid
            g.request_id = str(uuid.uuid4())
            
        # Log request
        logger.info(f"API call started: {request.method} {request.path}")
        
        try:
            # Execute the API call
            response = f(*args, **kwargs)
            
            # Log success
            duration = time.time() - start_time
            logger.info(
                f"API call completed: {request.method} {request.path} "
                f"- Status: {response.status_code} - Duration: {duration:.3f}s"
            )
            
            return response
        except Exception as e:
            # Log exception
            duration = time.time() - start_time
            logger.error(
                f"API call failed: {request.method} {request.path} "
                f"- Error: {str(e)} - Duration: {duration:.3f}s",
                exc_info=True
            )
            
            # Log traceback for errors
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Re-raise the exception
            raise
            
    return decorated_function

def log_exception(e):
    """Log an exception with detailed information
    
    Args:
        e: The exception to log
    """
    logger.error(f"Exception: {str(e)}", exc_info=True)
    if has_request_context():
        logger.error(f"Request details: {request.method} {request.path}")
        
        # Log user information if available
        from utils.firebase_admin import get_current_user
        user = get_current_user()
        if user:
            logger.error(f"User: {user.get('uid')}")