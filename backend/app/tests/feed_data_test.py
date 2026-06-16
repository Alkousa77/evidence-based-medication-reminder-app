import sys

from app import create_app
from app.models.models import *
from datetime import datetime, timedelta, timezone
from app.services.base_crud import BaseCRUD
from werkzeug.security import generate_password_hash
from app.services.schedule_updater import UK_TZ

app = create_app()
# used to feed data for API testing (Postman)
#default: risk mode, set arg false to test safe case
def feed_data(risk=True):
    with app.app_context():
        db.drop_all()
        db.create_all()
        #create user
        user = BaseCRUD.create(User,first_name= "Reem",
                                last_name= "Leem",
                                email= "test@test.com",
                                password_hash= generate_password_hash("pass"))
        # create caregiver with email to get notifations
        BaseCRUD.create(Caregiver, 
                        user_id=user.id,
                        contact_email= "mhealthtest@outlook.com",
                        first_name= "Family",
                        last_name= "Member",
                        notify_on_risk=True)
        
        #create habit, med schedule,schedule_time so the reminders are ready
        habit = BaseCRUD.create(Habit, user_id=user.id, name="Breakfast", time_of_day=datetime.now(UK_TZ).time())
        med = BaseCRUD.create(Medication, user_id= user.id, name="Vitamin", amount=10, dose_unit="mg")
        schedule = BaseCRUD.create(MedSchedule, medication_id= med.id, habit_id=habit.id, enabled=True)
        st= BaseCRUD.create(ScheduleTime, schedule_id=schedule.id, next_due_at=datetime.now(UK_TZ))
        #get todays date fro dose logging
        today = datetime.now(UK_TZ).date()

        for i in range (1,3): ##2 missed doses if non risk mode else 2 taken doses
            BaseCRUD.create(DoseLog, 
                            schedule_time_id=st.id,
                            status= "Taken" if risk else "Missed",
                            scheduled_date = today-timedelta(days=i),
                            logged_at=datetime.now(UK_TZ) - timedelta(days=i))
            
        for i in range (3,14):#11 missde doses if risk mode else 11 taken doses
            BaseCRUD.create(DoseLog, 
                            schedule_time_id=st.id,
                            status= "Missed" if risk else "Taken",
                            scheduled_date = today-timedelta(days=i),
                            logged_at=datetime.now(UK_TZ) - timedelta(days=i))

        BaseCRUD.create(Streak, medication_id= med.id, current_streak=2 if risk else 0) #set streaks manually for testing through postman
            
        
        
if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1].lower() == "false": 
        feed_data(risk=False)
    else:
        feed_data()