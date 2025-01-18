from datetime import datetime, timedelta
from flask import jsonify
from .models import db, Meetings

def find_active_meeting():
    current_time = datetime.now()
    tolerance = timedelta(minutes=60) # set the tolerance to 60 minutes

    active_meeting = None
    meetings = Meetings.query.all()
    for meeting in meetings:
        if meeting.scheduled_time and current_time - meeting.scheduled_time <= tolerance and current_time >= meeting.scheduled_time:
            active_meeting = meeting
            break

    if active_meeting == None:
        last_meeting = Meetings.query.order_by(Meetings.meeting_id.desc()).first()
        if last_meeting:
            #meeting_id = str(last_meeting.meeting_id)
            return last_meeting
        else:
           return None
    return active_meeting
