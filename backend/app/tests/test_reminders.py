from unittest.mock import patch
import pytest
from app.models.models import *
from app.services.adherence_calc import AdherenceCalculation
from app.services.base_crud import BaseCRUD
from app.tests.conftest import *
from datetime import date, timedelta, time, datetime, timezone
from app.services.scheduler import check_due_reminders

# schedules with times already passed were used to confirm that reminders are still triggered once they reach their scheduled time.
# scheduler runs every 30 seconds
def test_overdue_schedule_create_reminder_events(db, app):
    user = make_user(db)
    med = make_med(db, user.id)
    schedule = make_schedule(db,med.id)
    schedule_time = make_overdue_schedule_time(db, schedule.id)
    with patch("app.services.scheduler.send_push_notification"):
        check_due_reminders(app)
        
    event = ReminderEvent.query.filter_by(schedule_time_id=schedule_time.id).first()
    assert event is not None, "A reminderEvent should be created for an over due schedule"

def test_future_schedule_does_not_trigger_reminder(db, app): #tomorrow
    user = make_user(db)
    med = make_med(db, user.id)
    schedule = make_schedule(db,med.id)
    schedule_time = make_schedule_time(db, schedule.id)
    with patch("app.services.scheduler.send_push_notification"):
        check_due_reminders(app)
        
    event = ReminderEvent.query.filter_by(schedule_time_id=schedule_time.id).first()
    assert event is None, "A reminderEvent should be created for an over due schedule"
    
def test_already_triggered_reminders_do_not_trigger_again(db, app):
    user = make_user(db)
    BaseCRUD.update(User, user.id, push_token= "token222")
    med = make_med(db, user.id)
    schedule = make_schedule(db,med.id)
    schedule_time = make_overdue_schedule_time(db, schedule.id)
    
    BaseCRUD.create(ReminderEvent, schedule_time_id= schedule_time.id, delivered= True)
    with patch("app.services.scheduler.send_push_notification") as mock_push_notification:
        check_due_reminders(app)
        
    events = ReminderEvent.query.filter_by(schedule_time_id=schedule_time.id).all()
    assert len(events) == 1, "No duplicate reminder events should be created"
    mock_push_notification.assert_not_called()
    
    