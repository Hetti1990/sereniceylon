from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import jwt_required
from decorators import admin_required

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required
@admin_required
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        })
    return jsonify(user_list)

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required
@admin_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role
    })

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
