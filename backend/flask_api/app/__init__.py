from flask import Flask
from .models import db
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
    
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # Configure upload folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    resources_dir = os.path.join(base_dir, 'resources')    

    SCREENSHOT_UPLOAD_FOLDER = os.path.join(resources_dir, 'screenshots')
    if not os.path.exists(SCREENSHOT_UPLOAD_FOLDER):
        os.makedirs(SCREENSHOT_UPLOAD_FOLDER)
    app.config['SCREENSHOT_UPLOAD_FOLDER'] = SCREENSHOT_UPLOAD_FOLDER
    
    AUDIO_UPLOAD_FOLDER = os.path.join(resources_dir, 'audio')
    if not os.path.exists(AUDIO_UPLOAD_FOLDER):
        os.makedirs(AUDIO_UPLOAD_FOLDER)
    app.config['AUDIO_UPLOAD_FOLDER'] = AUDIO_UPLOAD_FOLDER

    FONTS_UPLOAD_FOLDER = os.path.join(resources_dir, 'fonts')
    if not os.path.exists(FONTS_UPLOAD_FOLDER):
        os.makedirs(FONTS_UPLOAD_FOLDER)
    app.config['FONTS_UPLOAD_FOLDER'] = FONTS_UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Database created")

    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app



