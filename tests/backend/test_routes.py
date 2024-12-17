import pytest

@pytest.fixture
def client(app):
    """Fixture to create a test client."""
    return app.test_client()

def test_add_meeting_success(client):
    """Test successful meeting addition without participants."""
    response = client.post('/add-meeting', json={
        "title": "Test Meeting",
        "scheduled_time": "2024-07-29T14:30:00",
        "platform": "Zoom"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert "meeting_id" in data
    assert data['participants_added'] == 0

def test_add_meeting_with_participants(client):
    """Test successful meeting addition with participants."""
    response = client.post('/add-meeting', json={
        "title": "Team Sync",
        "scheduled_time": "2024-07-29T15:00:00",
        "platform": "Teams",
        "participants": [
            {
                "firstname": "Jan",
                "lastname": "Kowalski",
                "email": "jan.kowalski@example.com"
            },
            {
                "firstname": "Anna",
                "lastname": "Nowak",
                "email": "anna.nowak@example.com"
            }
        ]
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == "Meeting and participants added successfully"
    assert "meeting_id" in data
    assert data['participants_added'] == 2

def test_add_meeting_missing_data(client):
    """Test error when required meeting data is missing."""
    response = client.post('/add-meeting', json={
        "scheduled_time": "2024-07-29T14:30:00",
        "platform": "Zoom"
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Title, scheduled_time, and platform are required'

def test_add_meeting_missing_participant_data(client):
    """Test error when participant data is incomplete."""
    response = client.post('/add-meeting', json={
        "title": "Meeting With Invalid Participant",
        "scheduled_time": "2024-07-29T16:00:00",
        "platform": "Zoom",
        "participants": [
            {
                "firstname": "John",
                "lastname": "Doe"
                # Missing email
            }
        ]
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == "Each participant must have firstname, lastname, and email"

def test_get_meetings_success(client):
    """Test successful retrieval of meetings."""
    response = client.get('/get-meetings')
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "meetings" in data
    assert isinstance(data['meetings'], list)


def test_routes_rendering(client):
    """Test rendering of HTML pages."""
    endpoints = ['/', '/recording', '/notes']
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        # Check that the response contains valid HTML structure
        assert b"<!DOCTYPE html>" in response.data or b"<html>" in response.data

