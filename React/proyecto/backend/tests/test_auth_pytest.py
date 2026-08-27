
import json
from unittest.mock import MagicMock

class TestAuth:
    # Test suite for the authentication endpoints.

    def test_register_user_success(self, client, mocks):
        """Test successful user registration (201 Created)."""
        response = client.post(
            '/auth/register',
            data=json.dumps({'username': 'testuser', 'email': 'test@example.com', 'password': 'password123', 'role_id': 2}),
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.data.decode() == "User created successfully."
        mocks['user_repo'].add_user.assert_called_once()
    # Test user registration with missing fields (400 Bad Request).
    def test_register_user_missing_fields(self, client):
        response = client.post(
            '/auth/register',
            data=json.dumps({'username': 'testuser'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert "Missing required fields" in response.data.decode()
    # Test user registration when user already exists (409 Conflict).
    def test_register_user_conflict(self, client, mocks):
        
        mocks['user_repo'].add_user.side_effect = Exception("User already exists")
        
        response = client.post(
            '/auth/register',
            data=json.dumps({'username': 'testuser', 'email': 'test@example.com', 'password': 'password123', 'role_id': 2}),
            content_type='application/json'
        )
        assert response.status_code == 409
        assert "User could not be created" in response.data.decode()
    # Test successful user login (200 OK).
    def test_login_user_success(self, client, mocks):
        
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.role_name = 'customer'
        mocks['user_repo'].find_user_by_credentials.return_value = mock_user

        response = client.post('/auth/login',data=json.dumps({'username': 'testuser', 'password': 'password123'}), content_type='application/json')    
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'token' in data
    # Test login with invalid credentials (401 Unauthorized).
    def test_login_user_invalid_credentials(self, client, mocks):
        
        mocks['user_repo'].find_user_by_credentials.return_value = None

        response = client.post('/auth/login',data=json.dumps({'username': 'wronguser', 'password': 'wrongpassword'}), content_type='application/json')
        assert response.status_code == 401
        assert "Invalid credentials" in response.data.decode()
    # Test login with missing fields (400 Bad Request).
    def test_login_user_missing_fields(self, client):
        response = client.post('/auth/login',data=json.dumps({'username': 'testuser'}), content_type='application/json')
        assert response.status_code == 400
        assert "Missing username or password" in response.data.decode()
        assert response.status_code == 400
        assert "Missing username or password" in response.data.decode()