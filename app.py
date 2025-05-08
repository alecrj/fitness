import firebase_admin
from firebase_admin import credentials, firestore, storage
from config import Config

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
from flask import Flask, jsonify
from flask_cors import CORS

# Import blueprints
from auth.routes import auth_bp
from recipes.routes import recipes_bp
# from nutrition.routes import nutrition_bp
# from social.routes import social_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(recipes_bp, url_prefix='/api/recipes')
    # app.register_blueprint(nutrition_bp, url_prefix='/api/nutrition')
    # app.register_blueprint(social_bp, url_prefix='/api/social')

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'version': '1.0.0'})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])