from flask import Blueprint, request, jsonify, Response, current_app
from wrapper_file import auth_required

purchases_blueprint = Blueprint('purchases', __name__)

# Purchases and invoices enndpoints
# First, we need to create an endpoint to purchase a product
# This endpoint will allow a user to purchase a product by its id
# It will check if the product exists and if there is enough stock
# If the purchase is successful, it will create an invoice and return the invoice id
# iF the product does not exist or there is not enough stock, it will return a 409 Conflict response
@purchases_blueprint.route('/purchases', methods=['POST'])
@auth_required(allowed_roles=['user', 'admin'])
def purchase_product():
    db_manager = current_app.config['DB_MANAGER']
    cache = current_app.config['CACHE_MANAGER']
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
    # Delete the cache for the product and all products
    cache.delete("products_all", f"product:{product_id}")  
    return jsonify(invoice_id=invoice_id), 201


# list invoices endpoint
# This endpoint will return all invoices for the authenticated user
# It will return a list of invoices with their id, user id, product id, product name, unit price, quantity, total, and date of purchase
@purchases_blueprint.route('/invoices', methods=['GET'])
@auth_required(allowed_roles=['user', 'admin'])
def list_invoices():
    db_manager = current_app.config['DB_MANAGER']
    row = db_manager.get_invoices_by_user(request.user['id'])
    return jsonify([
        dict(id=r.id, user_id=r.user_id, product_id=r.product_id, product_name=r.product_name,
             unit_price=float(r.unit_price), quantity=r.quantity, total=float(r.total), date_of_purchase=r.date_of_purchase)
        for r in row
    ]), 200