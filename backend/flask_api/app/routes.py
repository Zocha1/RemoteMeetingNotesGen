from flask import Blueprint, request, jsonify, current_app, render_template, send_file
import base64
from datetime import datetime, timedelta
import time
import os
from io import StringIO, BytesIO
from .models import *
import requests
#from xhtml2pdf import pisa
from .audio_processing import process_audio_to_text
from .email_service import send_meeting_notes_email
from .image_processing import detect_whiteboard, crop_and_save_whiteboard
from .active_meeting import find_active_meeting
import easyocr
# import pdfkit
import tempfile
# imports for generating pdf files
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Image
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage 

# Define Blueprint
main_routes = Blueprint('main', __name__)

# def find_active_meeting():
#     current_time = datetime.now()
#     tolerance = timedelta(minutes=10) # set the tolerance to 60 minutes

#     active_meeting = None
#     meetings = Meetings.query.all()
#     for meeting in meetings:
#         if meeting.scheduled_time and current_time - meeting.scheduled_time <= tolerance and current_time >= meeting.scheduled_time:
#             active_meeting = meeting
#             break

#     if active_meeting == None:
#         last_meeting = Meetings.query.order_by(Meetings.meeting_id.desc()).first()
#         if last_meeting:
#             #meeting_id = str(last_meeting.meeting_id)
#             return last_meeting
#         else:
#            return None
#     return active_meeting

@main_routes.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['file']

    try:
        active_meeting = find_active_meeting()
        #last_meeting = Meetings.query.order_by(Meetings.meeting_id.desc()).first()
        if active_meeting:
            meeting_id = str(active_meeting.meeting_id)
        else:
           return jsonify({'error': 'No meeting found in database'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to fetch last meeting ID: {str(e)}'}), 500

    audio_upload_folder = current_app.config['AUDIO_UPLOAD_FOLDER']
    meeting_folder = os.path.join(audio_upload_folder, meeting_id)
    os.makedirs(meeting_folder, exist_ok=True) 

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f"audio_{timestamp}{os.path.splitext(audio_file.filename)[1]}"
    upload_path = os.path.join(meeting_folder, file_name)

    # upload_path = os.path.join(meeting_folder, audio_file.filename)
    
    try:
        audio_file.save(upload_path)
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
    
    try:
        transcribed_text = process_audio_to_text(upload_path)
        print(f"Transcribed text: {transcribed_text}")
    except Exception as e:
        return jsonify({'error': f'Failed to process audio: {str(e)}'}), 500


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
    
@main_routes.route('/meeting-data', methods=['GET'])
def get_meeting_data():
    """
    Pobiera dane ze spotkań oraz transkrypcji i zwraca je w JSON.
    """
    try:
        # Pobierz wszystkie spotkania z bazy danych
        meetings = Meetings.query.all()
        # Pobierz transkrypcje z bazy danych
        transcriptions = Transcriptions.query.all()
    except Exception as e:
        return jsonify({'error': f'Failed to fetch data: {str(e)}'}), 500
    
    meeting_data = []
    for meeting in meetings:
        # Filtruj transkrypcje dla konkretnego spotkania
      filtered_transcriptions = [t for t in transcriptions if t.meeting_id == meeting.meeting_id]
      
      # Stwórz słownik danych dla każdego spotkania
      meeting_entry = {
          'meeting_id': meeting.meeting_id,
          'title': meeting.title,
          'scheduled_time': meeting.scheduled_time.isoformat() if meeting.scheduled_time else None,
          'platform': meeting.platform,
          'transcriptions': [
             {
                 'transcription_id': t.transcription_id,
                 'full_text': t.full_text,
                 'summary': t.summary
             }
             for t in filtered_transcriptions]
      }
      meeting_data.append(meeting_entry)
    
    return jsonify(meeting_data)

@main_routes.route('/meeting-details/<int:meeting_id>', methods=['GET'])
def get_meeting_details(meeting_id):
    """
    Pobiera dane konkretnego spotkania i jego transkrypcję z bazy danych
    i renderuje je w szablonie meeting_details.html.
    """
    try:
        # Pobierz spotkanie z bazy danych
        meeting = Meetings.query.filter_by(meeting_id=meeting_id).first_or_404()
        # Pobierz transkrypcje do tego spotkania
        transcription = Transcriptions.query.filter_by(meeting_id=meeting_id).first()

        if not transcription:
           return render_template("meeting_details.html", meeting=meeting, transcription=None)
           
        return render_template("meeting_details.html", meeting=meeting, transcription=transcription)

    except Exception as e:
        return jsonify({'error': f'Failed to fetch meeting data: {str(e)}'}), 500

# @main_routes.route('/get-meetings', methods=['GET'])
# def get_meetings():
#     """Retrieve all meetings from the database along with participants."""
#     try:
#         meetings = Meetings.query.all()
#         meetings_data = []

#         for meeting in meetings:
#             # Retrieve participants assigned to the given meeting
#             participants = Participants.query.filter_by(meeting_id=meeting.meeting_id).all()
#             participant_list = []

#             for participant in participants:
#                 user = Users.query.get(participant.user_id)
#                 participant_list.append({
#                     "user_id": user.user_id,
#                     "firstname": user.firstname,
#                     "lastname": user.lastname,
#                     "email": user.email,
#                     "role": participant.role
#                 })

#             meetings_data.append({
#                 "meeting_id": meeting.meeting_id,
#                 "title": meeting.title,
#                 "scheduled_time": meeting.scheduled_time.isoformat(),
#                 "platform": meeting.platform,
#                 "participants": participant_list
#             })

#         return jsonify({
#             "message": "Meetings retrieved successfully",
#             "meetings": meetings_data
#         }), 200

#     except Exception as e:
#         return jsonify({"error": f"Error retrieving meetings: {str(e)}"}), 500


@main_routes.route('/upload-screenshot', methods=['POST'])
def upload_screenshot():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'Image data is missing'}), 400

    try:
        image_data = data['image'].split(",")[1]
        image_data = base64.b64decode(image_data)

        #last_meeting = Meetings.query.order_by(Meetings.meeting_id.desc()).first()
        last_meeting = find_active_meeting()
        if not last_meeting:
            return jsonify({'error': 'No meeting found in database'}), 404

        screenshot_upload_folder = current_app.config['SCREENSHOT_UPLOAD_FOLDER']
        meeting_folder = os.path.join(screenshot_upload_folder, str(last_meeting.meeting_id))
        os.makedirs(meeting_folder, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_path = os.path.join(meeting_folder, f'screenshot_{timestamp}.png')

        with open(file_path, 'wb') as f:
            f.write(image_data)

        reader = easyocr.Reader(['en', 'pl'])
        contours = detect_whiteboard(file_path)
        if contours:
            cropped_path = os.path.join(meeting_folder, 'whiteboards')
            os.makedirs(cropped_path, exist_ok=True)
            crop_and_save_whiteboard(file_path, cropped_path, contours, timestamp)

            for i, file in enumerate(os.listdir(cropped_path)):
                cropped_img_path = os.path.join(cropped_path, file)
                ocr_results = reader.readtext(cropped_img_path, detail=0)

                cropped_screenshot = Screenshots(
                    meeting_id=last_meeting.meeting_id,
                    image_path=cropped_img_path,
                    timestamp=datetime.now()
                )
                db.session.add(cropped_screenshot)
                db.session.flush()

                ocr_result = OCR(
                    screenshot_id=cropped_screenshot.screenshot_id,
                    text="\n".join(ocr_results) if ocr_results else "No text recognized"
                )
                db.session.add(ocr_result)

        else:
            ocr_results = reader.readtext(file_path, detail=0)

            new_screenshot = Screenshots(
                meeting_id=last_meeting.meeting_id,
                image_path=file_path,
                timestamp=datetime.now()
            )
            db.session.add(new_screenshot)
            db.session.flush()

            ocr_result = OCR(
                screenshot_id=new_screenshot.screenshot_id,
                text="\n".join(ocr_results) if ocr_results else "No text recognized"
            )
            db.session.add(ocr_result)

        db.session.commit()
        return jsonify({'message': 'Screenshot and OCR processed successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def parse_emails(emails_str):
    """Parsuje string z emailem, zwraca listę stringow."""
    if emails_str is None:
        return []
    return [email.strip() for email in emails_str.split(',')]

@main_routes.route('/send-notes-email/<int:meeting_id>', methods=['POST'])
def send_notes_email_endpoint(meeting_id):
    """
      Pobiera transkrypcję, podsumowanie, ocr z bazy danych i wysyła je mailem.
    """
    try:
       # Pobierz spotkanie z bazy danych
        meeting = Meetings.query.filter_by(meeting_id=meeting_id).first_or_404()
        # Pobierz transkrypcje do tego spotkania
        transcription = Transcriptions.query.filter_by(meeting_id=meeting_id).first()
        
         # Pobierz dane do maila, i wyślij wiadomość
        if transcription:
           ##emails = [Users.query.filter_by(user_id = participant.user_id).first().email for participant in participants]
           # emails = ["pawelrus.637@gmail.com"]
            emails_str = os.getenv('EMAILS_TO_SEND')
            emails = parse_emails(emails_str)
            screenshots = Screenshots.query.filter_by(meeting_id=meeting_id).all()
            ocr_texts = []
            for screenshot in screenshots:
                ocr_result = OCR.query.filter_by(screenshot_id=screenshot.screenshot_id).first()
                if ocr_result:
                   ocr_texts.append(f"<p><strong>Screenshot {screenshot.screenshot_id} text:</strong> {ocr_result.text}  </p>")
            print(f"OCR texts: {ocr_texts}")

            send_meeting_notes_email(emails, meeting.title, transcription.full_text, transcription.summary, ocr_texts)
            return jsonify({'message': 'Email sent successfully'}), 200
        else:
            return jsonify({'error': f'No transription found'}), 404
    except Exception as e:
       return jsonify({'error': f'Failed to fetch meeting data: {str(e)}'}), 500


          
@main_routes.route('/download-meeting-data/<string:output_format>/<int:meeting_id>', methods=['GET'])
def download_meeting_data_md(output_format, meeting_id):
    """Pobiera dane konkretnego spotkania i jego transkrypcję i zwraca w pliku .txt, .md, .html lub .pdf."""
    try:
        # Pobierz spotkanie z bazy danych
        meeting = Meetings.query.filter_by(meeting_id=meeting_id).first_or_404()
        # Pobierz transkrypcje do tego spotkania
        transcription = Transcriptions.query.filter_by(meeting_id=meeting_id).first()
        # Pobierz screenshoty z bazy danych
        screenshots = Screenshots.query.filter_by(meeting_id=meeting_id).all()

        ocr_texts = []

        if output_format == 'md':
            text_output = f"## Meeting ID: {meeting.meeting_id}\n"
            text_output += f"## Title: {meeting.title}\n"
            text_output += f"## Scheduled Time: {meeting.scheduled_time}\n"
            text_output += f"## Platform: {meeting.platform}\n\n"
            
            if transcription:
                text_output += f"## Transcription:\n{transcription.full_text}\n\n"
                text_output += f"## Summary:\n{transcription.summary}\n\n"
                # Add OCR data
                for screenshot in screenshots:
                    ocr_result = OCR.query.filter_by(screenshot_id=screenshot.screenshot_id).first()
                    if ocr_result:
                        formatted_timestamp = screenshot.timestamp.strftime('%Y-%m-%d %H:%M')
                        ocr_texts.append(f"### Screenshot {formatted_timestamp} text: \n{ocr_result.text}\n")

                text_output += f"## OCR Results:\n{os.linesep.join(ocr_texts)}\n"
            else:
                text_output += "## No Transcription data available\n"
            # Generowanie pliku markdown
            output = StringIO()
            output.write(text_output)
            mem = BytesIO()
            mem.write(output.getvalue().encode('utf-8'))
            mem.seek(0)
    
            return send_file(
                mem,
            as_attachment=True,
                download_name=f"meeting_{meeting_id}_data.md",
                mimetype='text/markdown'
            )
        elif output_format == 'txt':
            text_output = f"Meeting ID: {meeting.meeting_id}\n"
            text_output += f"Title: {meeting.title}\n"
            text_output += f"Scheduled Time: {meeting.scheduled_time}\n"
            text_output += f"Platform: {meeting.platform}\n\n"
        
            if transcription:
                text_output += f"Transcription:\n{transcription.full_text}\n\n"
                text_output += f"Summary:\n{transcription.summary}\n\n"
                # Add OCR data
                for screenshot in screenshots:
                    ocr_result = OCR.query.filter_by(screenshot_id=screenshot.screenshot_id).first()
                    if ocr_result:
                        formatted_timestamp = screenshot.timestamp.strftime('%Y-%m-%d %H:%M')
                        ocr_texts.append(f"Screenshot {formatted_timestamp} text:\n {ocr_result.text}\n")

                text_output += f"OCR Results:\n{os.linesep.join(ocr_texts)}\n"
            else:
                text_output += "No Transcription data available\n"


            # Generowanie pliku tekstowego
            output = StringIO()
            output.write(text_output)
            mem = BytesIO()
            mem.write(output.getvalue().encode('utf-8'))
            mem.seek(0)
    
            return send_file(
                mem,
            as_attachment=True,
                download_name=f"meeting_{meeting_id}_data.txt",
                mimetype='text/plain'
            )
        elif output_format == 'html':# or output_format == 'pdf':
            styles = """
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        padding: 20px;
                        background-color: #f4f4f9;
                        color: #333;
                    }
                    h2 {
                        color: #0056b3;
                        border-bottom: 2px solid #0056b3;
                        padding-bottom: 5px;
                    }
                    p {
                        line-height: 1.6;
                    }
                    .highlight {
                        background-color: #dff0d8;
                        padding: 5px;
                        border-left: 4px solid #3c763d;
                    }
                </style>
                """
            text_output = "<html><head>"
            text_output += styles
            text_output += "</head><body>"
            text_output += f"<h2>Meeting ID: {meeting.meeting_id}</h2>"
            text_output += f"<h2>Title: {meeting.title}</h2>"
            text_output += f"<h2>Scheduled Time: {meeting.scheduled_time}</h2>"
            text_output += f"<h2>Platform: {meeting.platform}</h2>"
        
            if transcription:
                text_output += f"<h2>Transcription:</h2><p>{transcription.full_text}</p>"
                text_output += f"<h2>Summary:</h2><p>{transcription.summary}</p>"
                # Add OCR data
                text_output += f"<h2>OCR Results:</h2><br>"
                for screenshot in screenshots:
                    ocr_result = OCR.query.filter_by(screenshot_id=screenshot.screenshot_id).first()
                    if ocr_result:
                        formatted_timestamp = screenshot.timestamp.strftime('%Y-%m-%d %H:%M')
                        text_output += f'<img src="{screenshot.image_path}" alt="Screenshot {formatted_timestamp}" width="750">'
                        text_output += f"<p><strong>Screenshot {formatted_timestamp} text:</strong> {ocr_result.text}  </p><br>"
                
            else:
                text_output += "<h2>No Transcription data available</h2>"
            text_output += "</body></html>"
            
            
            output = StringIO()
            output.write(text_output)
            mem = BytesIO()
            mem.write(output.getvalue().encode('utf-8'))
            mem.seek(0)

            return send_file(
                mem,
                as_attachment=True,
                download_name=f"meeting_{meeting_id}_data.html",
                mimetype='text/html'
            )

        elif output_format == 'pdf':
            
            font_path =  current_app.config['FONTS_UPLOAD_FOLDER'] + "/DejaVuSans.ttf"
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
            font_path_bold = current_app.config['FONTS_UPLOAD_FOLDER'] + "/DejaVuSans-Bold.ttf"
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path_bold))

            mem = BytesIO()
            doc = SimpleDocTemplate(mem, pagesize=letter, author="Remote Meeting Notes Generator", title=f"Meeting {meeting.title} Notes", subject=f"Notes from {meeting.title} meeting")
            styles = getSampleStyleSheet()
             # Ustawienia stylu do poprawnego wyświetlania polskich znaków
            style_h2 = ParagraphStyle(
                 name='CustomH2',
                 parent=styles['h2'],
                 fontName='DejaVuSans-Bold',
            )
            style_normal = ParagraphStyle(
                name='CustomNormal',
                parent=styles['Normal'],
                fontName='DejaVuSans',
            )
            story = []
            story.append(Paragraph(f"<b>Meeting ID:</b> {meeting.meeting_id}", style_h2))
            story.append(Paragraph(f"<b>Title:</b> {meeting.title}", style_h2))
            story.append(Paragraph(f"<b>Scheduled Time:</b> {meeting.scheduled_time}", style_h2))
            story.append(Paragraph(f"<b>Platform:</b> {meeting.platform}", style_h2))
            if transcription:
                story.append(Paragraph(f"<b>Transcription:</b>", style_h2))
                story.append(Paragraph(transcription.full_text, style_normal))
                story.append(Paragraph(f"<b>Summary:</b>", style_h2))
                story.append(Paragraph(transcription.summary, style_normal))

                if screenshots:
                    story.append(Paragraph(f"<b>OCR Results:</b>", style_h2))
                    for screenshot in screenshots:
                         ocr_result = OCR.query.filter_by(screenshot_id=screenshot.screenshot_id).first()
                         if ocr_result:
                                try:
                                    pil_image = PILImage.open(screenshot.image_path)
                                    # img = Image(screenshot.image_path)
                                    img_width, img_height = pil_image.size
                                    max_width = 5.5*inch
                                    max_height = 5.5*inch
                                    scale_factor = min(max_width/img_width, max_height/img_height)
                                    img = Image(screenshot.image_path, width=img_width * scale_factor, height = img_height * scale_factor)  
                                    story.append(img)
                                except Exception as e:
                                    print(f"Failed to add image to PDF: {str(e)}")
                                formatted_timestamp = screenshot.timestamp.strftime('%Y-%m-%d %H:%M')
                                story.append(Paragraph(f"<b>Screenshot {formatted_timestamp} text:</b>", styles['h4']))
                                story.append(Paragraph(ocr_result.text, style_normal))
                                style_spaceAfter = ParagraphStyle(
                                    name='space',
                                    parent = style_normal,
                                    spaceAfter = 0.2*inch
                                )
                                story.append(Paragraph(" ", style_spaceAfter))
                                                
            else:
               story.append(Paragraph("<b>No Transcription data available</b>", styles['h2']))

            doc.build(story)
            mem.seek(0)
            return send_file(
                mem,
                as_attachment=True,
                download_name=f"meeting_{meeting_id}_data.pdf",
                mimetype='application/pdf'
            )
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch data and generate {output_format} file: {str(e)}'}), 500

@main_routes.route('/')
def index():
    return render_template('base.html')

@main_routes.route('/authorization.html')
def success():
    return render_template('authorization.html')

@main_routes.route('/home')
def home():
    return render_template('home.html')

@main_routes.route('/recording')
def recording():
    return render_template('recording.html')

@main_routes.route('/notes')
def notes():
    return render_template('notes.html')

@main_routes.route('/plan-meeting')
def plan_meeting():
    return render_template('calendar.html')

#SYNCHRONIZACJA Z GOOGLE CALENDAR

credentials_path = "instance/client_secret.json"

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from flask import session, redirect, request, url_for

@main_routes.route('/authorize-google', methods=['GET'])
def authorize_google():

    flow = Flow.from_client_secrets_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri="http://localhost:5000/oauth2callback"
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)



from google.oauth2.credentials import Credentials

@main_routes.route('/oauth2callback', methods=['GET'])
def oauth2callback():

    state = session['state']
    if not os.path.exists(credentials_path):
        print(f"Błąd: Plik {credentials_path} nie istnieje!")
    else:
        print(f"Plik {credentials_path} został poprawnie znaleziony.")

    flow = Flow.from_client_secrets_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/calendar'],
        state=state,
        redirect_uri="http://localhost:5000/oauth2callback"
    )
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    succesfull_link = "http://localhost:5000/authorization.html"
    return redirect(succesfull_link)


@main_routes.route('/sync-google-calendar', methods=['POST'])
def sync_google_calendar():
    # Check if credentials exist in session
    if 'credentials' not in session:
        return jsonify({'error': 'Google Calendar not authorized'}), 401

    credentials = Credentials(**session['credentials'])
    service = build('calendar', 'v3', credentials=credentials)

    # Get meeting details from request
    data = request.get_json()
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    title = data.get('title')

    # Ensure times are valid
    if not start_time or not end_time:
        return jsonify({'error': 'Start time and end time are required'}), 400

    if start_time >= end_time:
        return jsonify({'error': 'End time must be after start time'}), 400

    event = {
        'summary': title or "No Title",
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
        'attendees': [{'email': email} for email in data.get('attendees', [])]
    }

    try:
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return jsonify({'message': 'Event created successfully', 'event_id': created_event['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#ZOOM

@main_routes.route('/zoom/authorize', methods=['GET'])
def zoom_authorize():
    client_id = os.getenv('ZOOM_CLIENT_ID')
    redirect_uri = "http://localhost:5000/zoom/oauth2callback"
    authorization_url = f"https://zoom.us/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    return redirect(authorization_url)


import base64

@main_routes.route('/zoom/oauth2callback', methods=['GET'])
def zoom_callback():
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'Authorization code not found'}), 400

    # Exchange code for access token
    token_url = "https://zoom.us/oauth/token"
    client_id = os.getenv('ZOOM_CLIENT_ID')
    client_secret = os.getenv('ZOOM_CLIENT_SECRET')
    redirect_uri = "http://localhost:5000/zoom/oauth2callback"

    # Properly encode client_id and client_secret
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        session['zoom_access_token'] = tokens['access_token']
        succesfull_link = "http://localhost:5000/authorization.html"
        return redirect(succesfull_link)


@main_routes.route('/zoom/create-meeting', methods=['POST'])
def create_zoom_meeting():
    if 'zoom_access_token' not in session:
        return jsonify({'error': 'User not authorized with Zoom'}), 401

    access_token = session['zoom_access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    meeting_data = {
        "topic": "Test Meeting",
        "type": 2,
        "start_time": "2025-01-10T15:00:00Z",
        "duration": 30,
        "timezone": "UTC"
    }
  
    response = requests.post("https://api.zoom.us/v2/users/me/meetings", headers=headers, json=meeting_data)
    if response.status_code == 201:
        return jsonify(response.json())
    else:
        return jsonify({'error': response.json()}), response.status_code
       
    

@main_routes.route('/zoom/sync-meeting', methods=['POST'])
def zoom_sync_meeting():
    
    if 'zoom_access_token' not in session:
        return jsonify({'error': 'User not authorized with Zoom'}), 401
    # Retrieve meeting details from request
    data = request.get_json()
    title = data.get('title', 'New Meeting')
    start_time = data.get('start_time')  # Example: '2025-01-10T15:00:00Z'
    end_time = data.get('end_time')  # Example: '2025-01-10T15:30:00Z'
    duration = data.get('duration', 30)  # Optional: Duration in minutes

    if not start_time or not end_time:
        return jsonify({'error': 'Start time and end time are required'}), 400

    # Calculate meeting duration if not provided
    if not duration:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
        duration = int((end_dt - start_dt).total_seconds() / 60)

    access_token = session['zoom_access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    meeting_data = {
        "topic": title,
        "type": 2,  # Scheduled meeting
        "start_time": start_time,
        "duration": duration,
        "timezone": "UTC",
        "settings": {
            "join_before_host": True,
            "mute_upon_entry": True,
            "waiting_room": True,
        }
    }

    # Create meeting via Zoom API
    print("Headers:", headers)
    print("Meeting Data:", meeting_data)

    response = requests.post("https://api.zoom.us/v2/users/me/meetings", headers=headers, json=meeting_data)
    print("Zoom Response Status Code:", response.status_code)
    print("Zoom Response Content:", response.json())


    if response.status_code == 201:
        zoom_meeting = response.json()
        # Save Zoom meeting details to the database
        new_meeting = Meetings(
            title=zoom_meeting['topic'],
            scheduled_time=datetime.fromisoformat(start_time),
            platform="Zoom"
        )
        db.session.add(new_meeting)
        db.session.commit()

        return jsonify({
            'message': 'Meeting synchronized with Zoom successfully',
            'zoom_meeting': zoom_meeting,
            'local_meeting_id': new_meeting.meeting_id
        }), 201
    else:
        return jsonify({'error': response.json()}), response.status_code