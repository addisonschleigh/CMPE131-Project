from . import main_bp
from flask import render_template
#from .forms import LoginForm
#from app import myapp_obj
from flask import current_app as myapp_obj
#from .models import User

@main_bp.route('/')
# view functions
def hello():
    return render_template('main/index.html')

@main_bp.route('/feature')
def feature():
    return render_template('main/feature.html')