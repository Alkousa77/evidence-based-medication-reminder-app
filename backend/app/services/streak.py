from app.services.base_crud import BaseCRUD
from app.models.models import Streak


class StreakUpdater:
    
    @staticmethod
    def update_taken_streak(medication_id):
        streak = BaseCRUD.get_first_record_by_filter(Streak, medication_id = medication_id)
        
        if streak:
            return BaseCRUD.update(Streak,streak.id, current_streak = streak.current_streak +1)
            

        return BaseCRUD.create(Streak, medication_id = medication_id, current_streak = 1)
            
        
    @staticmethod
    def update_missed_streak(medication_id):
        streak = BaseCRUD.get_first_record_by_filter(Streak, medication_id = medication_id)
        
        if not streak:
            return
        
        return BaseCRUD.update(Streak,streak.id, current_streak= 0)
        
                   
