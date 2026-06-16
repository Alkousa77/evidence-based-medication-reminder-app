from flask import Blueprint, request, jsonify
from app.services.medication import MedicationService
from app.services.auth import Auth

med = Blueprint("med", __name__)

@med.post("/medications")
@Auth.login_required
def create_medication():
    data = request.json
    return MedicationService.create(data)
     

@med.get("/medications")
@Auth.login_required
def get_medications():
    return MedicationService.get_all()

@med.delete("/medications/<int:med_id>")
@Auth.login_required
def delete_medication(med_id):
    return MedicationService.delete(med_id)


@med.put("/medications")
@Auth.login_required
def update_med():
    data = request.json
    return MedicationService.update(data)



@med.get("/medications/me/<int:medication_id>")
@Auth.login_required
def get_medication(medication_id):
    return MedicationService.get_med(medication_id)