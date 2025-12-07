from . import main_bp
from flask import render_template, request, flash, redirect, url_for
from ..forms import LoginForm
from app import db
from flask import current_app as myapp_obj

from ..models import Course, Assignment
from ..models import User

courses = {}
assignments_by_course = {}

@main_bp.route('/')
# view functions
def index():
    return render_template('main/index.html', courses=courses)

@main_bp.route('/course/<course_name>/<section_name>')
def feature(course_name, section_name):
    course_assignments = assignments_by_course.get(course_name, [])
    return render_template('main/feature.html', course=course_name, section=section_name, assignments=course_assignments)

@main_bp.route('/course/<course_name>/<section_name>/delete', methods=['POST'])
def delete_course(course_name, section_name):
    del courses[course_name]
    return redirect(url_for('.index'))

@main_bp.route('/assignment/<course_name>/<section_name>/<assignment_name>')
def assignment(course_name, section_name, assignment_name):
    assignment_points = request.args.get('assignment_points', type=int)
    return render_template('main/assignment.html', course=course_name, section=section_name, assignment=assignment_name, points=assignment_points)

@main_bp.route('/assignment/<course_name>/<section_name>/<assignment_name>/delete', methods=['POST'])
def delete_assignment(course_name, section_name, assignment_name):
    assignment_list = assignments_by_course.get(course_name, [])

    # Remove the dict matching the assignment name
    assignments_by_course[course_name] = [
        a for a in assignment_list if a["name"] != assignment_name
    ]

    return redirect(url_for('.feature', course_name=course_name, section_name=section_name))
    '''
    course_data = assignments_by_course[course_name]
    assignment_list = course_data[course_data.index(section_name)]
    assignment_list.remove(assignment_name)
    return redirect(url_for('.feature', course_name=course_name, section_name=section_name))
    '''