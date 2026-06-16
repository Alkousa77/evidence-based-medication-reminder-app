import pytest
from app.models.models import Streak
from app.services.streak import StreakUpdater
from app.tests.conftest import make_user, make_med


def test_first_taken_creates_streak_of_1(db):
    user = make_user(db)
    med = make_med(db, user.id)
    
    StreakUpdater.update_taken_streak(med.id)
    
    streak = Streak.query.filter_by(medication_id=med.id).first()
    assert streak is not None, "Streak record should be created"
    assert streak.current_streak == 1
    
    
def test_multiple_taken_streaks(db):
    user = make_user(db)
    med = make_med(db, user.id)
    for i in range(6):
        StreakUpdater.update_taken_streak(med.id)    
    streak = Streak.query.filter_by(medication_id=med.id).first()
    assert streak.current_streak == 6
    
def test_missed_resets_streak_to_0(db):
    user = make_user(db)
    med = make_med(db, user.id)
    StreakUpdater.update_taken_streak(med.id)  
    StreakUpdater.update_taken_streak(med.id)   
    StreakUpdater.update_missed_streak(med.id)    
    streak = Streak.query.filter_by(medication_id=med.id).first()
    assert streak.current_streak == 0