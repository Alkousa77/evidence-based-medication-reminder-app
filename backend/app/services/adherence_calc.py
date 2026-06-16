from app.models.models import DoseLog, MedSchedule, ScheduleTime, RiskFlag
from app.services.base_crud import BaseCRUD 
from app.services.caregiver import CaregiverService

class AdherenceCalculation:
        
    @staticmethod
    def calculate_adhernce_rate(medication_id):

        # get the dose logs for the related med, sorted in desc order for accurate itertions to get unique dates (new to old)
        logs = DoseLog.query.filter(
            DoseLog.schedule_time.has(
                ScheduleTime.schedule.has(
                    MedSchedule.medication_id == medication_id
                )
            )
        ).order_by(DoseLog.scheduled_date.desc()).all() 
        
        unique_dates = set() # store unique dates to limit 14 days
        selected_logs = [] # store all 14 dose active days logs
        for log in logs:
            if log.scheduled_date not in unique_dates: #if log date  not in unique dates
                unique_dates.add(log.scheduled_date) #add date to unique dates
            
            if len(unique_dates) > 14: # run loop unitl there is 15 uniques dates(this ensures all doses on 14th date are included)
                break
            selected_logs.append(log) # append all logs within iterations(full 14 days doses not including the 15th "Break")
            
        # get the number of taken doses and total    
        taken = 0  
        for log in selected_logs:
            if log.status == "Taken":
                taken +=1
        total = len(selected_logs)
        
        # calcualte average 
        if total ==0:
            return
        rate = taken / total
        
        # get risk flags for med 
        risk_exists = BaseCRUD.get_first_record_by_filter(RiskFlag,medication_id = medication_id)
        #if at risk and record doesnt exist, create risk record and trigger related fucntions
        if rate <= 0.6 and not risk_exists:
            BaseCRUD.create(
                RiskFlag,
                medication_id = medication_id
            )
            CaregiverService.notify_if_enabled(medication_id)

        elif rate >0.6 and risk_exists: # if rate is more than 60% and risk flags exists delete it.
            BaseCRUD.delete(RiskFlag,risk_exists.id)
                
            
            
            
