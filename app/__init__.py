from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # redirect for @login_required
login_manager.login_message_category = 'error'

# find the working directory you are in
basedir =  os.path.abspath(os.path.dirname(__file__))
def create_app():
    # Create the Flask app
    myapp_obj = Flask(__name__)
    myapp_obj.config.from_object(Config)

    # Initialize the extensions
    db.init_app(myapp_obj)
    login_manager.init_app(myapp_obj)

    # Now we import the blueprints after the db connection is initialized
    from .auth import auth_bp
    from .main import main_bp

    # Register all the blueprints
    myapp_obj.register_blueprint(auth_bp, url_prefix='/auth')
    myapp_obj.register_blueprint(main_bp)

    # Import models so the login manager can use them
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create all the tables
    with myapp_obj.app_context():
        db.create_all()

    return myapp_obj
