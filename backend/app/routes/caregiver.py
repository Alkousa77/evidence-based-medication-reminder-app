
from flask import Blueprint, request, jsonify
from app.services.caregiver import CaregiverService
from app.services.auth import Auth


caregiver = Blueprint("caregivers", __name__)

@caregiver.get("/caregivers")
@Auth.login_required
def get_caregivers():
    return CaregiverService.get_all()

@caregiver.post("/caregivers")
@Auth.login_required
def create_cargiver():
    data = request.json
    return CaregiverService.create(data)

@caregiver.delete("/caregivers/<int:caregiver_id>")
@Auth.login_required
def delete_cargiver(caregiver_id):
    return CaregiverService.delete(caregiver_id)

    
@caregiver.post("/caregivers/<int:caregiver_id>/toggle")
@Auth.login_required
def toggle_caregiver(caregiver_id):
    return CaregiverService.toggle(caregiver_id)

@caregiver.put("/caregivers")
@Auth.login_required
def update_caregiver():
    data = request.json
    return CaregiverService.update(data)

@caregiver.get("/caregivers/me/<int:caregiver_id>")
@Auth.login_required
def get_caregiver(caregiver_id):
    return CaregiverService.get_caregiver(caregiver_id)
