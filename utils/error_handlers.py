"""Error handling utilities for Flask application"""
from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
import firebase_admin.exceptions
import requests.exceptions
from utils.logging import logger, log_exception

def register_error_handlers(app):
    """Register error handlers for the Flask app
    
    Args:
        app: Flask application instance
    """
    @app.errorhandler(400)
    def bad_request(e):
        """Handle bad request errors"""
        return handle_http_error(e, 400, "Bad Request")
    
    @app.errorhandler(401)
    def unauthorized(e):
        """Handle unauthorized errors"""
        return handle_http_error(e, 401, "Unauthorized")
    
    @app.errorhandler(403)
    def forbidden(e):
        """Handle forbidden errors"""
        return handle_http_error(e, 403, "Forbidden")
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle not found errors"""
        return handle_http_error(e, 404, "Not Found")
    
    @app.errorhandler(429)
    def too_many_requests(e):
        """Handle rate limit exceeded errors"""
        return handle_http_error(e, 429, "Too Many Requests")
    
    @app.errorhandler(500)
    def internal_server_error(e):
        """Handle internal server errors"""
        return handle_http_error(e, 500, "Internal Server Error")
    
    @app.errorhandler(ValueError)
    def handle_value_error(e):
        """Handle ValueError exceptions"""
        log_exception(e)
        return jsonify({
            'error': 'Validation Error',
            'message': str(e)
        }), 400
    
    @app.errorhandler(firebase_admin.exceptions.FirebaseError)
    def handle_firebase_error(e):
        """Handle Firebase-related errors"""
        log_exception(e)
        
        # Determine appropriate status code
        if 'PERMISSION_DENIED' in str(e):
            status_code = 403
            error_type = 'Permission Denied'
        elif 'NOT_FOUND' in str(e):
            status_code = 404
            error_type = 'Not Found'
        elif 'UNAUTHENTICATED' in str(e):
            status_code = 401
            error_type = 'Unauthorized'
        else:
            status_code = 500
            error_type = 'Firebase Error'
            
        return jsonify({
            'error': error_type,
            'message': str(e)
        }), status_code
    
    @app.errorhandler(requests.exceptions.RequestException)
    def handle_request_error(e):
        """Handle external API request errors"""
        log_exception(e)
        
        # Determine if this is a timeout or connectivity issue
        if isinstance(e, requests.exceptions.Timeout):
            error_type = 'External API Timeout'
        elif isinstance(e, requests.exceptions.ConnectionError):
            error_type = 'External API Connection Error'
        else:
            error_type = 'External API Error'
            
        # Only show detailed error in development
        if current_app.debug:
            message = str(e)
        else:
            message = "Error communicating with external service"
            
        return jsonify({
            'error': error_type,
            'message': message
        }), 503  # Service Unavailable
    
    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        """Handle any unhandled exceptions"""
        log_exception(e)
        
        # In production, hide detailed error messages for security
        if current_app.debug:
            message = str(e)
        else:
            message = "An unexpected error occurred"
            
        return jsonify({
            'error': 'Server Error',
            'message': message
        }), 500

def handle_http_error(e, status_code, default_message):
    """Common handler for HTTP errors
    
    Args:
        e: The exception
        status_code: HTTP status code
        default_message: Default message if exception doesn't have one
        
    Returns:
        JSON response with error details
    """
    # Log the error
    logger.error(f"HTTP {status_code}: {str(e)}")
    
    # Get error description
    if isinstance(e, HTTPException):
        description = e.description
    else:
        description = str(e) if str(e) else default_message
        
    # Return JSON response
    return jsonify({
        'error': default_message,
        'message': description
    }), status_code

def handle_validation_error(errors):
    """Format validation errors into a standardized response
    
    Args:
        errors: Dictionary of validation errors by field
        
    Returns:
        JSON response with validation errors
    """
    return jsonify({
        'error': 'Validation Error',
        'details': errors
    }), 400