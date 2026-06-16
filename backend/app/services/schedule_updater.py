from datetime import datetime, timedelta, timezone
from app.models.models import ScheduleTime
from app.services.base_crud import BaseCRUD
from zoneinfo import ZoneInfo

#get uk time zone to ahndle creation and moving coretly
UK_TZ = ZoneInfo("Europe/London")
def get_uk_now():
    return datetime.now(UK_TZ)

class ScheduleUpdater:

    @staticmethod 
    def set_first_next_due_at(schedule_time_id):
        
        now= get_uk_now()
        scheduled_time_record = BaseCRUD.get_by_id(ScheduleTime, schedule_time_id)
        #habit based
        if scheduled_time_record.schedule.habit_id:
            scheduled_time = scheduled_time_record.schedule.habit.time_of_day #get time (raw time 00:00)
            #combine now's date with the schedule time (BST is needed to store corect time on datetime)
            dt_test = datetime.combine(
                now.date(),
                scheduled_time,
                tzinfo = UK_TZ
            )
            #if the combined datetime is in the future then set the next due to it(has it passed?)
            if dt_test > now:
                next_due = dt_test
            else: # else the next due is tomorrow (habits are daily)
                next_due = dt_test + timedelta(days = 1)
                
            return BaseCRUD.update(
                            ScheduleTime,
                            schedule_time_id,
                            next_due_at = next_due
            )
            #standard
        else:    
            scheduled_time = scheduled_time_record.time_of_day # get time
            valid_days = { day.day_of_week
                            for day in scheduled_time_record.schedule.days} # find the valid next days
    
            
            for i in range(7):
                test_date = now.date() + timedelta(days = i) # iterate over the 7 days 
            
                day = test_date.strftime("%a").upper()  # get DAY for tested date
                
                
                if day in valid_days:       # check if valid days contain the tested day
                    dt_test = datetime.combine( 
                        test_date,                       # combine the test date adn scheduled time 
                        scheduled_time,
                        tzinfo=UK_TZ
                    )
                    if dt_test > now: # to test if the shcedule time hasn't passed (02/02 19:00 > 02/02 18:00)
                        return BaseCRUD.update(
                            ScheduleTime,
                            schedule_time_id,
                            next_due_at = dt_test
                        )   
                        
                    
                    
    @staticmethod 
    def move_next_due_at(schedule_time_id):
        scheduled_time_record = BaseCRUD.get_by_id(ScheduleTime, schedule_time_id)
        #no need to replace with timezone(already careated with UK_Zone, calculation only needs storeing is done with UK_zone)
        current_due_at = scheduled_time_record.next_due_at
        #habit based
        if scheduled_time_record.schedule.habit_id:
            scheduled_time = scheduled_time_record.schedule.habit.time_of_day
            next_due_date = current_due_at.date() + timedelta(days= 1)
            #zone combinig raw time (local) with date datetime has to be on zone 
            next_due = datetime.combine(
                next_due_date,
                scheduled_time,
                tzinfo=UK_TZ
            )
            
            return BaseCRUD.update(
                        ScheduleTime,
                        schedule_time_id,
                        next_due_at = next_due
            )
            
        #standard
        else:
            scheduled_time = scheduled_time_record.time_of_day
            
            valid_days = { day.day_of_week
                            for day in scheduled_time_record.schedule.days}
            
            for i in range(1,8): # checking from 1 not 0 to not check today as this method is called once the dose is logged. 
                test_date = current_due_at.date() + timedelta(days = i) # iterate over the 7 days after current_due_at
            
                day = test_date.strftime("%a").upper()  # get DAY for tested date
                
                
                if day in valid_days:       # check if valid days contain the tested day
                    dt_test = datetime.combine( 
                        test_date,                  # combine the test date and scheduled time 
                        scheduled_time,
                        tzinfo=UK_TZ
                    )
                    return BaseCRUD.update(  
                        ScheduleTime,
                        schedule_time_id,
                        next_due_at = dt_test
                    )   
                    