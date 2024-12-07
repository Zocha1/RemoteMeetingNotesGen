from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, DateTime, Text, Float
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import re
import datetime

Base = declarative_base()

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

class Users(Base):
    __tablename__ = "users"
    
    user_id = Column("userid", Integer, primary_key = True, autoincrement = True)
    firstname = Column("firstname", CHAR)
    lastname = Column("lastname", CHAR)
    email = Column("email", String, unique = True)

    
    def __init__(self, firstname, lastname, email):
        if not is_valid_email(email):
            raise ValueError(f"Invalid email address: {email}")
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        
    def __repr__(self):
        return f"{self.user_id}, {self.firstname} {self.lastname}, {self.email}"
    
class Meetings(Base):
    __tablename__ = "meetings"
    
    meeting_id = Column("mid", Integer, primary_key = True, autoincrement = True)
    title = Column("title", CHAR)
    scheduled_time = Column("scheduledtime", DateTime)
    platform = Column("platform", CHAR)
    created_by = Column("createdby", Integer, ForeignKey('users.userid'))
    
    def __init__(self, title, scheduled_time, platform, created_by):
        self.title = title
        self.scheduled_time = scheduled_time
        self.platform = platform
        self.created_by = created_by
    
    def __repr__(self):
        return f"({self.meeting_id}), Title: {self.title}, Scheduled time: {self.scheduled_time}, Platform: {self.platform}, Created by: {self.created_by}"
    

class Participants(Base):
    __tablename__ = "participants"
    
    participant_id = Column("pid", Integer, primary_key = True, autoincrement = True)
    meeting_id = Column("mid", Integer, ForeignKey('meetings.mid'))
    user_id = Column("userid", Integer, ForeignKey('users.userid'))
    role = Column("role", CHAR)
    joined_at = Column("joined_at", DateTime)
    
    def __init__(self, meeting_id, user_id, role, joined_at):
        self.meeting_id = meeting_id
        self.user_id = user_id
        self.role = role
        self. joined_at = joined_at
    
    def __repr__(self):
        return f"({self.participant_id}), Meeting ID: {self.meeting_id}, User ID: {self.user_id}, Role: {self.role}, Joined at: {self.joined_at}"
    
    
class Transcriptions(Base):
    __tablename__ = "transcriptions"
    
    transcription_id = Column("tid", Integer, primary_key = True, autoincrement = True)
    meeting_id = Column("mid", Integer, ForeignKey('meetings.mid'))
    full_text = Column("transcription", Text)
    created_at = Column("created_at", DateTime)

    def __init__(self, meeting_id, full_text, created_at):
        self.meeting_id = meeting_id
        self.full_text = full_text
        self.created_at = created_at
    
    def __repr__(self):
        return f"({self.transcription_id}), Meeting ID: {self.meeting_id}, Trnascription: {self.full_text}, Created at: {self.created_at}"
    

class Screenshots(Base):
    __tablename__ = "screenshots"
    
    screenshot_id = Column("scid", Integer, primary_key = True, autoincrement = True)
    meeting_id = Column("mid", Integer, ForeignKey('meetings.mid'))
    image_path = Column("image_path", CHAR)
    timestamp = Column('timestamp', DateTime)
    
    def __init__(self, meeting_id, image_path, timestamp):
        self.meeting_id = meeting_id
        self.image_path = image_path
        self.timestamp = timestamp
        
    def __repr__(self):
        return f"({self.screenshot_id}), Meeting ID: {self.meeting_id}, Image path: {self.image_path}, Created at: {self.timestamp}"
    
class Reports(Base):
    __tablename__ = "reports"
    
    report_id = Column("rid", Integer, primary_key = True, autoincrement = True)
    meeting_id = Column("mid", Integer, ForeignKey('meetings.mid'))
    file_path = Column("file_path", CHAR)
    format = Column("format", CHAR)
    created_at = Column("created_at", DateTime)
    
    def __init__(self, meeting_id, file_path, format, created_at):
        self.meeting_id = meeting_id
        self.file_path = file_path
        self.format = format
        self.created_at = created_at
        
    def __repr__(self):
        return f"({self.report_id}), Meeting ID: {self.meeting_id}, Path to report: {self.file_path}, Format: {self.format}, Created at: {self.created_at}"
    
class OCR(Base):
    __tablename__  = "ocr"
    
    ocr_id = Column("oid", Integer, primary_key = True, autoincrement = True)
    screenshot_id = Column("scid", Integer, ForeignKey('screenshots.scid'))
    text = Column("text", Text)
    confidence = Column("confidence", Float)
    
    def __init__(self, screenshot_id, text, confidence):
        self.screenshot_id = screenshot_id
        self.text = text
        self.confidence = confidence
        
    def __repr__(self):
        return f"({self.ocr_id}), Screenshot ID: {self.screenshot_id}, Recognized text: {self.text}, Confidence: {self.confidence}"

