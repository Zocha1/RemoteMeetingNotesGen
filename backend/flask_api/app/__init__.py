from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    db.init_app(app)

    from . import models  
    app.register_blueprint(models.model)

    return app
