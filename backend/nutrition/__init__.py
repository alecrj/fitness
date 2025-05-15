# nutrition/__init__.py
from flask import Blueprint
nutrition_bp = Blueprint('nutrition', __name__)
from nutrition import routes