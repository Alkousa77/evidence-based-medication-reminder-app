from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from app.models.models import ScheduleTime, ReminderEvent, User
from app.services.dose_logging import DoseLogging
from app.services.base_crud import BaseCRUD
from app.services.dose_handling import DoseHandler
from app.services.push import send_push_notification


def check_for_missed_doses(app):
    #set up context as scheduler runs outside flask flow 
    with app.app_context():
        schedule_times = BaseCRUD.get_all(ScheduleTime)
        #check schedule times for missed doses
        for schedule_time in schedule_times:
            DoseHandler.handle_missed(schedule_time)
        
def check_due_reminders(app):
    with app.app_context():
        now= datetime.now(timezone.utc) #current time to compare with stored due times
        due_schedules = ScheduleTime.query.filter(ScheduleTime.next_due_at <= now).all() # gets all due reminders even if the check is slightly late as schdeulr runs every 30sec
        for due_schedule in due_schedules:
            #check if reminder was already delivered
            existing = BaseCRUD.get_first_record_by_filter(ReminderEvent, schedule_time_id = due_schedule.id, delivered=True)
            if not existing:
                #create remidner event if not delivered for this schedule time
                event =  BaseCRUD.create(
                    ReminderEvent,
                    schedule_time_id = due_schedule.id,
                    delivered = False
                )
                #get user linked to this due schedule
                user = BaseCRUD.get_first_record_by_filter(User, id = due_schedule.schedule.medication.user_id)
                BaseCRUD.update(ReminderEvent, event.id, delivered=True) #update the reminder 
                #send notification if user and user tokens exist 
                if user and user.push_token: 
                    if due_schedule.schedule.habit:
                        body = f"It's time for {due_schedule.schedule.habit.name} - Don't forget to take your {due_schedule.schedule.medication.name}"
                    else:
                        body= f"It's time to take {due_schedule.schedule.medication.name}"
                    send_push_notification(user.push_token, "Medication Reminder", body)
                    print("Reminder SENT")

def start_scheduler(app):
    #create background scheduler for running reminder checks automatically
    scheduler = BackgroundScheduler()
    #check for due rmeinder evry 30 seconds
    scheduler.add_job(
        func=check_due_reminders,
        args=[app],        
        trigger="interval",
        seconds=30
    )
    #check for missed doses every 10 minutes
    scheduler.add_job(
        func=check_for_missed_doses,
        args=[app],
        trigger="interval",
        minutes=10
    )
    scheduler.start()
    
