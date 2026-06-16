from app import create_app
from app.extensions import db
from app.models.models import *

#create an instance of the configuerd flask app
app = create_app()

#set app context so flask uses this app instance and its db config (db.init_app(), app.config.from_object)
with app.app_context():
    db.drop_all() #remove all existing tables
    db.create_all() #recreate all tables based on models
    print(" Dropped + recreated tables.")