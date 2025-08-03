from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role', 'Customer') # Default role is Customer

    if not email or not password or not name:
        return jsonify({"msg": "Missing email, password, or name"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    new_user = User(email=email, name=name, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity={'email': user.email, 'role': user.role})
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Bad email or password"}), 401

# In a real application, you'd want to use a token blocklist for logout.
# For simplicity, we'll just have a placeholder endpoint.
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # To properly logout with JWT, you need to handle token revocation on the client side,
    # or implement a server-side token blocklist.
    return jsonify({"msg": "Logout successful (client should discard token)"}), 200

from decorators import admin_required

@auth_bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    current_user_identity = get_jwt_identity()
    user = User.query.filter_by(email=current_user_identity['email']).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if request.method == 'GET':
        return jsonify({
            "name": user.name,
            "email": user.email,
            "role": user.role,
        })

    if request.method == 'PUT':
        data = request.get_json()
        if 'name' in data:
            user.name = data['name']
        # Add other fields to update as needed
        db.session.commit()
        return jsonify({"msg": "Profile updated successfully"})

# Example of a protected route for admins
@auth_bp.route('/admin-test')
@jwt_required()
@admin_required
def admin_test():
    return jsonify(message="Welcome, Admin!")
