import sys
import os
import pytest

# Add `backend/flask_api` to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend/flask_api')))

from app import create_app  # Import your Flask app creation function
from database.db import init_db  # Import database initialization 

@pytest.fixture
def app():
    """Fixture to set up the Flask application for testing."""
    app = create_app() 
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'  # Set a temp folder for uploads
    yield app

@pytest.fixture
def client(app):
    """Fixture to create a test client for the Flask app."""
    return app.test_client()
