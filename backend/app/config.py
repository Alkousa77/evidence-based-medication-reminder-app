import os
from dotenv import load_dotenv

load_dotenv()  # loads .env 

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") # development cloud database
        
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" # temp in memory db 
    Testing = True

    
    