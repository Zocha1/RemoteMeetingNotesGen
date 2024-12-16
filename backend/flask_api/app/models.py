from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import re

db = SQLAlchemy()

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

class Users(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, firstname, lastname, email):
        if not is_valid_email(email):
            raise ValueError(f"Invalid email address: {email}")
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        
    def __repr__(self):
        return f"{self.user_id}, {self.firstname} {self.lastname}, {self.email}"
    
class Meetings(db.Model):
    __tablename__ = "meetings"
    
    meeting_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    scheduled_time = db.Column(db.DateTime)
    platform = db.Column(db.String(50))
    
    def __init__(self, title, scheduled_time, platform):
        self.title = title
        self.scheduled_time = scheduled_time
        self.platform = platform
    
    def __repr__(self):
        return f"({self.meeting_id}), Title: {self.title}, Scheduled time: {self.scheduled_time}, Platform: {self.platform}"
    

class Participants(db.Model):
    __tablename__ = "participants"
    
    participant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.meeting_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    role = db.Column(db.String(50))
    joined_at = db.Column(db.DateTime)
    
    def __init__(self, meeting_id, user_id, role, joined_at):
        self.meeting_id = meeting_id
        self.user_id = user_id
        self.role = role
        self. joined_at = joined_at
    
    def __repr__(self):
        return f"({self.participant_id}), Meeting ID: {self.meeting_id}, User ID: {self.user_id}, Role: {self.role}, Joined at: {self.joined_at}"
    
    
class Transcriptions(db.Model):
    __tablename__ = "transcriptions"
    
    transcription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.meeting_id'))
    full_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, meeting_id, full_text, created_at):
        self.meeting_id = meeting_id
        self.full_text = full_text
        self.created_at = created_at
    
    def __repr__(self):
        return f"({self.transcription_id}), Meeting ID: {self.meeting_id}, Trnascription: {self.full_text}, Created at: {self.created_at}"
    

class Screenshots(db.Model):
    __tablename__ = "screenshots"
    
    screenshot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.meeting_id'))
    image_path = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    
    def __init__(self, meeting_id, image_path, timestamp):
        self.meeting_id = meeting_id
        self.image_path = image_path
        self.timestamp = timestamp
        
    def __repr__(self):
        return f"({self.screenshot_id}), Meeting ID: {self.meeting_id}, Image path: {self.image_path}, Created at: {self.timestamp}"
    
class Reports(db.Model):
    __tablename__ = "reports"
    
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.meeting_id'))
    file_path = db.Column(db.String(200))
    format = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, meeting_id, file_path, format, created_at):
        self.meeting_id = meeting_id
        self.file_path = file_path
        self.format = format
        self.created_at = created_at
        
    def __repr__(self):
        return f"({self.report_id}), Meeting ID: {self.meeting_id}, Path to report: {self.file_path}, Format: {self.format}, Created at: {self.created_at}"
    
class OCR(db.Model):
    __tablename__  = "ocr"
    
    ocr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    screenshot_id = db.Column(db.Integer, db.ForeignKey('screenshots.screenshot_id'))
    text = db.Column(db.Text)
    confidence = db.Column(db.Float)
    
    def __init__(self, screenshot_id, text, confidence):
        self.screenshot_id = screenshot_id
        self.text = text
        self.confidence = confidence
        
    def __repr__(self):
        return f"({self.ocr_id}), Screenshot ID: {self.screenshot_id}, Recognized text: {self.text}, Confidence: {self.confidence}"

