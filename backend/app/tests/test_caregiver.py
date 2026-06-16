from unittest.mock import patch
import pytest
from app.models.models import RiskFlag, CaregiverNotificationLog
from app.services.adherence_calc import AdherenceCalculation
from app.services.base_crud import BaseCRUD
from app.tests.conftest import *

def test_caregiver_with_notify_on_recieves_email(db):
    user = make_user(db)
    med = make_med(db, user.id)
    schedule = make_schedule(db,med.id)
    schedule_time = make_schedule_time(db, schedule.id)
    make_dose_logs(db, schedule_time.id, ["Taken"]*7+["Missed"]*7)
    make_caregiver(db,user.id, notify=True)
    with patch("app.services.email.EmailService.send_email") as mock_email:
        AdherenceCalculation.calculate_adhernce_rate(med.id)
        
    mock_email.assert_called_once()
    
def test_caregiver_with_notify_off_does_not_recieve_email(db):
    user = make_user(db)
    med = make_med(db, user.id)
    schedule = make_schedule(db,med.id)
    schedule_time = make_schedule_time(db, schedule.id)
    make_dose_logs(db, schedule_time.id, ["Taken"]*7+["Missed"]*7)
    make_caregiver(db,user.id, notify=False)
    with patch("app.services.email.EmailService.send_email") as mock_email:
        AdherenceCalculation.calculate_adhernce_rate(med.id)
        
    mock_email.assert_not_called()
    
def test_caregiver_notifiation_no_risk_no_email_sent(db):
    user = make_user(db)
    med = make_med(db, user.id)
    schedule = make_schedule(db,med.id)
    schedule_time = make_schedule_time(db, schedule.id)
    make_dose_logs(db, schedule_time.id, ["Taken"]*11+["Missed"]*3)
    make_caregiver(db,user.id, notify=True)
    with patch("app.services.email.EmailService.send_email") as mock_email:
        AdherenceCalculation.calculate_adhernce_rate(med.id)
        
    mock_email.assert_not_called()
    
    