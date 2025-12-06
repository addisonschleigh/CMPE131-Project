from . import main_bp
from flask import render_template
from ..forms import LoginForm
# from ...app import myapp_obj
from flask import current_app as myapp_obj

from ..models import Course, Assignment
from ..models import User

courses = {}
assignments_by_course = {}

@main_bp.route('/')
# view functions
def hello():
    return render_template('main/index.html', courses=courses)

@main_bp.route('/course/<course_name>/<section_name>')
def feature(course_name, section_name):
    course_assignments = assignments_by_course.get(course_name, [])
    return render_template('main/feature.html', course=course_name, section=section_name, assignments=course_assignments)