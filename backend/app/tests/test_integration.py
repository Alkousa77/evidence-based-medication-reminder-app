from unittest.mock import patch

from app.extensions import db as _db
from app.models.models import *
from datetime import date, timedelta, time, datetime, timezone
from app.services.base_crud import BaseCRUD
from app.tests.conftest import *
from app.services.schedule_updater import UK_TZ

def register_and_login(client):
    client.post("/signup", json={"first_name": "Test",
                                 "last_name": "Last",
                                 "email": "test@test.com",
                                 "password":"pass"})
    client.post("/login", json={"email": "test@test.com",
                                 "password":"pass"})

def get_user():
    
    return User.query.filter_by(email="test@test.com").first()
    
# test 1; Check if taking a dose starts/increaments the user's streak    
def test_marking_dose_taken_increments_streak(db,client): #set client up (this sets up app and db in retrun)
    register_and_login(client)
    user= get_user()
    med= make_med(db,user.id)
    schedule = make_schedule(db,med.id)
    st = make_schedule_time(db,schedule.id)
    #dont run the send email function
    with patch("app.services.email.EmailService.send_email"):
        response = client.post(f"/doses/{st.id}/taken") #get the response after loggin the dose as taken
        
    assert response.status_code == 200
    streak =Streak.query.filter_by(medication_id = med.id).first()
    assert streak is not None #ensure streak record exist
    assert streak.current_streak == 1 #ensure streak is 1 as expected
    
 # test 2: Esure API (remidners) includes the streaks   
def test_streak_returned_in_reminders_response(client,db):
    register_and_login(client)
    user= get_user()
    med= make_med(db,user.id)
    schedule = make_schedule(db,med.id)
    st = make_schedule_time(db,schedule.id)
    BaseCRUD.create(Streak, medication_id=med.id, current_streak= 5)
    
    response = client.get("/reminders")
    data = response.get_json()
    assert any(s["current_streak"]==5 for s in data["streaks"]) #go over streaks in reminders and ck if they have streaks = 5

#test 3: confirm that risk flaggin wroks correctly
def test_low_adherence_creates_risk_flag(client, db):
    register_and_login(client)
    user= get_user()
    med= make_med(db,user.id)
    schedule = make_schedule(db,med.id)
    st = make_schedule_time(db,schedule.id)
    make_dose_logs(db, st.id, ["Missed"]*11 + ["Taken"]*2) # 13 previous records
    
    with patch("app.services.email.EmailService.send_email"):
        client.post(f"/doses/{st.id}/taken") #14th record (total = Missed(11)/taken(3))
        
    flag = RiskFlag.query.filter_by(medication_id = med.id)
    assert flag is not None
 #tes 4: ensure  alerts are included in reminders   
def test_risk_flag_returned_in_reminders_response(client, db):
    register_and_login(client)
    user= get_user()
    med= make_med(db,user.id)
    schedule = make_schedule(db,med.id)
    st = make_schedule_time(db,schedule.id)
    BaseCRUD.create(RiskFlag, medication_id = med.id)
        
    response = client.get("/reminders")
    data = response.get_json()
    assert any(alert["medication_id"]==med.id for alert in data["alerts"])
    
#test 5: check  send email is called when risk is present and caregiver's notification is enabled
def test_caregiver_email_sent_when_risk_triggered(db,client):
    register_and_login(client)
    user= get_user()
    make_caregiver(db, user.id, notify=True)
    med= make_med(db,user.id)
    schedule = make_schedule(db,med.id)
    st = make_schedule_time(db,schedule.id)
    make_dose_logs(db, st.id, ["Missed"]*11 + ["Taken"]*2) 
    with patch("app.services.email.EmailService.send_email") as mock_email:
        client.post(f"/doses/{st.id}/taken")
    mock_email.assert_called_once()
    assert mock_email.call_args[1]["to"] =="carere@test.com" #the email created with make_caregiver()
#test 6: check habit context (name) is returned with reminders    
def test_habit_linked_reminder_returns_habit_name(db, client):
    register_and_login(client)
    user= get_user()
    med= make_med(db,user.id)
    habit = make_habit(db,user.id)
    schedule = make_schedule(db,med.id, habit_id = habit.id)
    st = ScheduleTime(schedule_id = schedule.id, 
                      time_of_day= None,
                      next_due_at= datetime.now(UK_TZ)+timedelta(hours=1))
    db.session.add(st)
    db.session.commit()
    
    response = client.get("/reminders")
    data = response.get_json()
    
    assert len(data["reminders"]) ==1
    assert data["reminders"][0]["habit_name"] == "Breakfast"
    
    