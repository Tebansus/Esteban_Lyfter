import pytest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app as flask_app
from JWT_manager import JWT_Manager

# Use fixture method to create JWT Manager
# The fixture initializes the JWT Manager with the specified key paths
@pytest.fixture(scope='session')
def jwt_manager():
    
    return JWT_Manager(private_key_path="keys/private.pem", public_key_path="keys/public.pem")

@pytest.fixture
def app(jwt_manager):
    
    # Create mock objects for all repositories and managers
    mock_user_repo = MagicMock()
    mock_product_repo = MagicMock()
    mock_cart_repo = MagicMock()
    mock_sales_repo = MagicMock()
    mock_refund_repo = MagicMock()
    mock_cache_manager = MagicMock()

    # Configure the app for testing
    flask_app.config['TESTING'] = True

    # Use patch.dict to replace dependencies in the app's config
    with patch.dict(flask_app.config, {
        'USER_REPO': mock_user_repo,
        'PRODUCT_REPO': mock_product_repo,
        'CART_REPO': mock_cart_repo,
        'SALES_REPO': mock_sales_repo,
        'REFUND_REPO': mock_refund_repo,
        'CACHE_MANAGER': mock_cache_manager,
        'JWT_MANAGER': jwt_manager
    }):
        # Yield the app and the mocks so tests can access them
        yield flask_app, {
            'user_repo': mock_user_repo,
            'product_repo': mock_product_repo,
            'cart_repo': mock_cart_repo,
            'sales_repo': mock_sales_repo,
            'refund_repo': mock_refund_repo,
            'cache_manager': mock_cache_manager
        }

@pytest.fixture
def client(app):    
    # The app fixture returns a tuple, so only the app object is needed for the client
    app_instance, _ = app
    return app_instance.test_client()
# Fixture to provide easy access to the dictionary of mocks.
@pytest.fixture
def mocks(app):    
    # The app fixture returns a tuple, we need the second element (the mocks dict)
    _, mocks_dict = app
    return mocks_dict
# Admin token fixture to generate a JWT for an admin user.
@pytest.fixture
def admin_token(jwt_manager):
    
    return jwt_manager.encode({'id': 2, 'role': 'admin'})
# Customer token fixture to generate a JWT for a customer user.
@pytest.fixture
def customer_token(jwt_manager):
    """Fixture to generate a JWT for a customer user."""
    return jwt_manager.encode({'id': 1, 'role': 'customer'})