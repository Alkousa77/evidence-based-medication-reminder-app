from flask import jsonify, session
from app.services.base_crud import BaseCRUD
from app.models.models import Habit


class HabitService:
    
    @staticmethod
    def create(data):
        habit =  BaseCRUD.create(
        Habit,
        user_id = session["user_id"],
        name = data["name"],
        time_of_day=data["time"])
        if not habit: 
            return jsonify({"error":"failed to create habit"}), 500
        return jsonify({"message":"habit created"})
    
    @staticmethod  
    def get_all():
        habits =  BaseCRUD.get_all_records_by_filter(Habit, user_id = session["user_id"])

        result = []
        for h in habits:
            result.append({"id":  h.id,"name": h.name ,"time": h.time_of_day.strftime("%H:%M")})
            
        return jsonify(result)
    @staticmethod
    def delete(habit_id):
        habit = BaseCRUD.get_by_id(Habit, habit_id)
        if not habit or habit.user_id != session["user_id"]:
            return jsonify({"error":"forbidden"}), 403
    
        BaseCRUD.delete(Habit, habit_id)
        return jsonify({"message":"deleted"}),200
            
    @staticmethod
    def update(data):
        habit = BaseCRUD.get_first_record_by_filter(Habit, id = data["id"])
        if habit:
             updated_habit= BaseCRUD.update(Habit, habit.id, name = data.get("name")
                                   , time_of_day = data.get("time"))
             return jsonify({"id":updated_habit.id, "name": updated_habit.name, "time": updated_habit.time_of_day.strftime("%H:%M")})
        
        return jsonify({"error":"habit not found"}), 404
        
    @staticmethod
    def get_habit(habit_id):
        habit = BaseCRUD.get_by_id(Habit, habit_id)
        if habit and habit.user_id == session["user_id"]:
            return jsonify({"id": habit_id, "name": habit.name, "time": habit.time_of_day.strftime("%H:%M")})
        return jsonify({"error": "forbidden"}), 403