from flask import Blueprint, jsonify
from models import User
# In a real application, you would use authentication to get the current user's ID
# For now, we'll hardcode a user ID for testing purposes

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'level': user.level,
        'experience': user.experience,
        'currency': user.currency
    })