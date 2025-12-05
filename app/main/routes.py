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

@main_bp.route('/course/<course_name>')
def feature(course_name):
    return render_template('main/feature.html', course=course_name, assignments=["Assignment 1", "Assignment 2"])