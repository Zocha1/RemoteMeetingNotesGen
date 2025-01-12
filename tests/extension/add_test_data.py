from backend.flask_api.app import create_app, models
from datetime import datetime

def add_test_data():
    app = create_app()
    with app.app_context():
        meeting = models.Meetings(title="Test Meeting for Cypress", scheduled_time=datetime.now(), platform="Test Platform")
        models.db.session.add(meeting)
        models.db.session.flush()
        transcription = models.Transcriptions(meeting_id=meeting.meeting_id, full_text="Test transcription for Cypress", summary="Test summary for Cypress", created_at=datetime.now())
        models.db.session.add(transcription)
        models.db.session.commit()

if __name__ == "__main__":
    add_test_data()