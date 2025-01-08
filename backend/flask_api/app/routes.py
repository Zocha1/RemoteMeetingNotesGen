from flask import Blueprint, request, jsonify, current_app, render_template
import base64
from datetime import datetime
import os
from .models import *
from PIL import Image
import pytesseract
from pytesseract import Output

# Define Blueprint
main_routes = Blueprint('main', __name__)

@main_routes.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], audio_file.filename)
    audio_file.save(upload_path)

    return jsonify({'message': 'Audio file saved successfully', 'file_path': upload_path})

@main_routes.route('/add-meeting', methods=['POST'])
def add_meeting():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title = data.get('title')
    scheduled_time_str = data.get('scheduled_time')
    platform = data.get('platform')
    participants = data.get('participants', [])

    if not all([title, scheduled_time_str, platform]):
        return jsonify({'error': 'Title, scheduled_time, and platform are required'}), 400

    try:
        # Convert scheduled_time from string to datetime
        scheduled_time = datetime.fromisoformat(scheduled_time_str)
        # Create a new meeting
        new_meeting = Meetings(title=title, scheduled_time=scheduled_time, platform=platform)
        db.session.add(new_meeting)
        db.session.flush()  # flush to get the meeting_id

        for participant in participants:
            firstname = participant.get('firstname')
            lastname = participant.get('lastname')
            email = participant.get('email')

            if not all([firstname, lastname, email]):
                return jsonify({'error': 'Each participant must have firstname, lastname, and email'}), 400

            # check if user already exists
            user = Users.query.filter_by(email=email).first()
            if not user:
                user = Users(firstname=firstname, lastname=lastname, email=email)
                db.session.add(user)
                db.session.flush()  # get the user_id

            new_participant = Participants(
                meeting_id=new_meeting.meeting_id,
                user_id=user.user_id,
                role="Participant",  # default role
            )
            db.session.add(new_participant)

        db.session.commit()

        return jsonify({
            'message': 'Meeting and participants added successfully',
            'meeting_id': new_meeting.meeting_id,
            'participants_added': len(participants)
        }), 201
    
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS): {str(e)}'}), 400 # 400 Bad Request
    
    except Exception as e:
        db.session.rollback() # rollback if error
        return jsonify({'error': f'Error while creating meeting: {str(e)}'}), 500 # 500 Internal Server Error
    
@main_routes.route('/get-meetings', methods=['GET'])
def get_meetings():
    """Retrieve all meetings from the database along with participants."""
    try:
        meetings = Meetings.query.all()
        meetings_data = []

        for meeting in meetings:
            # Retrieve participants assigned to the given meeting
            participants = Participants.query.filter_by(meeting_id=meeting.meeting_id).all()
            participant_list = []

            for participant in participants:
                user = Users.query.get(participant.user_id)
                participant_list.append({
                    "user_id": user.user_id,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "email": user.email,
                    "role": participant.role
                })

            meetings_data.append({
                "meeting_id": meeting.meeting_id,
                "title": meeting.title,
                "scheduled_time": meeting.scheduled_time.isoformat(),
                "platform": meeting.platform,
                "participants": participant_list
            })

        return jsonify({
            "message": "Meetings retrieved successfully",
            "meetings": meetings_data
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error retrieving meetings: {str(e)}"}), 500


@main_routes.route('/upload-screenshot', methods=['POST'])
def upload_screenshot():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'Image data is missing'}), 400

    try:
    # 1) Dekodowanie base64 i zapis pliku
        image_data = data['image'].split(",")[1]
        image_data = base64.b64decode(image_data)

    # Generowanie nazwy pliku
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f'screenshot_{timestamp}.png')

        # Zapisywanie na dysku
        with open(file_path, 'wb') as f:
            f.write(image_data)

        # 2) Dodanie do bazy - tabela 'Screenshots'
        new_screenshot = Screenshots(
            meeting_id=None,  # Wstaw tutaj właściwe ID spotkania, jeśli to ma być powiązane
            image_path=file_path,
            timestamp=datetime.now()
        )
        db.session.add(new_screenshot)
        # flush() aby mieć screenshot_id
        db.session.flush()

        # 3) Przetwarzanie OCR (pytesseract)
        img = Image.open(file_path)

        # Proste odczytanie tekstu:
        recognized_text = pytesseract.image_to_string(img, lang='eng')

        # Wyliczenie średniego confidence:
        ocr_data = pytesseract.image_to_data(img, lang='eng', output_type=Output.DICT)
        confidences = [c for c in ocr_data['conf'] if c >= 0]
        average_conf = sum(confidences) / len(confidences) if len(confidences) > 0 else 0.0

        # 4) Dodanie wpisu w tabeli 'OCR'
        ocr_result = OCR(
            screenshot_id=new_screenshot.screenshot_id,
            text=recognized_text,
            confidence=average_conf
        )
        db.session.add(ocr_result)

        # 5) Commit zmian w bazie
        db.session.commit()

        # 6) Odpowiedź do wtyczki
        return jsonify({
            'message': 'Screenshot saved and OCR processed successfully',
            'file_path': file_path,
            'recognized_text': recognized_text,
            'confidence': average_conf
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main_routes.route('/')
def index():
    return render_template('base.html')

@main_routes.route('/recording')
def recording():
    return render_template('recording.html')

@main_routes.route('/notes')
def notes():
    return render_template('notes.html')

@main_routes.route('/plan-meeting')
def plan_meeting():
    return render_template('calendar.html')