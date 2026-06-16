from flask import jsonify, session

from app.services.dose_logging import DoseLogging
from app.services.base_crud import BaseCRUD
from app.models.models import ScheduleTime, Medication, ReminderEvent
from app.services.adherence_calc import AdherenceCalculation
from app.services.schedule_updater import ScheduleUpdater
from app.services.streak import StreakUpdater



class DoseHandler:
    
    @staticmethod
    def handle_taken(schedule_time_id):
        
        schedule_time = BaseCRUD.get_by_id(ScheduleTime, schedule_time_id)
        if not schedule_time:
            return jsonify({"error":"not found"}), 404
        
        if schedule_time.schedule.medication.user_id != session["user_id"]:
            return jsonify({"error":"forbidden"}), 403
        #log taken
        log = DoseLogging.log_taken(schedule_time_id)

        if not log:
            return jsonify({"error":"failed to log dose"}), 500
        
        medication_id = schedule_time.schedule.medication_id
        
        #move next reminder
        ScheduleUpdater.move_next_due_at(schedule_time_id)
        
        #Streak
        StreakUpdater.update_taken_streak(medication_id)
        
        #risk calc
        AdherenceCalculation.calculate_adhernce_rate(medication_id)
        
        #delete old reminder event, so the next due time can create a new event
        old_event = BaseCRUD.get_first_record_by_filter(ReminderEvent, schedule_time_id=schedule_time_id, delivered=True)
        if old_event:
            BaseCRUD.delete(ReminderEvent, old_event.id)
        return jsonify({"message":"taken handled"})
    
    

    
    @staticmethod
    def handle_missed(schedule_time):
        #log taken
        log = DoseLogging.log_missed_if_overdue(schedule_time)
        if not log:
            return None
        
        schedule_time = BaseCRUD.get_by_id(ScheduleTime, schedule_time.id)
        medication_id = schedule_time.schedule.medication_id
        
        #move next reminder
        ScheduleUpdater.move_next_due_at(schedule_time.id)
        
        #Streak
        StreakUpdater.update_missed_streak(medication_id)
        
        #risk calc
        AdherenceCalculation.calculate_adhernce_rate(medication_id)
        
        #delete reminder event
        old_event = BaseCRUD.get_first_record_by_filter(ReminderEvent, schedule_time_id=schedule_time.id, delivered=True)
        if old_event:
            BaseCRUD.delete(ReminderEvent, old_event.id)
        return log
    
    
    