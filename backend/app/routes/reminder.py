
from flask import Blueprint, request, jsonify
from app.services.reminder import Reminder
from app.services.auth import Auth


reminder = Blueprint("reminders", __name__)

@reminder.get("/reminders")
@Auth.login_required
def get_reminders():
    return Reminder.get_upcoming()


@reminder.post("/reminders/dismiss")
@Auth.login_required
def dismiss_alerts():
    data= request.json
    medication_ids = data.get("medication_ids", []) #default value [] 
    return Reminder.update_dismissd_alerts(medication_ids)