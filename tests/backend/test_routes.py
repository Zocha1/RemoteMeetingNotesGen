import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend/flask_api')))
import pytest
import json
from app import create_app
from app.models import *
from datetime import datetime

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
    # Dodawanie danych testowych do bazy
    with client.application.app_context():
        meeting = Meetings(title="Test Meeting", scheduled_time=datetime.now(), platform="Test Platform")
        transcription = Transcriptions(meeting_id=1, full_text="Test transcription", summary="Test summary", created_at=datetime.now())
        db.session.add(meeting)
        db.session.add(transcription)
        db.session.commit()

    response = client.get('/meeting-data')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    meeting = data[0]
    assert 'meeting_id' in meeting
    assert 'title' in meeting
    assert 'scheduled_time' in meeting
    assert 'platform' in meeting
    assert 'transcriptions' in meeting
    assert isinstance(meeting["transcriptions"], list)
    assert len(meeting["transcriptions"]) >0
    transcription = meeting["transcriptions"][0]
    assert 'transcription_id' in transcription
    assert 'full_text' in transcription
    assert 'summary' in transcription

def test_get_meeting_details_success(client):
    """Test successful retrieval of a specific meeting's details."""
     # Dodawanie danych testowych do bazy
    with client.application.app_context():
        meeting = Meetings(title="Test Meeting", scheduled_time=datetime.now(), platform="Test Platform")
        transcription = Transcriptions(meeting_id=meeting.meeting_id, full_text="Test transcription", summary="Test summary", created_at=datetime.now())
        db.session.add(meeting)
        db.session.add(transcription)
        db.session.commit()

        meeting_id = meeting.meeting_id
    
    response = client.get(f'/meeting-details/{meeting_id}')
    assert response.status_code == 200
    assert b"<title>Meeting Details</title>" in response.data
    assert b"Test Meeting" in response.data
    assert b"Test transcription" in response.data
    assert b"Test summary" in response.data

def test_routes_rendering(client):
    """Test rendering of HTML pages."""
    endpoints = ['/home', '/plan-meeting', '/notes']
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        # Check that the response contains valid HTML structure
        assert b"<!DOCTYPE html>" in response.data or b"<html>" in response.data

