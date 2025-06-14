from flask import Blueprint, request, jsonify

# Blueprint for the API to communicate with the modification repository and main. 
api_bp = Blueprint('api', __name__)
mod_repo = None  
# Inititate the API with the modification repository, which will be used to handle requests.
def init_api(repo):
    global mod_repo
    mod_repo = repo
# API to create users, with post method to handle user creation.
@api_bp.route('/user-create', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    success = mod_repo.add_user(name, email, username, password)
    if success:
        return jsonify({'message': 'User created successfully'}), 201
    else:
        return jsonify({'message': 'Failed to create user.'}), 400
# API to create cars, with post method to handle car creation.
@api_bp.route('/car-create', methods=['POST'])
def create_car():
    data = request.get_json()
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    success = mod_repo.add_car(make, model, year)
    if success:
        return jsonify({'message': 'Car created successfully'}), 201
    else:
        return jsonify({'message': 'Failed to create car.'}), 400
# API to create rentals, with post method to handle rental creation.
@api_bp.route('/rental-create', methods=['POST'])
def create_rental():
    data = request.get_json()
    user_id = data.get('user_id')
    car_id = data.get('car_id')
    success = mod_repo.generate_new_rental(user_id, car_id)
    
    if success:
        mod_repo.modify_car_rented_state(car_id, 'RENTED')
        return jsonify({'message': 'Rental created successfully'}), 201
    else:
        return jsonify({'message': 'Failed to create rental.'}), 400
# API to modify the rented state of a car, with patch method to handle state modification.
@api_bp.route('/car-state-modify', methods=['PATCH'])
def modify_car_state():
    data = request.get_json()
    car_id = data.get('car_id')
    rented_state = data.get('rented_state')
    
    if not car_id or not rented_state:
        return jsonify({'message': 'Car ID and new rented state are needed.'}), 400
    
    success = mod_repo.modify_car_rented_state(car_id, rented_state)
    
    if success:
        return jsonify({'message': 'Car rented state modified successfully'}), 200
    else:
        return jsonify({'message': 'Failed to modify car rented state.'}), 400
# API to modify the state of an account, with patch method to handle state modification.
@api_bp.route('/account-state-modify', methods=['PATCH'])
def modify_account_state():
    data = request.get_json()
    email = data.get('email')
    new_state = data.get('new_state')
    
    if not email or not new_state:
        return jsonify({'message': 'Email and new state are needed.'}), 400
    
    success = mod_repo.modify_account_state(email, new_state)
    
    if success:
        return jsonify({'message': 'Account state modified successfully'}), 200
    else:
        return jsonify({'message': 'Failed to modify account state.'}), 400
# API to end a rental, with patch method to handle rental ending.  
@api_bp.route('/rental-end', methods=['PATCH'])
def end_rental():
    data = request.get_json()
    rental_id = data.get('rental_id')
    
    if not rental_id:
        return jsonify({'message': 'Rental ID is needed.'}), 400
    
    success = mod_repo.end_rental(rental_id)
    
    if success:        
        return jsonify({'message': 'Rental ended successfully'}), 200
    else:
        return jsonify({'message': 'Failed to end rental.'}), 400
    
# API to modify the state of a rental, with patch method to handle state modification.
@api_bp.route('/rental-state-modify', methods=['PATCH'])
def modify_rental_state():
    data = request.get_json()
    rental_id = data.get('rental_id')
    new_state = data.get('new_state')
    
    if not rental_id or not new_state:
        return jsonify({'message': 'Rental ID and new state are needed.'}), 400
    
    success = mod_repo.modify_rental_status(rental_id, new_state)
    
    if success:
        return jsonify({'message': 'Rental status modified successfully'}), 200
    else:
        return jsonify({'message': 'Failed to modify rental status.'}), 400
# API to flag a user as a defaulter, with patch method to handle user flagging.
@api_bp.route('/flag-defaulter', methods=['PATCH'])
def flag_defaulter():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'message': 'Email is needed.'}), 400
    
    success = mod_repo.modify_account_state(email, 'DEFAULTER')
    
    if success:
        return jsonify({'message': 'User flagged as defaulter.'}), 200
    else:
        return jsonify({'message': 'Failed to flag user as defaulter.'}), 400
# API endpoints to list users with filter, with get method to handle user listing.
@api_bp.route('/list-users', methods=['GET'])
def list_users():
    filters = request.args.to_dict()       
    users = mod_repo.get_all_users(filters)
    if users:
        return jsonify(users), 200
    return jsonify({'message': 'No users found.'}), 404
# API endpoints to list cars with filter, with get method to handle car listing.
@api_bp.route('/list-cars', methods=['GET'])
def list_cars():
    filters = request.args.to_dict()
    cars = mod_repo.get_all_cars(filters)
    if cars:
        return jsonify(cars), 200
    return jsonify({'message': 'No cars found.'}), 404
# API endpoints to list rentals with filter, with get method to handle rental listing.
@api_bp.route('/list-rentals', methods=['GET'])
def list_rentals():
    filters = request.args.to_dict()
    rentals = mod_repo.get_all_rentals(filters)
    if rentals:
        return jsonify(rentals), 200
    return jsonify({'message': 'No rentals found.'}), 404