from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .auth import auth_bp
from .main import main_bp
import os
from .config import Config

db = SQLAlchemy()

# find the working directory you are in
basedir =  os.path.abspath(os.path.dirname(__file__))
def create_app():

    myapp_obj = Flask(__name__)

    myapp_obj.config.from_object(Config)

    myapp_obj.register_blueprint(auth_bp, url_prefix='/auth')
    myapp_obj.register_blueprint(main_bp)


    db.init_app(myapp_obj)
    with myapp_obj.app_context():
        db.create_all()

    return myapp_obj
