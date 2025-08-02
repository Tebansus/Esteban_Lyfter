from db import DB_Manager
from JWT_manager import JWT_Manager
from flask import Flask, request, Response, jsonify
from functools import wraps
# Define the Flask app and initialize the DB_Manager and JWT_Manager
# the DB_Manager will handle database operations and the JWT_Manager will handle JWT encoding and decoding
app = Flask("user-service")
db_manager = DB_Manager()
jwt_manager = JWT_Manager(private_key_path="keys/private.pem", public_key_path="keys/public.pem")
# Error handling function to return a response with a specific status code
def error(status):
    return Response(status=status)
# Decorator to check if the user is authenticated and has the required role
# This decorator will check the Authorization header for a Bearer token
# If the token is valid, it will allow access to the endpoint
# If the token is invalid or the user does not have the required role, it will return a 403 Forbidden response
def auth_required(allowed_roles=None):
    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            auth = request.headers.get('Authorization', '')
            if not auth.startswith('Bearer '):
                return error(403)
            token = auth.replace('Bearer ', '')
            decoded = jwt_manager.decode(token)
            if decoded is None:
                return error(403)
            if allowed_roles and decoded.get('role') not in allowed_roles:
                return error(403)
            request.user = decoded
            return func(*args, **kwargs)
        return decorated_function
    return wrapper
# Liveness endpoint to check if the service is running
@app.route("/liveness")
def liveness():
    return "<p>Hello, World!</p>"
# Register endpoint to create a new user
# This endpoint will accept a JSON payload with username, password, and role
# If the user is successfully created, it will return a JWT token and the user id
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True, silent=True) 
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')  # Default role is 'user'
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
@app.route('/login', methods=['POST'])
def login():
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
@app.route('/me')
@auth_required()
def me():
    user_row = db_manager.get_user_by_id(request.user['id'])
    if not user_row:
        return Response(status=404)
    return jsonify(id=user_row.id, username=user_row.username, role=user_row.role), 200

## Product CRUD operations endpoints
#The create_product endpoint allows an admin to add a new product to the catalog
# It requires the user to be authenticated and have the 'admin' role
# It will return the id of the newly created product

@app.route('/products', methods=['POST'])
@auth_required(allowed_roles=['admin'])
def create_product():
    data = request.get_json(force=True, silent=True) or {}
    required_fields = ['name', 'price', 'date_of_entry', 'quantity']
    if not all(field in data for field in required_fields):
        return Response(status=400)
    product_id = db_manager.insert_product(
        data['name'], data['price'], data['date_of_entry'], data['quantity']
    )
    return jsonify(id=product_id[0]), 201
# Get products endpoint
# This endpoint will return a list of all products in the catalog

# It will return a list of products with their id, name, price, date of entry, and quantity
@app.route('/products', methods=['GET'])
@auth_required()
def list_products():
    rows = db_manager.list_products()    
    
    return jsonify([dict(id=r.id, name=r.name, price=float(r.price), date_of_entry=r.Date_of_Entry, quantity=r.quantity) for r in rows]), 200
# Get product by id endpoint
# This endpoint will return a specific product by its id
# It requires the user to be authenticated, but does not require a specific role
# If the product does not exist, it will return a 404 Not Found response
@app.route('/products/<int:product_id>', methods=['GET'])
@auth_required()
def get_product(product_id):
    product = db_manager.get_product(product_id)
    if not product:
        return Response(status=404)
    return jsonify(id=product.id, name=product.name, price=float(product.price), date_of_entry=product.Date_of_Entry, quantity=product.quantity), 200
# Update product endpoint
# This endpoint allows an admin to update a product's information
# It requires the user to be authenticated and have the 'admin' role
@app.route('/products/<int:product_id>', methods=['PATCH'])
@auth_required(allowed_roles=['admin'])
def update_product(product_id):
    data = request.get_json(force=True, silent=True) or {}
    if not data:
        return Response(status=400)
    updated = db_manager.edit_product(product_id, **data)
    if updated == 0:
        return Response(status=404)
    return Response(status=204) 
# Delete product endpoint
# This endpoint allows an admin to delete a product by its id
# It requires the user to be authenticated and have the 'admin' role
@app.route('/products/<int:product_id>', methods=['DELETE'])
@auth_required(allowed_roles=['admin'])
def delete_product(product_id):
    deleted = db_manager.delete_product(product_id)
    if deleted == 0:
        return Response(status=404)
    return Response(status=204) 

#Purchases and invoices enndpoints
# First, we need to create an endpoint to purchase a product
# This endpoint will allow a user to purchase a product by its id
# It will check if the product exists and if there is enough stock
# If the purchase is successful, it will create an invoice and return the invoice id
# iF the product does not exist or there is not enough stock, it will return a 409 Conflict response
@app.route('/purchases', methods=['POST'])
@auth_required(allowed_roles=['user', 'admin'])
def purchase_product():
    data = request.get_json(force=True, silent=True) or {}
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    if not product_id or quantity <= 0:
        return Response(status=400)
    product = db_manager.get_product(product_id)
    if not product or product.quantity < quantity:
        return Response(status=409)
    #reduce stock
    reduce = db_manager.adjust_stock(product_id, -quantity)
    if not reduce:
        return Response(status=409)
    #create invoice
    invoice_id = db_manager.insert_invoice(
        user_id=request.user['id'],
        product_id=product.id,
        product_name=product.name,
        unit_price=product.price,
        quantity=quantity
    )
    return jsonify(invoice_id=invoice_id), 201
# list invoices endpoint
# This endpoint will return all invoices for the authenticated user
# It will return a list of invoices with their id, user id, product id, product name, unit price, quantity, total, and date of purchase
@app.route('/invoices', methods=['GET'])
@auth_required(allowed_roles=['user', 'admin'])
def list_invoices():
    row = db_manager.get_invoices_by_user(request.user['id'])
    return jsonify([
        dict(id=r.id, user_id=r.user_id, product_id=r.product_id, product_name=r.product_name,
             unit_price=float(r.unit_price), quantity=r.quantity, total=float(r.total), date_of_purchase=r.date_of_purchase)
        for r in row
    ]), 200
# Main entry point to run the Flask app
# This will start the Flask development server on localhost:5000
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
