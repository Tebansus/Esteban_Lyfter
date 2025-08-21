from flask import Blueprint, request, jsonify, Response, current_app
from wrapper_file import auth_required

products_blueprint = Blueprint('products', __name__)

# Product CRUD operations endpoints
#The create_product endpoint allows an admin to add a new product to the catalog
# It requires the user to be authenticated and have the 'admin' role
# It will return the id of the newly created product

@products_blueprint.route('/products', methods=['POST'])
@auth_required(allowed_roles=['admin'])
def create_product():
    db_manager = current_app.config['DB_MANAGER']
    cache = current_app.config['CACHE_MANAGER']
    data = request.get_json(force=True, silent=True) or {}
    required_fields = ['name', 'price', 'date_of_entry', 'quantity']
    if not all(field in data for field in required_fields):
        return Response(status=400)
    product_id = db_manager.insert_product(
        data['name'], data['price'], data['date_of_entry'], data['quantity']
    )
    cache.delete("products_all")
    return jsonify(id=product_id[0]), 201

# Get products endpoint
# This endpoint will return a list of all products in the catalog
# It will return a list of products with their id, name, price, date of entry, and quantity
#Added the cache functionality to store the list of products
# The cache will be used to store the list of products for 5 minutes
# If the cache is empty, it will fetch the products from the database and store them in it
@products_blueprint.route('/products', methods=['GET'])
@auth_required()
def list_products():
    db_manager = current_app.config['DB_MANAGER']
    cache = current_app.config['CACHE_MANAGER']
    cache_key = "products_all"
    cached = cache.get_json(cache_key)
    # use cache if available
    if cached is not None:
        return jsonify(cached), 200                      
    # If no cache, fetch from DB
    rows = db_manager.list_products()
    products = [
        dict(id=r.id, name=r.name, price=float(r.price), date_of_entry=r.Date_of_Entry, quantity=r.quantity) for r in rows
    ]
    # Store in cache
    cache.set_json(cache_key, products)                  
    return jsonify(products), 200

# Get product by id endpoint
# This endpoint will return a specific product by its id
# It requires the user to be authenticated, but does not require a specific role
# If the product does not exist, it will return a 404 Not Found response
# Added cache functionality to store the product details
# The cache will be used to store the product details for 5 minutes
@products_blueprint.route('/products/<int:product_id>', methods=['GET'])
@auth_required()
def get_product(product_id):
    db_manager = current_app.config['DB_MANAGER']
    cache = current_app.config['CACHE_MANAGER']
    cache_key = f"product:{product_id}"
    cached = cache.get_json(cache_key)
    # If cache is available, return it
    if cached is not None:
        return jsonify(cached), 200
    # Else, fetch from DB
    product = db_manager.get_product(product_id)
    if not product:
        return Response(status=404)

    product_data = dict(
        id=product.id, name=product.name, price=float(product.price),
        date_of_entry=product.Date_of_Entry, quantity=product.quantity
    )
    cache.set_json(cache_key, product_data)
    return jsonify(product_data), 200

# Update product endpoint
# This endpoint allows an admin to update a product's information
# It requires the user to be authenticated and have the 'admin' role
@products_blueprint.route('/products/<int:product_id>', methods=['PATCH'])
@auth_required(allowed_roles=['admin'])
def update_product(product_id):
    db_manager = current_app.config['DB_MANAGER']
    cache = current_app.config['CACHE_MANAGER']
    data = request.get_json(force=True, silent=True) or {}
    if not data:
        return Response(status=400)
    updated = db_manager.edit_product(product_id, **data)
    if updated == 0:
        return Response(status=404)
    # Delete the cache for the product and all products
    cache.delete("products_all", f"product:{product_id}")  
    return Response(status=204) 


# Delete product endpoint
# This endpoint allows an admin to delete a product by its id
# It requires the user to be authenticated and have the 'admin' role
@products_blueprint.route('/products/<int:product_id>', methods=['DELETE'])
@auth_required(allowed_roles=['admin'])
def delete_product(product_id):
    db_manager = current_app.config['DB_MANAGER']
    cache = current_app.config['CACHE_MANAGER']
    deleted = db_manager.delete_product(product_id)
    if deleted == 0:
        return Response(status=404)
    # Delete the cache for the product and all products
    cache.delete("products_all", f"product:{product_id}")   
    return Response(status=204) 
