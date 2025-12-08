from . import main_bp
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..forms import LoginForm
from app import db
from flask import current_app as myapp_obj

from ..models import Course, Assignment
from ..models import User

courses = {}
assignments_by_course = {}
completed_assignments_by_course = {}
role =""

@main_bp.route('/')
# view functions
def index():
    role = request.args.get('role')
    print(role)
    return render_template('main/index.html', courses=courses, role=role)

@main_bp.route('/course/<course_name>/<section_name>')
def feature(course_name, section_name):
    role = request.args.get('role') or request.args.get('role')
    course_assignments = assignments_by_course.get(course_name, [])
    completed_course_assignments = completed_assignments_by_course.get(course_name, [])
    print(role)
    return render_template('main/feature.html', course=course_name, section=section_name, assignments=course_assignments, completed_assignments=completed_course_assignments, role=role)


@main_bp.route('/course/<course_name>/<section_name>/delete', methods=['POST'])
def delete_course(course_name, section_name):
    role = request.form.get('role') or request.args.get('role')
    del courses[course_name]
    print(role)
    return redirect(url_for('.index', role=role))

@main_bp.route('/assignment/<course_name>/<section_name>/<assignment_name>')
def assignment(course_name, section_name, assignment_name):
    assignment_points = request.args.get('assignment_points', type=int)
    role = request.form.get('role') or request.args.get('role')
    print(role)
    return render_template('main/assignment.html', course=course_name, section=section_name, assignment=assignment_name, points=assignment_points, role=role)

@main_bp.route('/assignment/<course_name>/<section_name>/<assignment_name>/delete', methods=['POST'])
def delete_assignment(course_name, section_name, assignment_name):
    role = request.form.get('role') or request.args.get('role')
    assignment_list = assignments_by_course.get(course_name, [])

    # Remove the dict matching the assignment name
    assignments_by_course[course_name] = [
        a for a in assignment_list if a["name"] != assignment_name
    ]
    print(role)
    return redirect(url_for('.feature', course_name=course_name, section_name=section_name, role=role))

@main_bp.route('/assignment/<course_name>/<section_name>/<assignment_name>/submit', methods=['POST'])
def submit_assignment(course_name, section_name, assignment_name):
    role = request.form.get('role') or request.args.get('role')
    assignments = assignments_by_course.get(course_name, [])
    assignment = next(
        (a for a in assignments if a["name"] == assignment_name and a["section"] == section_name),
        None
    )
    if assignment is None:
        flash ("Assignment not found", "error")
        print(role)
        return redirect(url_for('main.feature', course_name=course_name, section_name=section_name, role=role))

    assignments.remove(assignment)
    completed_assignments_by_course.setdefault(course_name, []).append(assignment)

    flash(f"'{assignment_name}' submitted", "success")
    print(role)
    return redirect(url_for('main.feature', course_name=course_name, section_name=section_name, role=role))