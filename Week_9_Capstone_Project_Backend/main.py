import os
from flask import Flask, jsonify
from db import PgManager
from JWT_manager import JWT_Manager
from redis_manager import Cache_Manager
from dotenv import load_dotenv
#Import Repositories
from user_repo import UserRepo
from product_repo import ProductRepo
from cart_repo import CartRepo
from sales_repo import SalesRepo
from refund_repo import RefundRepo

#Import Blueprints
from auth import auth_blueprint
from products import products_blueprint
from sales import sales_blueprint

#Initialize app and environment
app = Flask("petstore-service")
load_dotenv()
# Initiliaze db manager
#
pg_manager = PgManager(db_name=os.getenv("DB_NAME"),user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"),host=os.getenv("DB_HOST"))
jwt_manager = JWT_Manager(private_key_path="keys/private.pem", public_key_path="keys/public.pem")
cache_manager = Cache_Manager()

# Initialize Repositories
user_repo = UserRepo(pg_manager)
product_repo = ProductRepo(pg_manager)
cart_repo = CartRepo(pg_manager)
sales_repo = SalesRepo(pg_manager)
refund_repo = RefundRepo(pg_manager)


# Make managers and repos available to blueprints
app.config['JWT_MANAGER'] = jwt_manager
app.config['CACHE_MANAGER'] = cache_manager
app.config['USER_REPO'] = user_repo
app.config['PRODUCT_REPO'] = product_repo
app.config['CART_REPO'] = cart_repo
app.config['SALES_REPO'] = sales_repo
app.config['REFUND_REPO'] = refund_repo

# Register Blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(products_blueprint, url_prefix='/api')
app.register_blueprint(sales_blueprint, url_prefix='/api')

# Liveness and health
@app.route("/health")
def health_check():   
    return jsonify({"status": "good"}), 200

# Call app
if __name__ == "__main__":
    
    app.run(debug=True, host="0.0.0.0", port=5000)