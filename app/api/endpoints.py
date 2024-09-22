from pymongo.errors import PyMongoError
from werkzeug.exceptions import BadRequest
from flask import Blueprint, jsonify, request
from app.services.auth_service import check_authorization
from app.services.user_service import get_all_users, create_user, update_user


api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def list_users():
    try:
        users = get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"msg": "Internal server error", "error": str(e)}), 500

@api.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        required_fields = ['first_name', 'middle_name', 'last_name', 'password', 'phone', 'session_token']

        missing_fields = [field for field in required_fields if field not in data or not data.get(field)]

        if missing_fields:
            raise BadRequest(f"Invalid data. The following fields are required: {', '.join(missing_fields)}.")
        
        user = create_user(data)
        return jsonify({"Status": "success", "user_id": str(user.inserted_id)}), 201
    
    except BadRequest as e:
        return jsonify({"Status": "failure", "Reason": str(e)}), 400
    except PyMongoError as e:  
        return jsonify({"Status": "failure", "Reason": "Database is not available"}), 500
    except RuntimeError as e: 
        return jsonify({"Status": "failure", "Reason": str(e)}), 500
    except Exception as e:  
        return jsonify({"Status": "failure", "Reason": "Internal server error"}), 500
    
@api.route('/users', methods=['PUT'])
@check_authorization
def update_user_info():
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            raise BadRequest('Invalid data. "user_id" is required.')

        result = update_user(data)
        if result:
            return jsonify({"Status": "success"}), 200
        else:
            return jsonify({"Status": "failure", "Reason": "User not found"}), 404

    except BadRequest as e:
        return jsonify({"Status": "failure", "Reason": str(e)}), 400
    except PyMongoError as e: 
        return jsonify({"Status": "failure", "Reason": "Database is not available"}), 500
    except RuntimeError as e:
        return jsonify({"Status": "failure", "Reason": str(e)}), 500
    except Exception as e:
        return jsonify({"Status": "failure", "Reason": "Internal server error"}), 500