from flask import Blueprint, request, jsonify, Response, current_app
from auth_wrapper import auth_required

products_blueprint = Blueprint('products', __name__)
# Product management endpoints
# First, the create product endpoint
# This endpoint allows admins to create new products by using the product repository
# AAlso, invalidates the product cache
@products_blueprint.route('/products', methods=['POST'])
@auth_required(allowed_roles=['admin'])
def create_product():    
    product_repo = current_app.config['PRODUCT_REPO']
    cache = current_app.config['CACHE_MANAGER']
    data = request.get_json()
    
    if not data or not all(k in data for k in ['name', 'price', 'stock_quantity']):
        return Response(status=400, response="Missing fields.")

    product_repo.add_product(name=data['name'],description=data.get('description', ''),price=data['price'],stock_quantity=data['stock_quantity'])
    cache.delete("all_products")  
    return Response(status=201)

 # This endpoint allows users to retrieve a list of all products, with caching
@products_blueprint.route('/products', methods=['GET'])
@auth_required()
def get_all_products():
   
    product_repo = current_app.config['PRODUCT_REPO']
    cache = current_app.config['CACHE_MANAGER']
    cache_key = "all_products"    
    cached_products = cache.get_json(cache_key)
    if cached_products:
        return jsonify(cached_products), 200
        
    products = product_repo.list_products()
    product_list = [dict(row) for row in products]
    
    cache.set_json(cache_key, product_list, ttl=300) # Cache for 5 minutes
    return jsonify(product_list), 200

# This endpoint allows users to retrieve a single product by its ID, with caching
@products_blueprint.route('/products/<int:product_id>', methods=['GET'])
@auth_required()
def get_product(product_id):   
    product_repo = current_app.config['PRODUCT_REPO']
    cache = current_app.config['CACHE_MANAGER']
    cache_key = f"product:{product_id}"

    cached_product = cache.get_json(cache_key)
    if cached_product:
        return jsonify(cached_product), 200

    product = product_repo.get_product_by_id(product_id)
    if not product:
        return Response(status=404)

    product_data = dict(product)
    cache.set_json(cache_key, product_data, ttl=300)
    return jsonify(product_data), 200

# This endpoint allows admins to update a product's details
@products_blueprint.route('/products/<int:product_id>', methods=['PUT'])
@auth_required(allowed_roles=['admin'])
def update_product(product_id):
    
    product_repo = current_app.config['PRODUCT_REPO']
    cache = current_app.config['CACHE_MANAGER']
    data = request.get_json()

    product_repo.modify_product(product_id, **data)
    
    # Invalidate caches
    cache.delete("all_products", f"product:{product_id}")
    return Response(status=204)

# This endpoint allows admins to delete a product, invalidating the cache
@products_blueprint.route('/products/<int:product_id>', methods=['DELETE'])
@auth_required(allowed_roles=['admin'])
def delete_product(product_id):   
    product_repo = current_app.config['PRODUCT_REPO']
    cache = current_app.config['CACHE_MANAGER']
    product_repo.delete_product(product_id)
    # Invalidate caches
    cache.delete("all_products", f"product:{product_id}")
    return Response(status=204)