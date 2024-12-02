from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure upload folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    resources_dir = os.path.join(base_dir, 'resources')
    UPLOAD_FOLDER = os.path.join(resources_dir, 'screenshots')      
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # db.init_app(app)

    # Register blueprints
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
