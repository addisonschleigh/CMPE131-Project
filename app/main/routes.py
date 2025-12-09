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
    pending = []
    submitted = []

    # Build a set of completed keys for quick lookup
    completed_index = set()
    for c_course, comp_list in completed_assignments_by_course.items():
        if not isinstance(comp_list, list):
            continue
        for ca in comp_list:
            if isinstance(ca, dict):
                name = str(ca.get('name'))
                section = str(ca.get('section', ''))
            else:
                name = str(ca)
                section = ''
            completed_index.add((c_course, section, name))

    # Scan active assignments
    for course, a_list in assignments_by_course.items():
        if not isinstance(a_list, list):
            continue
        for a in a_list:
            if isinstance(a, dict):
                name = str(a.get('name'))
                section = str(a.get('section', ''))
                points = a.get('points')
            else:
                name = str(a)
                section = ''
                points = None

            key = (course, section, name)
            row = {'course': course, 'section': section, 'name': name, 'points': points}

            if key in completed_index:
                submitted.append(row)
            else:
                pending.append(row)

    # Also include completed-only items (those removed from active lists)
    submitted_keys = {(r['course'], str(r['section']), str(r['name'])) for r in submitted}
    for course, comp_list in completed_assignments_by_course.items():
        if not isinstance(comp_list, list):
            continue
        for ca in comp_list:
            if isinstance(ca, dict):
                name = str(ca.get('name'))
                section = str(ca.get('section', ''))
                points = ca.get('points')
            else:
                name = str(ca)
                section = ''
                points = None

            key = (course, section, name)
            if key not in submitted_keys:
                submitted.append({'course': course, 'section': section, 'name': name, 'points': points})

    return render_template(
        'main/index.html',
        courses=courses, pending=pending,
        submitted=submitted,
        role=role)

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
    # preserve role for redirects if used
    role = request.form.get('role') or request.args.get('role')

    # Defensive: get course list (may be missing)
    course_list = assignments_by_course.get(course_name, [])

    # Try to find assignment matching name+section first (robust string compare)
    item = next(
        (a for a in course_list
         if str(a.get('name')) == str(assignment_name) and str(a.get('section', '')) == str(section_name)),
        None
    )

    # Fallback: match by name only (in case section wasn't stored)
    if item is None:
        item = next((a for a in course_list if str(a.get('name')) == str(assignment_name)), None)

    if item is None:
        flash("Assignment not found.", "warning")
        return redirect(url_for('main.feature', course_name=course_name, section_name=section_name, role=role))

    # Remove from active list if present
    try:
        course_list.remove(item)
    except ValueError:
        pass  # item already removed — continue

    # Normalize completed item to guarantee keys and string section
    completed_item = {
        'name': item.get('name'),
        'points': item.get('points'),
        'section': str(item.get('section', section_name))
    }

    completed_assignments_by_course.setdefault(course_name, []).append(completed_item)

    flash(f"Submitted '{assignment_name}'.", "success")
    return redirect(url_for('main.feature', course_name=course_name, section_name=section_name, role=role))