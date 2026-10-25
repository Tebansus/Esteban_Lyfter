from flask import Blueprint, request, jsonify, Response, current_app
from auth_wrapper import auth_required
from decimal import Decimal

# Main sales repo. This handles all sales-related operations.
# It provides methods to manage the shopping cart, process checkouts, and handle invoices.
# It uses blueprints to organize routes and handlers away from the main application logic.
# It calls the necessary repositories using the current application context, which all have the necessary methods for data access.

sales_blueprint = Blueprint('sales', __name__)
# First, the view cart endpoint that allows users to see their current cart items.
@sales_blueprint.route('/cart', methods=['GET'])
@auth_required()
def view_cart():    
    cart_repo = current_app.config['CART_REPO']
    user_id = request.user['id']
    
    active_cart = cart_repo.get_active_cart_by_user(user_id)
    if not active_cart:
        return jsonify({"message": "Your cart is empty."}), 200        
    items = cart_repo.get_cart_items(active_cart.id)
    return jsonify({"cart_id": active_cart.id, "items": [dict(item) for item in items]}), 200

# Add to cart endpoint that allows users to add items to their cart.
# Calls the necessary repositories to add the item to the cart.
@sales_blueprint.route('/cart/items', methods=['POST'])
@auth_required()
def add_to_cart():    
    cart_repo = current_app.config['CART_REPO']
    product_repo = current_app.config['PRODUCT_REPO']
    user_id = request.user['id']
    data = request.get_json()
    if not data or not all(k in data for k in ['product_id', 'quantity']):
        return Response(status=400, response="Missing product_id or quantity.")

    product = product_repo.get_product_by_id(data['product_id'])
    if not product or product.stock < data['quantity']:
        return Response(status=409, response="Product not available or insufficient stock.")

    active_cart = cart_repo.get_active_cart_by_user(user_id)
    if not active_cart:
        cart_repo.create_cart(user_id)
        active_cart = cart_repo.get_active_cart_by_user(user_id)

    cart_repo.add_item_to_cart(active_cart.id, data['product_id'], data['quantity'])
    return Response(status=201, response="Item added to cart.")

# Checkout endpoint that allows users to finalize their purchases.
# It validates stock, creates an invoice, adjusts stock levels, and cleans up the cart.
@sales_blueprint.route('/checkout', methods=['POST'])
@auth_required()
def checkout():    
    cart_repo = current_app.config['CART_REPO']
    sales_repo = current_app.config['SALES_REPO']
    product_repo = current_app.config['PRODUCT_REPO']
    user_id = request.user['id']
    data = request.get_json()

    if not data or 'shipping_address' not in data:
        return Response(status=400, response="Shipping address is required.")

    items = data.get('items', [])
    if not items:
        return Response(status=400, response="Cart is empty.")
    
    # Validate stock and calculate total price 
    total_price = Decimal('0.00')
    products_to_add = []
    for item in items:
        product = product_repo.get_product_by_id(item['product_id'])
        if product is None or product.stock < item['quantity']:
            return Response(status=409, response=f"Insufficient stock for product ID {item['product_id']}.")
        
        price_at_purchase = Decimal(str(product.precio))
        total_price += price_at_purchase * item['quantity']
        products_to_add.append({
            "product_id": item['product_id'],
            "name": product.nombre,
            "quantity": item['quantity'],
            "price_at_purchase": price_at_purchase
        })

    # Add address and get its ID
    address_id = sales_repo.add_address(user_id=user_id, address_line=data['shipping_address'], city="Unknown", state="Unknown", postal_code="00000", country="Unknown")

    # Create invoice and get its ID
    invoice_id = sales_repo.create_invoice(user_id=user_id, address_id=address_id, total=total_price)

    for product_item in products_to_add:
        # Add item to the invoice
        sales_repo.add_invoice_item(invoice_id=invoice_id, product_id=product_item['product_id'], quantity=product_item['quantity'], price=product_item['price_at_purchase'])
        # Atomically decrease the product's stock
        product_repo.adjust_stock(product_item['product_id'], quantity_delta=-product_item['quantity'])

    # Finalize cart if it exists in backend
    active_cart = cart_repo.get_active_cart_by_user(user_id)
    if active_cart:
        cart_repo.update_cart_status(active_cart.id, 'completed')

    # Send real email
    import smtplib
    from email.message import EmailMessage

    buyer_name = data.get('buyer_name', 'Cliente')
    buyer_email = data.get('buyer_email')
    shipping_address = data.get('shipping_address')

    msg = EmailMessage()
    msg['Subject'] = 'Confirmación de compra en PawStore'
    msg['From'] = 'noreply@pawstore.com'
    msg['To'] = buyer_email

    items_detail = ""
    for p in products_to_add:
        items_detail += f"- {p['name']} (x{p['quantity']}): ${p['price_at_purchase'] * p['quantity']}\n"

    msg.set_content(f"""Hola {buyer_name},

Tu compra por un total de ${total_price} ha sido confirmada.
Se enviará a: {shipping_address}

Detalle de los productos:
{items_detail}

Gracias por tu compra.
El equipo de PawStore""")

    try:
        # Send via local SMTP server (like MailHog) or a real one if configured
        with smtplib.SMTP('localhost', 1025) as server:
            server.send_message(msg)
    except Exception as e:
        print(f"No se pudo enviar el correo real: {e}")
        # Fallback to console print for debug
        print(f"\n--- EMAIL SIMULADO ---")
        print(msg.as_string())
        print(f"----------------------\n")

    return jsonify({"message": "Checkout successful", "invoice_id": invoice_id, "total_price": str(total_price)}), 200

# Refund processing endpoint that allows admins to process refunds.
# It validates the refund request and updates the necessary records.
# Logs the refund action in the refund repository.
@sales_blueprint.route('/refunds', methods=['POST'])
@auth_required(allowed_roles=['admin'])
def process_refund():
   
    refund_repo = current_app.config['REFUND_REPO']
    product_repo = current_app.config['PRODUCT_REPO']
    data = request.get_json()

    required_fields = ['invoice_id', 'product_id', 'quantity', 'reason']
    if not data or not all(field in data for field in required_fields):
        return Response(status=400, response="Missing required fields for refund.")

    # Create the refund record in the database
    refund_repo.create_refund(invoice_id=data['invoice_id'],product_id=data['product_id'],quantity=data['quantity'], reason=data['reason'])

    # Restore the stock quantity for the refunded product
    product_repo.adjust_stock(product_id=data['product_id'], quantity_delta=data['quantity'])


    return jsonify({"message": "Refund processed successfully."}), 201