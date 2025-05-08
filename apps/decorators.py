from functools import wraps
from flask import abort, jsonify
from flask_login import current_user
from .models.general.role import Role

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role_name):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator



# General position-based decorators for companies
def position_required(position_title):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not (current_user.is_authenticated and current_user.has_position(position_title)):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def it_administrator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        allowed_roles = ['IT Administrator', 'responsible']
        if not current_user.is_authenticated:
            return jsonify({"error": "User not authenticated"}), 403

        user_role = Role.query.filter_by(id=current_user.role_id).first()
        
        if user_role and user_role.position in allowed_roles:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized access"}), 403

    return decorated_function


def responsible_required(f):
    return position_required('responsible')(f)

def agent_required(f):
    return position_required('agent')(f)

def consultant_required(f):
    return position_required('consultant')(f)

def customer_required(f):
    return position_required('customer')(f)

