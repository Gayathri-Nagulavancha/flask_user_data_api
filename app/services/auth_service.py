import logging
from functools import wraps
from flask import request, current_app

def check_authorization(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        session_token_header = request.headers.get('Session-Token')

        logging.info(f"Authorization Header: {auth_header}")
        logging.info(f"Session Token: {session_token_header}")

        if not auth_header or not session_token_header:
            return {"Status": "failure", "Reason": "Missing tokens"}, 403
        
        try:
            token_type, token = auth_header.split()
            if token_type != "Bearer" or token != current_app.config['AUTH_TOKEN']:
                return {"Status": "failure", "Reason": "Invalid Bearer token"}, 403

            if session_token_header != current_app.config['SESSION_TOKEN']:
                return {"Status": "failure", "Reason": "Invalid session token"}, 403
            
        except ValueError:
            return {"Status": "failure", "Reason": "Authorization header format is invalid"}, 403
        
        return f(*args, **kwargs)
    
    return decorated_function