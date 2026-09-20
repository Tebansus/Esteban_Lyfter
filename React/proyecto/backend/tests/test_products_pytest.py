
import json
from unittest.mock import MagicMock

# Helper class to simulate a SQLAlchemy Row object
class MockRow:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def _asdict(self):
        return self.__dict__

    
    def __iter__(self):
        return iter(self.__dict__.items())
# Test suite for the products endpoints.
class TestProducts:

    # Test creating a product as an admin (201 Created).
    def test_create_product_success_as_admin(self, client, mocks, admin_token):
        
        response = client.post('/api/products',headers={'Authorization': f'Bearer {admin_token}'}, data=json.dumps({'name': 'Dog Food', 'price': 25.50, 'stock_quantity': 100}),
                               content_type='application/json')       
        assert response.status_code == 201
        mocks['product_repo'].add_product.assert_called_once()
        mocks['cache_manager'].delete.assert_called_with("all_products")
    # test that a customer cannot create a product (403 Forbidden).
    def test_create_product_forbidden_as_customer(self, client, customer_token):
        
        response = client.post('/api/products',headers={'Authorization': f'Bearer {customer_token}'},data=json.dumps({'name': 'Dog Food', 'price': 25.50, 'stock_quantity': 100}),
            content_type='application/json')
        assert response.status_code == 403
        assert "does not have access" in response.data.decode()
    # Test getting all products when not in cache (200 OK).
    def test_get_all_products_uncached(self, client, mocks, customer_token):
        
        mocks['cache_manager'].get_json.return_value = None        
        mock_product = MockRow(id=1, name='Dog Leash', price=15.00, stock_quantity=50)
        mocks['product_repo'].list_products.return_value = [mock_product]

        response = client.get('/api/products', headers={'Authorization': f'Bearer {customer_token}'})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == 'Dog Leash'
        mocks['cache_manager'].set_json.assert_called_once()
    # Test getting all products when they are in cache (200 OK).
    def test_get_all_products_cached(self, client, mocks, customer_token):
        
        cached_data = [{'id': 1, 'name': 'Cached Product'}]
        mocks['cache_manager'].get_json.return_value = cached_data

        response = client.get('/api/products', headers={'Authorization': f'Bearer {customer_token}'})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data[0]['name'] == 'Cached Product'
        mocks['product_repo'].list_products.assert_not_called()
    # Test deleting a product as an admin (204 No Content).
    def test_delete_product_as_admin(self, client, mocks, admin_token):
        response = client.delete('/api/products/1', headers={'Authorization': f'Bearer {admin_token}'})
        assert response.status_code == 204
        mocks['product_repo'].delete_product.assert_called_with(1)
        mocks['cache_manager'].delete.assert_called_with("all_products", "product:1")