from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from flask import jsonify, session
from app.models.models import DoseLog, ScheduleTime, MedSchedule, Medication
from app.services.base_crud import BaseCRUD 

UK_TZ = ZoneInfo("Europe/London")
def get_uk_now():
    return datetime.now(UK_TZ)

class DoseLogging:
    
    @staticmethod
    def log_taken(schedule_time_id):
        now= get_uk_now()
        
        schedule_time_record = BaseCRUD.get_by_id(ScheduleTime, schedule_time_id)
        if not schedule_time_record:
            return None
        # using BST timezone befre .date(), DB stores date as is no conversion to UTC, around midnight logging date can be wrong 
        scheduled_datetime = schedule_time_record.next_due_at.replace(tzinfo=timezone.utc).astimezone(UK_TZ) 
        
        
        exists = BaseCRUD.get_first_record_by_filter(
            DoseLog, schedule_time_id=schedule_time_record.id, scheduled_date = scheduled_datetime.date())
        
        if exists:
            return None
        if now> scheduled_datetime + timedelta(minutes= 60): # dont allow for logging after grace window if missed logger hasnt run yet
            return None
        
        log = BaseCRUD.create(DoseLog, 
                               schedule_time_id=schedule_time_record.id, 
                               status="Taken", 
                               scheduled_date=scheduled_datetime.date(), 
                               logged_at=now)
        return {log}
 
    @staticmethod
    def log_missed_if_overdue(schedule_time):
        
        now= get_uk_now()

        scheduled_datetime = schedule_time.next_due_at.replace(tzinfo=timezone.utc).astimezone(UK_TZ) 
        # if within grace period
        if now <= scheduled_datetime + timedelta(minutes=60):   # 18:00 <= 19:00(due time with grace period) not reached 
            return None 
        
        #if already logged
        exists = BaseCRUD.get_first_record_by_filter(
            DoseLog, schedule_time_id=schedule_time.id, scheduled_date = scheduled_datetime.date() )
        if exists:
            return None
        
        return BaseCRUD.create(
            DoseLog,
            schedule_time_id=schedule_time.id,
            status="Missed",
            scheduled_date=scheduled_datetime.date(),
            logged_at=now
        )
     #get all logs linked to the logged in user's medication 
    @staticmethod
    def get_logs():
        doses = DoseLog.query.filter(DoseLog.schedule_time.has(
            ScheduleTime.schedule.has(
                MedSchedule.medication.has(
                    Medication.user_id == session["user_id"]
                )
            )
        )).all()
        
        return jsonify([{"id":d.id,"status":d.status,"scheduled_date":d.logged_at,
                         "medication":d.schedule_time.schedule.medication.name}for d in doses])
            