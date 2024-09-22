import logging
from datetime import datetime, timezone
from app.models.user import User

def get_all_users():
    try:
        logging.info("Fetching all users")
        return User.get_all_users()
    except Exception as e:
        logging.error("Failed to fetch users: %s", str(e))
        raise RuntimeError("Failed to fetch users") from e

def create_user(data):
    try:
        logging.info("Service creating user with data: %s", data)
        return User.create_user(data)
    except Exception as e:
        logging.error("Failed to create user: %s", str(e))
        raise RuntimeError("Failed to create user") from e
    
def update_user(data):
    try:
        logging.info("Updating user with data: %s", data)
        
        user_id = data.get("user_id")
        
        return User.update_user(user_id, data)
        
    except Exception as e:
        logging.error("Failed to update user: %s", str(e))
        raise RuntimeError("Failed to update user") from e