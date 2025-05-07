from flask import jsonify, request
from utils.firebase_admin import auth_required
from auth import auth_bp  # Import auth_bp from auth/__init__.py
import firebase_admin
from firebase_admin import firestore, storage
from datetime import datetime
import uuid
import base64
from io import BytesIO

@auth_bp.route('/profile', methods=['POST'])
@auth_required
def create_profile(user_id):
    db = firebase_admin.firestore.client()
    bucket = firebase_admin.storage.bucket()
    
    data = request.get_json()
    name = data.get('name')
    image_base64 = data.get('profile_image_base64')
    image_url = None
    if image_base64:
        image_data = base64.b64decode(image_base64)
        image_path = f"profiles/{user_id}/{uuid.uuid4()}.jpg"
        blob = bucket.blob(image_path)
        blob.upload_from_string(image_data, content_type='image/jpeg')
        image_url = blob.public_url
    user = {
        'id': user_id,
        'name': name or 'User',
        'profile_image_url': image_url,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    db.collection('users').document(user_id).set(user)
    return jsonify(user), 201

@auth_bp.route('/profile', methods=['GET'])
@auth_required
def get_profile(user_id):
    db = firebase_admin.firestore.client()
    doc = db.collection('users').document(user_id).get()
    if doc.exists:
        user = doc.to_dict()
        user['id'] = doc.id
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404