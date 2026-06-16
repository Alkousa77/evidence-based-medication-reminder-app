from flask import Blueprint, request, jsonify
from app.services.auth import Auth


auth = Blueprint("auth", __name__)

@auth.post("/signup")
def signup():
    data = request.json
    return Auth.signup(data)

@auth.post("/login")
def login():
    data = request.json
    return Auth.login(data)

@auth.post("/logout")
def logout():
    return Auth.logout()

