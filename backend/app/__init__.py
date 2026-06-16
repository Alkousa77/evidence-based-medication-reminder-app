from flask import Flask
from .config import Config
from .extensions import db
from app.services.scheduler import start_scheduler
from flask_cors import CORS
from app.routes.auth import auth
from app.routes.caregiver import caregiver
from app.routes.dose import doses
from app.routes.habit import habit
from app.routes.med import med
from app.routes.reminder import reminder
from app.routes.schedule import schedule
from app.routes.user import user
from app.config import DevConfig

# funciton to create configured flask app instance (devConfig = cloud database, testConfig = in memory db)
def create_app(config_class=DevConfig):
    app = Flask(__name__) # Create flask instance

    # Load configuration
    app.config.from_object(config_class)

    # attach extensions (DB.) to this app
    db.init_app(app)
    
    CORS(app, supports_credentials=True) # allows front to back communication (No restriction fro dev) with creds for session cookies
    #register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(caregiver)
    app.register_blueprint(doses)
    app.register_blueprint(habit)
    app.register_blueprint(med)
    app.register_blueprint(reminder)
    app.register_blueprint(schedule)
    app.register_blueprint(user)
    start_scheduler(app)
 

    return app