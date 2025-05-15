from flask import Blueprint
recipes_bp = Blueprint('recipes', __name__)
from recipes import routes