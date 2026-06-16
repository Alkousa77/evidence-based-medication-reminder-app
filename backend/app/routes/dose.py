
from flask import Blueprint, request, jsonify
from app.services.dose_handling import DoseHandler
from app.services.dose_logging import DoseLogging
from app.services.auth import Auth


doses = Blueprint("doses", __name__)

@doses.post("/doses/<int:schedule_time_id>/taken")
@Auth.login_required
def handle_taken(schedule_time_id):
    return DoseHandler.handle_taken(schedule_time_id)
    

@doses.get("/doses/logs")
@Auth.login_required
def get_logs():
    return DoseLogging.get_logs()