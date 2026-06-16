from flask import Blueprint, request, jsonify
from app.extensions import db
from app.services.auth import Auth
from app.models.models import User
from app.services.base_crud import BaseCRUD


user = Blueprint("user", __name__)

@user.post("/users/push-token")
@Auth.login_required
def save_push_token():
    token =request.json.get("token") #get token  
    current_user = Auth.get_current_user() #get user
    BaseCRUD.update(User, current_user.id, push_token=token) #update record to include push notification token
    
    return jsonify({"message":"Push token saved"})


@user.get("/users/me")
@Auth.login_required
def get_user():
    user_details =  Auth.get_current_user()
    return jsonify({"first_name":user_details.first_name, "last_name":user_details.last_name, "email":user_details.email})

@user.put("/users/me")
@Auth.login_required
def update_user():
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    user_details = Auth.get_current_user()
    BaseCRUD.update(User, user_details.id, email = email, first_name=first_name, last_name=last_name)
    return jsonify({"message": "updated user"}), 200


@user.delete("/users/me")
@Auth.login_required
def delete_user():
     user_details =  Auth.get_current_user()
     BaseCRUD.delete(User, user_details.id)
     return jsonify({"message":"deleted user"}),200