from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def role_required(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user and current_user.get('role') == role_name:
                return fn(*args, **kwargs)
            else:
                return jsonify({"msg": f"'{role_name}' access required"}), 403
        return wrapper
    return decorator

admin_required = role_required('Admin')
agent_required = role_required('Agent')
customer_required = role_required('Customer')
