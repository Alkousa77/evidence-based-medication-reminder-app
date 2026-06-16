from functools import wraps

from app.models.models import User
from app.services.base_crud import BaseCRUD
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, session




class Auth:
    @staticmethod
    def signup(data):
        password_hash = generate_password_hash(data["password"])
        
        account = BaseCRUD.create(
            User,
            first_name = data["first_name"],
            last_name = data["last_name"],
            email=data["email"],
            password_hash=password_hash
        )
        if not account:
            return jsonify({"error":"failed to create account"}),500
        
        return jsonify({"message":"account created"}),201
    
    @staticmethod
    def login(data):
        #find user by email
        user = BaseCRUD.get_first_record_by_filter(User, email= data["email"])
        
        if not user or not check_password_hash(user.password_hash, data["password"]):
            return jsonify({"error":"invalid credentials"}), 401
        
        session["user_id"]= user.id 
        return jsonify({"message": "logged in"}),200


    
    @staticmethod
    def logout():
        #remove user session if it exists
        session.pop("user_id", None) # none prevents error, if no user
        return jsonify({"message": "logged out"})
        
    # decorator to protect routes; checks if user is logged in
    def login_required(f):
        @wraps(f)  
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return jsonify({"error": "login required"}), 401
            return f(*args, **kwargs)
        return wrapper
    
    
    @staticmethod
    def get_current_user():
        user = BaseCRUD.get_first_record_by_filter(User, id=session["user_id"])
        
        return user