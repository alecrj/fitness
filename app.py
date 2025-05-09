import firebase_admin
from firebase_admin import credentials, firestore, storage
from config import Config
import time

# Record application start time
APP_START_TIME = time.time()

# Initialize Firebase only if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        'storageBucket': Config.FIREBASE_STORAGE_BUCKET
    })

# Create global db and bucket objects
db = firestore.client()
bucket = storage.bucket()

# Now set up Flask and blueprints
from flask import Flask, jsonify, request, g
from flask_cors import CORS
import uuid
import os

# Import blueprints
from auth.routes import auth_bp
from recipes.routes import recipes_bp
from nutrition.routes import nutrition_bp
from social.routes import social_bp

# Import utilities
from utils.error_handlers import register_error_handlers
from utils.logging import configure_logging, log_api_call, logger
from utils.background_tasks import get_task_status
from utils.monitoring import track_api_performance, get_performance_stats
from utils.health_check import check_health
from utils.rate_limit import standard_rate_limit

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Store start time in app context
    app.config['start_time'] = APP_START_TIME

    # Configure logging
    configure_logging()

    # Request ID middleware
    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        g.request_start_time = time.time()

    # Register request/response processors
    @app.after_request
    def add_response_headers(response):
        # Add request ID header
        response.headers['X-Request-ID'] = g.request_id
        
        # Add timing information
        if hasattr(g, 'request_start_time'):
            duration = time.time() - g.request_start_time
            response.headers['X-Response-Time'] = str(int(duration * 1000))  # in ms
            
        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Track API performance
        track_api_performance()
        
        return response
        
    # Register middleware for user identification
    @app.before_request
    def identify_user():
        from utils.firebase_admin import get_current_user
        user = get_current_user()
        if user:
            g.user_id = user['uid']
        else:
            g.user_id = 'anonymous'

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(recipes_bp, url_prefix='/api/recipes')
    app.register_blueprint(nutrition_bp, url_prefix='/api/nutrition')
    app.register_blueprint(social_bp, url_prefix='/api/social')

    # Register error handlers
    register_error_handlers(app)

    # Task status endpoint
    @app.route('/api/tasks/<task_id>', methods=['GET'])
    def get_task(task_id):
        """Get the status of a background task"""
        status = get_task_status(task_id)
        
        if not status:
            return jsonify({'error': 'Task not found'}), 404
            
        return jsonify(status)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    @standard_rate_limit()
    def health_check():
        """Health check endpoint for monitoring"""
        detailed = request.args.get('detailed', 'false').lower() == 'true'
        
        if detailed:
            # Full health check with all dependencies
            return jsonify(check_health())
        else:
            # Simple health check
            return jsonify({
                'status': 'healthy',
                'version': os.environ.get('APP_VERSION', '1.0.0'),
                'timestamp': time.time(),
            })

    # Metrics endpoint
    @app.route('/metrics', methods=['GET'])
    @standard_rate_limit()
    def metrics():
        """Metrics endpoint for monitoring"""
        # Check for API key if configured
        if app.config.get('METRICS_API_KEY'):
            api_key = request.headers.get('X-API-Key')
            if not api_key or api_key != app.config.get('METRICS_API_KEY'):
                return jsonify({'error': 'Unauthorized'}), 401
                
        # Get performance stats
        stats = get_performance_stats()
        
        return jsonify(stats)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"Server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500

    # Log startup
    logger.info(f"Application started in {app.config['ENV']} mode")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])