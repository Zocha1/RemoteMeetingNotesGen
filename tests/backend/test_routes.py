import pytest

@pytest.fixture
def client(app):
    """Fixture to create a test client."""
    return app.test_client()

def test_plan_recording_success(client):
    """Test successful recording planning."""
    response = client.post('/plan-recording', json={"email": "test@example.com", "date": "2024-01-01"})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Recording scheduled successfully!'

def test_plan_recording_error(client):
    """Test error when email or date is missing."""
    response = client.post('/plan-recording', json={"email": ""})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Email and date are required'

def test_routes_rendering(client):
    """Test rendering of HTML pages."""
    endpoints = ['/', '/recording', '/notes']
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        # Check that the response contains valid HTML structure
        assert b"<!DOCTYPE html>" in response.data or b"<html>" in response.data

