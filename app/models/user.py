import logging
from datetime import datetime, timezone
from bson.objectid import ObjectId
from app.config.database import mongo
from pymongo.errors import PyMongoError
from werkzeug.security import generate_password_hash

class User:
    @staticmethod
    def create_user(data):
        try: 
            logging.info("Creating a new user with data: %s", data)

            created_datetime = datetime.now(timezone.utc).isoformat()
            updated_datetime = datetime.now(timezone.utc).isoformat()

            user = {
                "first_name": data.get('first_name'),
                "middle_name": data.get('middle_name'),
                "last_name": data.get('last_name'),
                "password": generate_password_hash(data.get('password')),
                "phone": data.get('phone'),
                "session_token": data.get('session_token'), 
                "created_datetime": created_datetime,
                "updated_datetime": updated_datetime
            }

            logging.info("Inserting user: %s", user)
            
            return mongo.db.users.insert_one(user)
        except PyMongoError as e:
            logging.error("Error while inserting user: %s", str(e))
            raise RuntimeError("Database is not available")
    
        except Exception as e:
            logging.error("Error while inserting user: %s", str(e))
            raise RuntimeError("Failed to create user") from e 
        
    @staticmethod
    def get_all_users():
        try:
            users = mongo.db.users.find()
            all_users = []

            for user in users:

                user_data = {
                    "id": str(user["_id"]),
                    "first_name": user.get("first_name"),
                    "middle_name": user.get("middle_name", ''),
                    "last_name": user.get("last_name"),
                    "phone": user.get("phone"),
                    "session_token": user.get("session_token"),
                    "created_datetime": user.get("created_datetime"),
                    "updated_datetime": user.get("updated_datetime")
                }

                all_users.append(user_data)
                
            return all_users
        
        except PyMongoError as e:
            logging.error("Error while inserting user: %s", str(e))
            raise RuntimeError("Database is not available")
    
        except Exception as e:
            logging.error("Error while fetching users: %s", str(e))
            raise RuntimeError("Failed to fetch users") from e
        
    @staticmethod
    def update_user(user_id, data):
        try:
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            
            if not user:
                logging.error("User with id %s not found", user_id)
                return False
            
            update_data = {}

            if 'first_name' in data:
                update_data['first_name'] = data['first_name']

            if 'middle_name' in data:
                update_data['middle_name'] = data['middle_name']

            if 'last_name' in data:
                update_data['last_name'] = data['last_name']

            if 'phone' in data:
                update_data['phone'] = data['phone']

            if 'password' in data:
                update_data['password'] = generate_password_hash(data['password'])

            update_data['updated_datetime'] = datetime.utcnow().isoformat()

            if update_data:
                mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
                logging.info("User with id %s updated successfully", user_id)
                return True
            else:
                logging.info("No updates provided for user with id %s", user_id)
                return False
            
        except PyMongoError as e:
            logging.error("Database error while updating user: %s", str(e))
            raise RuntimeError("Database is not available") from e
        except Exception as e:
            logging.error("Error while updating user: %s", str(e))
            raise RuntimeError("Failed to update user") from e