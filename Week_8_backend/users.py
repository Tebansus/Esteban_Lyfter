from flask import Blueprint, request, jsonify, Response, current_app
from wrapper_file import auth_required, error

users_blueprint = Blueprint('users', __name__)

# Register endpoint to create a new user
# This endpoint will accept a JSON payload with username, password, and role
# If the user is successfully created, it will return a JWT token and the user id
@users_blueprint.route('/register', methods=['POST'])
def register():
    db_manager = current_app.config['DB_MANAGER']
    jwt_manager = current_app.config['JWT_MANAGER']
    data = request.get_json(force=True, silent=True) 
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')  
    if not username or not password or not role in ('user', 'admin'):
        return Response(status=400)
    try:
        user_id = db_manager.insert_user(username, password, role)
    except Exception:
        return Response(status=409)
    token = jwt_manager.encode({'id': user_id, 'role': role})
    return jsonify(token=token, id=user_id, role=role), 201

## Login endpoint to authenticate a user
# This endpoint will accept a JSON payload with username and password
# if the user is authenticated, it will return a JWT token
@users_blueprint.route('/login', methods=['POST'])
def login():
    db_manager = current_app.config['DB_MANAGER']
    jwt_manager = current_app.config['JWT_MANAGER']
    data = request.get_json(force=True, silent=True)
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return Response(status=400)
    user = db_manager.get_user(username, password)
    if not user:
        return Response(status=403)
    token = jwt_manager.encode({'id': user.id, 'role': user.role})
    return jsonify(token=token), 200

# Endpoint to get the authenticated user's information
# This endpoint will return the user's id, username, and role
@users_blueprint.route('/me')
@auth_required()
def me():
    db_manager = current_app.config['DB_MANAGER']
    user_row = db_manager.get_user_by_id(request.user['id'])
    if not user_row:
        return Response(status=404)
    return jsonify(id=user_row.id, username=user_row.username, role=user_row.role), 200