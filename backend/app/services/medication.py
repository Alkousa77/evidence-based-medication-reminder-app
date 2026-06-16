from app.services.base_crud import BaseCRUD
from app.models.models import Medication
from flask import jsonify, session

class MedicationService:
    @staticmethod
    def create(data):
        med = BaseCRUD.create(
            Medication,
            user_id = session["user_id"],
            name= data["name"],
            dose_unit=data["dose_unit"],
            amount=data["amount"],
            active= True
        )

        return jsonify({
                "id": med.id,
                "name": med.name,
                "amount": med.amount,
                "dose_unit":med.dose_unit,})
    
    
    @staticmethod
    def get_all():
        meds = BaseCRUD.get_all_records_by_filter(Medication, user_id = session["user_id"])

        result = []
        for m in meds:
            result.append({
                "id": m.id,
                "name": m.name,
                "amount": m.amount,
                "dose_unit":m.dose_unit,
                "active": m.active            
                })
        return jsonify(result)
    
    @staticmethod
    def check_med_ownership(medication_id):
        med = BaseCRUD.get_by_id(Medication, medication_id)
        if not med or med.user_id != session["user_id"]:
            return None
        return med
        
    
    @staticmethod
    def delete(medication_id):
        if not MedicationService.check_med_ownership(medication_id):
                    return jsonify({"error":"forbidden"}), 403
        BaseCRUD.delete(Medication, medication_id)
        return jsonify({"message":"deleted"})

    
    @staticmethod
    def update(data):
        
        med = BaseCRUD.get_by_id(Medication, data["id"])
        
        if not med or med.user_id != session["user_id"]:
            return jsonify({"error":"forbidden"}), 403
        
        updated =  BaseCRUD.update(
            Medication,
            data["id"],
            name=data.get("name"),
            dose_unit= data.get("dose_unit"),
            amount=data.get("amount"),
            active=data.get("active")
        )
        return jsonify({
                "id": updated.id,
                "name": updated.name,
                "amount": updated.amount,
                "dose_unit":updated.dose_unit,})
    
    @staticmethod
    def get_med(med_id):
        med = BaseCRUD.get_by_id(Medication, med_id)
        
        if not med or med.user_id != session["user_id"]:
            return jsonify({"error":"forbidden"}), 403
        
        return jsonify({"name": med.name, "amount":med.amount, "dose_unit":med.dose_unit})
        
        