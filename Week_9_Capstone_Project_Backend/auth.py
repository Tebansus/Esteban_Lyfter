from flask import Blueprint, request, jsonify, Response, current_app
import hashlib
# Define blueprint
auth_blueprint = Blueprint('auth', __name__)
# Register and login methods taken from Week 7 and 8, blueprint division taken from week 8
@auth_blueprint.route('/register', methods=['POST'])
def register_user():    
    user_repo = current_app.config['USER_REPO']
    data = request.get_json()    
    if not data or not all(k in data for k in ['username', 'email', 'password', 'role_id']):
        return Response(status=400, response="Missing required fields, try again.")
    try:
        # Added password hasing to the Week 8 Solution
        hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()        
        user_repo.add_user(username=data['username'],email=data['email'],password=hashed_password,role_id=data["role_id"])
        return Response(status=201, response="User created successfully.")
    except Exception as e:        
        return Response(status=409, response=f"User could not be created. {e}")

# User authentication process to validate credentials and issue JWT token to be used for subsequent requests
@auth_blueprint.route('/login', methods=['POST'])
def login_user():    
    jwt_manager = current_app.config['JWT_MANAGER']
    user_repo = current_app.config['USER_REPO']
    data = request.get_json()

    if not data or not all(k in data for k in ['username', 'password']):
        return Response(status=400, response="Missing username or password.")  
   
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    user = user_repo.find_user_by_credentials(data['username'], hashed_password)
    if user:        
        token = jwt_manager.encode({'id': user.id, 'role': user.role_name})
        return jsonify(token=token), 200
    else:
        return Response(status=401, response="Invalid credentials.")