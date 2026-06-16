import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db as _db
from app.models.models import *
from datetime import date, timedelta, time, datetime, timezone
from app.config import TestConfig
from app.services.schedule_updater import UK_TZ

#setup  (reusable fixtures for tests) 
@pytest.fixture
def app():
    #create flask app using test config
    app = create_app(config_class=TestConfig)
    return app

@pytest.fixture
def db(app):
    # get app context to set up databse for tests
    with app.app_context():
        _db.create_all() #create all tables according to models
        yield _db # give test access to db, then pause until test done
        _db.session.remove() # close session & rollback any uncommitted transactions 
        _db.drop_all() #drop all tables and clean up 
        
@pytest.fixture
def client(app,db): 
    #create test client after app and db are ready
    return app.test_client() 


        
def make_user(db): #db param passed in through tests 
    user = User(first_name= "Test", last_name="User", email= "test@test.com", password_hash = generate_password_hash("password"))
    db.session.add(user)
    db.session.commit()
    return user

def make_med(db, user_id):
    med = Medication(user_id=user_id, name = "TestMED", dose_unit="mg", amount= 100, active= True,)
    db.session.add(med)
    db.session.commit()
    return med

def make_schedule(db, med_id, habit_id=None):
    schedule = MedSchedule(medication_id=med_id, habit_id = habit_id, enabled=True,)
    db.session.add(schedule)
    db.session.commit()
    return schedule

def make_schedule_time(db, schedule_id):
    tomorrow = datetime.now(UK_TZ) + timedelta(days=1)
    st = ScheduleTime(schedule_id= schedule_id, time_of_day= time(9,0), next_due_at= tomorrow)
    db.session.add(st)
    db.session.commit()
    return st

def make_overdue_schedule_time(db, schedule_id):
    overdue = datetime.now(UK_TZ) - timedelta(days=1)
    st = ScheduleTime(schedule_id= schedule_id, time_of_day= time(9,0), next_due_at= overdue)
    db.session.add(st)
    db.session.commit()
    return st

def make_dose_logs(db, schedule_time_id, statuses):
    today = date.today()
    for i, status in enumerate(statuses):
        log_date = today - timedelta(days=i +1)
        log = DoseLog(schedule_time_id = schedule_time_id, status= status,
                      scheduled_date = log_date, 
                      logged_at= datetime.combine(log_date, time(9,0), tzinfo=UK_TZ))
        db.session.add(log)
    db.session.commit()
    return log
    
def make_caregiver(db, user_id, notify=True):
    carer = Caregiver(user_id=user_id, first_name = "care", last_name= "giver", 
                      contact_email= "carere@test.com",notify_on_risk= notify )
    db.session.add(carer)
    db.session.commit()
    return carer

def make_habit(db, user_id):
    habit = Habit(user_id = user_id, name= "Breakfast", time_of_day= time(8, 30))
    db.session.add(habit)
    db.session.commit()
    return habit

