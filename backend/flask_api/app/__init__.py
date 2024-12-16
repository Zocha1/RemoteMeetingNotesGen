from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database.db import engine, init_db

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
    
    app.config['DB_ENGINE'] = engine

    if not os.path.exists('mydb.db'):
        init_db()
        print("Database initialized!")

    # Register blueprints
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
