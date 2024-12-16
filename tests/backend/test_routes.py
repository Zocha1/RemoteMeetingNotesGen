import pytest

@pytest.fixture
def client(app):
    """Fixture to create a test client."""
    return app.test_client()

def test_add_meeting_success(client):
    """Test successful meeting addition."""
    response = client.post('/add-meeting', json={
        "title": "Test Meeting",
        "scheduled_time": "2024-07-29T14:30:00",
        "platform": "Zoom"
    })
    assert response.status_code == 201

def test_add_meeting_missing_data(client):
    """Test error when required meeting data is missing."""
    response = client.post('/add-meeting', json={
       "scheduled_time": "2024-07-29T14:30:00",
        "platform": "Zoom"
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Title, scheduled_time, and platform are required'

def test_routes_rendering(client):
    """Test rendering of HTML pages."""
    endpoints = ['/', '/recording', '/notes']
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        # Check that the response contains valid HTML structure
        assert b"<!DOCTYPE html>" in response.data or b"<html>" in response.data

