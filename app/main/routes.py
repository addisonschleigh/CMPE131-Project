from . import main_bp
from flask import render_template
from ..forms import LoginForm
# from ...app import myapp_obj
from flask import current_app as myapp_obj

from ..models import Course
from ..models import User

courses = {}

@main_bp.route('/')
# view functions
def hello():
    return render_template('main/index.html', courses=courses)

@main_bp.route('/course1')
def feature():
    return render_template('main/feature.html', course="Course 1", assignments=["Assignment 1", "Assignment 2"])