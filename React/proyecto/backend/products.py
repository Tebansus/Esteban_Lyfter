from flask import Blueprint, request, jsonify, Response, current_app
from auth_wrapper import auth_required

products_blueprint = Blueprint('products', __name__)
# Product management endpoints
# First, the create product endpoint
# This endpoint allows admins to create new products by using the product repository
@products_blueprint.route('/products', methods=['POST'])
@auth_required(allowed_roles=['admin'])
def create_product():    
    product_repo = current_app.config['PRODUCT_REPO']
    data = request.get_json()
    
    if not data or not all(k in data for k in ['nombre', 'precio', 'stock']):
        return Response(status=400, response="Missing fields.")

    product_repo.add_product(nombre=data['nombre'],descripcion=data.get('descripcion', ''),precio=data['precio'],categoria=data.get('categoria',''),imagen=data.get('imagen',''),stock=data['stock'])
    return Response(status=201)

# This endpoint allows users to retrieve a list of all products
@products_blueprint.route('/products', methods=['GET'])
def get_all_products():
   
    product_repo = current_app.config['PRODUCT_REPO']
        
    products = product_repo.list_products()
    product_list = [dict(row._mapping) for row in products]
    
    return jsonify(product_list), 200

# This endpoint allows users to retrieve a single product by its ID
@products_blueprint.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):   
    product_repo = current_app.config['PRODUCT_REPO']

    product = product_repo.get_product_by_id(product_id)
    if not product:
        return Response(status=404)

    product_data = dict(product._mapping)
    return jsonify(product_data), 200

# This endpoint allows admins to update a product's details
@products_blueprint.route('/products/<int:product_id>', methods=['PUT'])
@auth_required(allowed_roles=['admin'])
def update_product(product_id):
    
    product_repo = current_app.config['PRODUCT_REPO']
    data = request.get_json()

    product_repo.modify_product(product_id, **data)
    
    return Response(status=204)

# This endpoint allows admins to delete a product
@products_blueprint.route('/products/<int:product_id>', methods=['DELETE'])
@auth_required(allowed_roles=['admin'])
def delete_product(product_id):   
    product_repo = current_app.config['PRODUCT_REPO']
    product_repo.delete_product(product_id)
    return Response(status=204)