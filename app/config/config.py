import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mydatabase')
    AUTH_TOKEN = os.getenv('AUTH_TOKEN', 'default_auth_token')
    SESSION_TOKEN = os.getenv('SESSION_TOKEN', 'default_session_token')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    MONGO_URI = os.getenv('TEST_MONGO_URI', 'mongodb://localhost:27017/test_database')