
import json
from unittest.mock import MagicMock
from decimal import Decimal

class TestSales:
    # Test suite for the sales, cart, and refund endpoints.
    # Test successful addition of an item to the cart (201 Created).
    def test_add_to_cart_success(self, client, mocks, customer_token):        
        mock_product = MagicMock()
        mock_product.stock = 10
        mocks['product_repo'].get_product_by_id.return_value = mock_product
        mock_cart = MagicMock()
        mock_cart.id = 1
        mocks['cart_repo'].get_active_cart_by_user.return_value = mock_cart
        response = client.post('/api/cart/items', headers={'Authorization': f'Bearer {customer_token}'}, data=json.dumps({'product_id': 1, 'quantity': 2}), content_type='application/json')
        assert response.status_code == 201
        mocks['cart_repo'].add_item_to_cart.assert_called_with(1, 1, 2)
    # test adding an item with insufficient stock (409 Conflict).
    def test_add_to_cart_insufficient_stock(self, client, mocks, customer_token):       
        mock_product = MagicMock()
        mock_product.stock = 1
        mocks['product_repo'].get_product_by_id.return_value = mock_product
        response = client.post('/api/cart/items', headers={'Authorization': f'Bearer {customer_token}'}, data=json.dumps({'product_id': 1, 'quantity': 5}), content_type='application/json')
        
        assert response.status_code == 409
        assert "insufficient stock" in response.data.decode()
    # test a successful checkout process (200 OK).
    def test_checkout_success(self, client, mocks, customer_token):       
        mock_cart = MagicMock()
        mock_cart.id = 1
        mocks['cart_repo'].get_active_cart_by_user.return_value = mock_cart

        mock_product = MagicMock()
        mock_product.stock = 20
        mock_product.precio = Decimal('10.00')
        mock_product.nombre = "Test Product"
        mocks['product_repo'].get_product_by_id.return_value = mock_product
        
        mocks['sales_repo'].add_address.return_value = 1
        mocks['sales_repo'].create_invoice.return_value = 101

        payload = {
            'shipping_address': 'Calle 123',
            'buyer_name': 'Test',
            'buyer_email': 'test@test.com',
            'items': [{'product_id': 1, 'quantity': 2, 'price': '10.00'}]
        }
        response = client.post('/api/checkout', headers={'Authorization': f'Bearer {customer_token}'}, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['invoice_id'] == 101
        assert data['total_price'] == '20.00'
        # Mock assertions
        mocks['product_repo'].adjust_stock.assert_called_with(1, quantity_delta=-2)
        mocks['cart_repo'].update_cart_status.assert_called_with(1, 'completed')
    # test processing a refund as an admin (201 Created).
    def test_process_refund_as_admin(self, client, mocks, admin_token):
        
        response = client.post('/api/refunds',headers={'Authorization': f'Bearer {admin_token}'},
            data=json.dumps({'invoice_id': 101,'product_id': 1,'quantity': 1,'reason': 'test'}),           
            content_type='application/json'
        )
        assert response.status_code == 201
        mocks['product_repo'].adjust_stock.assert_called_with(product_id=1, quantity_delta=1)