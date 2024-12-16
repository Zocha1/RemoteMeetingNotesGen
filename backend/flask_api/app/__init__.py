from flask import Flask
from .models import db
import os

def create_app():
    app = Flask(__name__)

    # Configure upload folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    resources_dir = os.path.join(base_dir, 'resources')
    UPLOAD_FOLDER = os.path.join(resources_dir, 'screenshots')      

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Database created")

    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
