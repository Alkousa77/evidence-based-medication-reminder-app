from flask import Blueprint, request, jsonify
from app.services.schedule import Schedule
from app.services.auth import Auth


schedule = Blueprint("schedules", __name__)

@schedule.post("/schedules")
@Auth.login_required
def create_schedule():
    data = request.json
    return Schedule.create(data)


@schedule.get("/medications/<int:med_id>/schedules")
@Auth.login_required
def get_schedule(med_id):
    return Schedule.get_med_schedules(med_id)
        
@schedule.delete("/schedules/<int:schedule_id>")
@Auth.login_required
def delete_schedule(schedule_id):
    return Schedule.delete(schedule_id)
        
@schedule.put("/schedules/<int:schedule_id>")
@Auth.login_required
def schedule_toggle(schedule_id):
    return Schedule.toggle(schedule_id)

    