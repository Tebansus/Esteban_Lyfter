from flask import request, Response, current_app
from functools import wraps
# Decorator to check if the user is authenticated and has the required role
# This decorator will check the Authorization header for a Bearer token
# If the token is valid, it will allow access to the endpoint
# If the token is invalid or the user does not have the required role, it will return a 403 Forbidden response
def error(status):
    return Response(status=status)

def auth_required(allowed_roles=None):
    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            jwt_manager = current_app.config['JWT_MANAGER']
            auth = request.headers.get('Authorization', '')
            if not auth.startswith('Bearer '):
                return error(403)

            token = auth.replace('Bearer ', '')
            decoded = jwt_manager.decode(token)
            if decoded is None:
                return error(403)

            if allowed_roles and decoded.get('role') not in allowed_roles:
                return error(403)

            request.user = decoded
            return func(*args, **kwargs)
        return decorated_function
    return wrapper