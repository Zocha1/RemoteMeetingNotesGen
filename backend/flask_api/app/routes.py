from flask import Blueprint, request, jsonify, current_app
import base64
from datetime import datetime
import os

# Define Blueprint
main_routes = Blueprint('main', __name__)

@main_routes.route('/upload', methods=['POST'])
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

@main_routes.route('/plan-recording', methods=['POST'])
def plan_recording():
    data = request.get_json()
    email = data.get('email')
    date = data.get('date')

    if not email or not date:
        return jsonify({'error': 'Email and date are required'}), 400

    # Example: Save the plan to a database or file (logic not implemented here)
    # schedule_recording(email, date)

    return jsonify({'message': 'Recording scheduled successfully!'})
