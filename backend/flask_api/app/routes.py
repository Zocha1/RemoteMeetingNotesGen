from flask import Blueprint, request, jsonify, current_app, render_template
import base64
from datetime import datetime
import os
from .models import *

# Define Blueprint
main_routes = Blueprint('main', __name__)

@main_routes.route('/upload-screenshot', methods=['POST'])
def upload_screenshot():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'Image data is missing'}), 400

    try:
        image_data = data['image'].split(",")[1]
        image_data = base64.b64decode(image_data)

        # Generate file path with timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f'screenshot_{timestamp}.png')

        # Save the image
        with open(file_path, 'wb') as f:
            f.write(image_data)

        return jsonify({'message': 'Screenshot saved successfully', 'file_path': file_path})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    

@main_routes.route('/')
def index():
    return render_template('base.html')

@main_routes.route('/recording')
def recording():
    return render_template('recording.html')

@main_routes.route('/notes')
def notes():
    return render_template('notes.html')