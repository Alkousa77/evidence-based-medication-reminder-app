from unittest.mock import patch
import pytest
from app.models.models import RiskFlag
from app.services.adherence_calc import AdherenceCalculation
from app.tests.conftest import *

def test_risk_flag_created_when_50_percent(db): #db is a fixture call to set it up before running
    
    user = make_user(db)
    med = make_med(db, user.id)
    schedule = make_schedule(db,med.id)
    schedule_time = make_schedule_time(db, schedule.id)
    make_dose_logs(db, schedule_time.id, ["Taken"]*7+["Missed"]*7)
    with patch("app.services.caregiver.CaregiverService.notify_if_enabled") : #replace notification with a mock 
        AdherenceCalculation.calculate_adhernce_rate(med.id)
        
    flag = RiskFlag.query.filter_by(medication_id= med.id).first()
    assert flag is not None, "RiskFlag should exist for 50 percent adherence"
    
    
def test_risk_flag_created_when_above_60_percent(db):
    
    user = make_user(db)
    med = make_med(db, user.id)
    schedule = make_schedule(db,med.id)
    schedule_time = make_schedule_time(db, schedule.id)
    make_dose_logs(db, schedule_time.id, ["Taken"]*10+["Missed"]*4)
    with patch("app.services.caregiver.CaregiverService.notify_if_enabled"):
        AdherenceCalculation.calculate_adhernce_rate(med.id)
        
    flag = RiskFlag.query.filter_by(medication_id= med.id).first()
    assert flag is None, "RiskFlag should Not exist for over 60 percent adherence"
    
def test_existing_risk_flag_removed_when_rate_improves(db):
    from app.services.base_crud import BaseCRUD
    
    user = make_user(db)
    med = make_med(db, user.id)
    schedule = make_schedule(db,med.id)
    schedule_time = make_schedule_time(db, schedule.id)
    BaseCRUD.create(RiskFlag, medication_id = med.id) # create pre existing risk flag
    
    make_dose_logs(db, schedule_time.id, ["Taken"]*10+["Missed"]*4)
    with patch("app.services.caregiver.CaregiverService.notify_if_enabled"):
        AdherenceCalculation.calculate_adhernce_rate(med.id)
        
    flag = RiskFlag.query.filter_by(medication_id= med.id).first()
    assert flag is None, "RiskFlag should be removed when adherence recovers"