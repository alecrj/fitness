import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration settings"""
    # Flask settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    SECRET_KEY = os.environ.get('SECRET_KEY', 'development-key')
    ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Firebase settings
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH', './firebase-credentials.json')
    FIREBASE_STORAGE_BUCKET = os.environ.get('FIREBASE_STORAGE_BUCKET', 'fitness-food-app-9d41d.firebasestorage.app')
    
    # External API settings
    USDA_API_KEY = os.environ.get('USDA_API_KEY')
    USDA_API_BASE_URL = 'https://api.nal.usda.gov/fdc/v1'
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Feature flags
    ENABLE_SOCIAL_FEATURES = os.environ.get('ENABLE_SOCIAL_FEATURES', 'True').lower() == 'true'
    ENABLE_RECIPE_IMPORT = os.environ.get('ENABLE_RECIPE_IMPORT', 'True').lower() == 'true'