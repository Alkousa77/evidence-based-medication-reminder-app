from flask import jsonify, session
from app.services.base_crud import BaseCRUD
from app.models.models import Caregiver, Medication, CaregiverNotificationLog
from app.services.email import EmailService

class CaregiverService:
    
    @staticmethod
    def create(data):
        caregiver = BaseCRUD.create(
            Caregiver,
            user_id = session["user_id"],
            first_name = data["first_name"],
            last_name = data["last_name"],
            contact_email = data["contact_email"],
            notify_on_risk = False #default to false
        )
        if not caregiver:
            return jsonify({"error":"failed to create caregiver"}), 500
        
        return jsonify({"message": "caregiver created"})
    @staticmethod
    def get_all():
        caregivers =  BaseCRUD.get_all_records_by_filter(Caregiver, user_id  = session["user_id"])
    
        
        return jsonify([{"id": c.id, "first_name":c.first_name ,"last_name": c.last_name ,"email":c.contact_email, "notify": c.notify_on_risk} for c in caregivers] #list of dict
        )
    
    @staticmethod
    def update(data):
        carer = BaseCRUD.get_first_record_by_filter(Caregiver, id = data["id"])
        if carer:
            updated_caregiver =  BaseCRUD.update(Caregiver, id= carer.id, first_name = data.get("first_name")
                                   , last_name = data.get("last_name"),contact_email = data.get("contact_email"))
            return jsonify({"id": updated_caregiver.id, "first_name":updated_caregiver.first_name ,"last_name": updated_caregiver.last_name ,"email":updated_caregiver.contact_email})
        
        return jsonify({"error":"caregiver not found"}), 404
        
    
    
    @staticmethod
    def delete(caregiver_id):
        caregiver = BaseCRUD.get_by_id(Caregiver, caregiver_id)
        
        if not caregiver or caregiver.user_id != session["user_id"]:
            return jsonify({"error":"forbidden"}), 403 
        
        BaseCRUD.delete(Caregiver, caregiver_id)
        return jsonify({"message":"deleted"}), 200
    #toggle notification for caregiver
    @staticmethod
    def toggle(caregiver_id):
        caregiver = BaseCRUD.get_by_id(Caregiver, caregiver_id)
        if not caregiver or caregiver.user_id != session["user_id"]:
             return jsonify({"error":"forbidden"}), 403
        print(caregiver.notify_on_risk)
        BaseCRUD.update(Caregiver, caregiver_id, notify_on_risk = not caregiver.notify_on_risk)
        return jsonify({"message":"updated"}), 200
    
    
    #notify caregiver via email
    @staticmethod
    def notify_if_enabled(medication_id):
        #get med
        medication = BaseCRUD.get_by_id(Medication, medication_id)
        if not medication:
            return
        
        user = medication.user
        caregivers = user.caregivers
        #get caregivers that have enabled notifcaiton
        for caregiver in caregivers:
            if caregiver.notify_on_risk:

               EmailService.send_email(
                   to=caregiver.contact_email,
                   body= f"Alert: {user.first_name} may be at risk of non adherence to {medication.name}."
               )
               
               # log notification
               BaseCRUD.create(
                   CaregiverNotificationLog,
                   caregiver_id = caregiver.id,
                   medication_id = medication_id
               ) 
               
               
               
    @staticmethod
    def get_caregiver(caregiver_id):
        caregiver = BaseCRUD.get_by_id(Caregiver, caregiver_id)
        if not caregiver or caregiver.user_id != session["user_id"]:
            return jsonify({"error":"forbidden"}), 403
        return jsonify({"id": caregiver.id, "first_name": caregiver.first_name, "last_name":caregiver.last_name, "email":caregiver.contact_email})
