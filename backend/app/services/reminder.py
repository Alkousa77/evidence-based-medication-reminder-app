
from datetime import datetime, timedelta, timezone

from flask import jsonify, session
from app.services.base_crud import BaseCRUD
from app.models.models import ReminderEvent, ScheduleTime, MedSchedule, Medication, RiskFlag, Streak
#Upcoming remidners and update alert status
class Reminder: 
    @staticmethod
    def get_upcoming():
        
        medications = BaseCRUD.get_all_records_by_filter(Medication, user_id = session["user_id"])
        now = datetime.now(timezone.utc) #UTC is ok, only comparing, (UTC to UTC) db stores UTC
        window = now + timedelta(hours=24) # set 24-hour window to show upcoming reminders
        
        streaks = []
        reminders = []
        alerts = []
        for med in medications:
            #check if medication has active risk flag
            risk = BaseCRUD.get_first_record_by_filter(RiskFlag, medication_id = med.id)
            if risk and not risk.dismissed:
                alerts.append({"medication_id":med.id, "name":med.name})
            #get streak record fro this medication    
            streak_rec = BaseCRUD.get_first_record_by_filter(Streak, medication_id = med.id)
            if streak_rec:
                streaks.append({"medication_id":streak_rec.medication_id,"current_streak": streak_rec.current_streak})
            # loop through each schedule linked to this medication    
            for schedule in med.schedules:
                if not schedule.enabled: # if med schedule not enabled skip
                    continue
                #loop over each schedule time
                for time in schedule.times:
                    if time.next_due_at.replace(tzinfo=timezone.utc)<=window: # get reminders within 24hrs (replace naive to aware timezone)
                        reminders.append({
                            "medication_id":med.id,
                            "schedule_time_id": time.id,
                            "medication_name": med.name,
                            "next_due_at": time.next_due_at,
                            "habit_name": schedule.habit.name if schedule.habit else None
                        })
        return jsonify({"reminders":reminders,"alerts":alerts, "streaks":streaks})
                        
    
    @staticmethod
    def update_dismissd_alerts(medication_ids):
        #mark risk alert for this medication as dismissed
        for med_id in medication_ids:
            risk = BaseCRUD.get_first_record_by_filter(RiskFlag, medication_id= med_id)
            if risk:
                BaseCRUD.update(RiskFlag,risk.id, dismissed = True)
                
        return jsonify({"message": "alert dismissed"})
        
        
        