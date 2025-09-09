from flask import request, Response, current_app
from functools import wraps

def auth_required(allowed_roles=None):
    # Decorator to protect endpoints, requiring a valid JWT.
    # It can also check if the user has one of the allowed roles.
    # This was recycled from week 7 and 8
    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            jwt_manager = current_app.config['JWT_MANAGER']
            auth_header = request.headers.get('Authorization', '')

            if not auth_header.startswith('Bearer '):
                return Response(status=403, response="Missing or invalid token.")

            token = auth_header.replace('Bearer ', '')
            decoded_payload = jwt_manager.decode(token)            
            if decoded_payload is None:
                return Response(status=403, response="Invalid token.")        
            if allowed_roles:
                user_role = decoded_payload.get('role')
                if user_role not in allowed_roles:
                    return Response(status=403, response=f"Role '{user_role}' does not have access.")           
            request.user = decoded_payload
            return func(*args, **kwargs)
        return decorated_function
    return wrapper