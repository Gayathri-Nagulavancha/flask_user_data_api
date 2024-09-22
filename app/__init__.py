import logging
from flask import Flask
from app.api.endpoints import api
from app.config.database import init_db
from app.config.config import DevelopmentConfig


def create_app():
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app.config.from_object(DevelopmentConfig)
    
    init_db(app)
    
    app.register_blueprint(api, url_prefix='/api')

    return app