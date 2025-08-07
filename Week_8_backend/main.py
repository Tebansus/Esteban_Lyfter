from db import DB_Manager
from JWT_manager import JWT_Manager
from flask import Flask
from redis_manager import Cache_Manager

from users import users_blueprint
from products import products_blueprint
from purchases import purchases_blueprint


# Define the Flask app and initialize the DB_Manager and JWT_Manager
# the DB_Manager will handle database operations and the JWT_Manager will handle JWT encoding and decoding
app = Flask("user-service")
db_manager = DB_Manager()
jwt_manager = JWT_Manager(private_key_path="keys/private.pem", public_key_path="keys/public.pem")
cache = Cache_Manager() 


# Make the managers available in the app context blueprint via config
app.config['CACHE_MANAGER'] = cache
app.config['JWT_MANAGER'] = jwt_manager
app.config['DB_MANAGER'] = db_manager

# Register blueprints 
app.register_blueprint(users_blueprint)
app.register_blueprint(products_blueprint)
app.register_blueprint(purchases_blueprint)

# Liveness endpoint to check if the service is running
@app.route("/liveness")
def liveness():
    return "<p>Hello, World!</p>"


# Readiness endpoint to check if the service is ready to handle requests
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
