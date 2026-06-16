from flask import jsonify, session

from app.services.base_crud import BaseCRUD
from app.models.models import MedSchedule, ScheduleDay, ScheduleTime, Medication
from app.services.schedule_updater import ScheduleUpdater

class Schedule:
    @staticmethod
    def create(data):
        
        medication_id = data["medication_id"]
        days = data["days"]
        times = data["times"]
        habit_id = data.get("habit_id") #get used as habit may not exist
        
        #create med schedule
        schedule = BaseCRUD.create(
            MedSchedule,
            medication_id = medication_id,
            habit_id = habit_id, #habit may be none
            enabled = True
        )
        #STANDARD
        #create days for standard
        if not habit_id:
            for day in days:
                BaseCRUD.create(
                    ScheduleDay,
                    schedule_id = schedule.id,
                    day_of_week = day
                )
            #create times
            for time in times:
                schedule_time = BaseCRUD.create(
                    ScheduleTime,
                    schedule_id = schedule.id,
                    time_of_day = time
                )
                #set first upcoming due EACH time
                ScheduleUpdater.set_first_next_due_at(schedule_time.id)
            
         #HABIT only need Shedule TIME record
        elif habit_id:
            schedule_time = BaseCRUD.create(
                ScheduleTime,
                schedule_id = schedule.id,
                time_of_day = None)
                
            #set first upcoming due time
            ScheduleUpdater.set_first_next_due_at(schedule_time.id)
        return jsonify({"message":"created"})
               
    @staticmethod
    def get_med_schedules(medication_id):
        
        med =  BaseCRUD.get_by_id(Medication, medication_id) 
        if not med or med.user_id != session["user_id"]:
            return jsonify({"error":"forbidden"}), 403
        schedules = BaseCRUD.get_all_records_by_filter(MedSchedule, medication_id = medication_id)      
        
        result = []
        for schedule in schedules:
            result.append({"id": schedule.id,
                           "enabled": schedule.enabled,
                          "days":  [ d.day_of_week for d in schedule.days],
                          "times": [d.time_of_day for d in schedule.times if d.time_of_day], 
                          "habit": schedule.habit.name if schedule.habit else None})    
            
        return jsonify(result)
    
    @staticmethod
    def delete(schedule_id):
        schedule = BaseCRUD.get_by_id(MedSchedule, schedule_id)

        if schedule.medication.user_id != session["user_id"]:
            return jsonify({"error":"forbidden"}), 403
        BaseCRUD.delete(MedSchedule, schedule_id)
        return jsonify({"message":"deleted"})
    #disable schedule
    @staticmethod
    def toggle(schedule_id):
        schedule = BaseCRUD.get_by_id(MedSchedule, schedule_id)

        if schedule.medication.user_id != session["user_id"]:
            return jsonify({"error":"forbidden"}), 403
        
        BaseCRUD.update(MedSchedule, schedule_id, enabled = not schedule.enabled)
        return jsonify({"message": "updated"})