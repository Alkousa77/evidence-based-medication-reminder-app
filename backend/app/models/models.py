from datetime import datetime, timezone

from ..extensions import db


class User (db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(512), nullable=False)
    push_token = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    medications = db.relationship("Medication", backref="user", cascade= "all, delete-orphan")
    habits = db.relationship("Habit", backref="user", cascade= "all, delete-orphan")
    caregivers = db.relationship("Caregiver", backref="user", cascade= "all, delete-orphan")
    
class Habit (db.Model):
    __tablename__ = "habits"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    time_of_day = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    schedules = db.relationship("MedSchedule", backref="habit", cascade= "all, delete-orphan")
    
class Medication (db.Model):
    __tablename__ = "medications"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dose_unit = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    schedules = db.relationship("MedSchedule", backref="medication", cascade= "all, delete-orphan")
    risk_flags = db.relationship("RiskFlag", backref="medication", cascade= "all, delete-orphan")
    streak = db.relationship("Streak", uselist = False,backref="medication", cascade= "all, delete-orphan")
    notification_logs = db.relationship("CaregiverNotificationLog", backref="medication", cascade= "all, delete-orphan")

class Streak (db.Model):
    __tablename__ = "streaks"
    
    id = db.Column(db.Integer, primary_key= True)
    medication_id = db.Column(db.Integer, db.ForeignKey("medications.id"),unique = True , nullable=False)
    current_streak = db.Column(db.Integer, nullable= False, default = 0)
    
class MedSchedule (db.Model):
    __tablename__ = "med_schedules"
    
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey("medications.id"), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=True)
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    days = db.relationship("ScheduleDay", backref="schedule", cascade= "all, delete-orphan")
    times = db.relationship("ScheduleTime", backref="schedule", cascade= "all, delete-orphan")
    
class ReminderEvent (db.Model):
    __tablename__ = "reminder_events"
    
    id = db.Column(db.Integer, primary_key=True)
    schedule_time_id = db.Column(db.Integer, db.ForeignKey("schedule_times.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    delivered = db.Column(db.Boolean, default = False, nullable = False)

class ScheduleDay(db.Model):
    __tablename__ = "schedule_days"
    __table_args__ = (
        db.UniqueConstraint("schedule_id", "day_of_week", name="uq_schedule_day"),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey("med_schedules.id"), nullable=False)
    day_of_week = db.Column(db.String(3), nullable=False) # MON etc
    
    
class ScheduleTime (db.Model):
    __tablename__ = "schedule_times"
    __table_args__ = (
        db.UniqueConstraint("schedule_id", "time_of_day", name="uq_schedule_time"),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey("med_schedules.id"), nullable=False)
    time_of_day = db.Column(db.Time, nullable=True)
    next_due_at = db.Column(db.DateTime, nullable = True)
    
    dose_logs = db.relationship("DoseLog", backref="schedule_time", cascade= "all, delete-orphan")
    reminder_events = db.relationship("ReminderEvent", backref = "schedule_time", cascade = "all, delete-orphan")

class DoseLog (db.Model):
    __tablename__ = "dose_logs"
    __table_args__ = (
        db.UniqueConstraint("schedule_time_id", "scheduled_date", name="uq_schedule_logging"),  # ensures schedule_time_id is logged once, per date
    )
    
    id = db.Column(db.Integer, primary_key=True)
    schedule_time_id = db.Column(db.Integer, db.ForeignKey("schedule_times.id"), nullable=False)
    status =  db.Column(db.String(10), nullable=False) # Taken or Missed
    scheduled_date = db.Column(db.Date, nullable=False)
    logged_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    
    
class RiskFlag (db.Model):
    __tablename__ = "risk_flags"
    
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey("medications.id"),unique=True, nullable=False)
    dismissed = db.Column(db.Boolean, default=False)
    flagged_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
class Caregiver(db.Model):
    __tablename__ = "caregivers"

    id= db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable= False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    contact_email= db.Column(db.String(255), nullable=False)
    notify_on_risk = db.Column(db.Boolean, default= False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) # lambda to ensure new time on creation of record only 
    
        
    notifications = db.relationship("CaregiverNotificationLog", backref="caregiver", cascade= "all, delete-orphan")
    
class CaregiverNotificationLog(db.Model):
    __tablename__ = "caregiver_notification_logs"
    
    id= db.Column(db.Integer, primary_key=True)
    caregiver_id = db.Column(db.Integer, db.ForeignKey("caregivers.id"), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey("medications.id"), nullable=False)
    sent_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    
