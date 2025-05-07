import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', './firebase-credentials.json')
    FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET', 'your-project-id.appspot.com')
    USDA_API_KEY = os.getenv('USDA_API_KEY', 'your-usda-api-key')
    USDA_API_BASE_URL = 'https://api.nal.usda.gov/fdc/v1'
    DEFAULT_FEED_PAGE_SIZE = int(os.getenv('DEFAULT_FEED_PAGE_SIZE', 20))

class ProductionConfig(Config):
    DEBUG = False
    def __init__(self):
        required = ['SECRET_KEY', 'FIREBASE_CREDENTIALS_PATH', 'FIREBASE_STORAGE_BUCKET', 'USDA_API_KEY']
        missing = [var for var in required if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")