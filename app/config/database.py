from flask_pymongo import PyMongo
import logging
from pymongo.errors import PyMongoError

mongo = PyMongo()

def init_db(app):
    try:
        mongo.init_app(app)
        logging.info("MongoDB initialized successfully.")
    except PyMongoError as e:
        logging.error(f"Failed to initialize MongoDB: {str(e)}")
        raise RuntimeError("MongoDB initialization failed") from e