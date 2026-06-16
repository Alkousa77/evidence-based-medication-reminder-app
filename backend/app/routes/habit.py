
from flask import Blueprint, request, jsonify
from app.services.habit import HabitService
from app.services.auth import Auth


habit = Blueprint("habits", __name__)

@habit.get("/habits")
@Auth.login_required
def get():
    return HabitService.get_all()


@habit.post("/habits")
@Auth.login_required
def create():
    data = request.json
    return HabitService.create(data)


@habit.delete("/habits/<int:habit_id>")
@Auth.login_required
def delete(habit_id):
    return HabitService.delete(habit_id)

@habit.put("/habits")
@Auth.login_required
def update_habit():
    data = request.json
    return HabitService.update(data)


@habit.get("/habits/me/<int:habit_id>")
@Auth.login_required
def get_habit(habit_id):
    print("IN ROUTE")
    return HabitService.get_habit(habit_id)