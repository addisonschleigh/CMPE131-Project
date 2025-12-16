from . import main_bp
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from ..forms import LoginForm
from app import db
from flask import current_app as myapp_obj

from ..models import Course, Assignment, Announcement
from ..models import User

courses = {}
assignments_by_course = {}
completed_assignments_by_course = {}
role =""
#enrolled_courses = []
#instructor_courses = []

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

            grade = None
            for ca in completed_assignments_by_course.get(course, []):
                if ca.get('name') == name and str(ca.get('section')) == section:
                    grade = ca.get('grade')
                    break

            key = (course, section, name)
            row = {'course': course, 'section': section, 'name': name, 'points': points, 'grade': grade}

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
                submitted.append({'course': course, 'section': section, 'name': name, 'points': points, 'grade': ca.get('grade')})

    return render_template('main/index.html',
                           courses=courses,
                           submitted=submitted,
                           pending=pending, role=role)

    if (role=="student"):
        return render_template(
            'main/index.html',
            courses=enrolled_courses, pending=pending,
            submitted=submitted,
            role=role)
    else:
        return render_template(
            'main/index.html',
            courses=instructor_courses, pending=pending,
            submitted=submitted,
            role=role
        )

@main_bp.route('/course/<course_name>/<section_name>')
def feature(course_name, section_name):
    role = request.args.get('role')
    course_assignments = assignments_by_course.get(course_name, [])
    completed_course_assignments = completed_assignments_by_course.get(course_name, [])

    course = Course.query.filter_by(name=course_name, section=section_name).first()
    course_announcements = Announcement.query.filter_by(course_id=course.id).order_by(Announcement.timestamp.desc()).all()

    print(role)
    return render_template(
        'main/feature.html',
        course=course_name,
        section=section_name,
        assignments=course_assignments,
        completed_assignments=completed_course_assignments,
        course_announcements=course_announcements,
        role=role
    )


@main_bp.route('/course/<course_name>/<section_name>/delete', methods=['POST'])
def delete_course(course_name, section_name):
    role = request.form.get('role') or request.args.get('role')
    del courses[course_name]
    course = Course.query.filter_by(name=course_name, section=section_name).first()
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('.index', role=role))

@main_bp.route('/assignment/<course_name>/<section_name>/<assignment_name>')
def assignment(course_name, section_name, assignment_name):
    assignment_points = request.args.get('assignment_points', type=int)
    role = request.form.get('role') or request.args.get('role')
    return render_template('main/assignment.html', course=course_name, section=section_name, assignment=assignment_name, points=assignment_points, role=role)

@main_bp.route('/assignment/<course_name>/<section_name>/<assignment_name>/delete', methods=['POST'])
def delete_assignment(course_name, section_name, assignment_name):
    role = request.form.get('role') or request.args.get('role')
    assignment_list = assignments_by_course.get(course_name, [])

    # Remove the dict matching the assignment name
    assignments_by_course[course_name] = [
        a for a in assignment_list if a["name"] != assignment_name
    ]
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
        'section': str(item.get('section', section_name)),
        'grade': ''
    }

    completed_assignments_by_course.setdefault(course_name, []).append(completed_item)

    flash(f"Submitted '{assignment_name}'.", "success")
    return redirect(url_for('main.feature', course_name=course_name, section_name=section_name, role=role))

@main_bp.route('/search')
def search():
    role = request.args.get('role')
    print(role)
    query = request.args.get('query') or request.args.get('search') or ""
    query = query.lower()
    course_results = []
    assignment_results = []

    # Search courses
    for course_name, section_name in courses.items():
        if query in course_name.lower() or query in section_name.lower():
            course_results.append({
                'course_name': course_name,
                'section_name': section_name
            })

    # Search assignments
    for course_name, assignment_list in assignments_by_course.items():
        for assignment in assignment_list:
            if query in assignment["name"].lower():
                assignment_results.append({
                    'course_name': course_name,
                    'section_name': assignment["section"],
                    'assignment_name': assignment["name"],
                    'points': assignment["points"]
                })
                print(assignment_results)

    return render_template(
        'main/search.html',
        query=query,
        courses=course_results,
        assignments=assignment_results,
        role=role
    )

@main_bp.route("/course/<course>/<section>/<assignment>/grade",
               methods=["POST"])
@login_required
def grade_assignment(course, section, assignment):
    role = request.args.get('role')
    if role != "instructor":
        abort(403)

    grade = int(request.form["grade"])

    for a in completed_assignments_by_course.get(course, []):
        if a["name"] == assignment and a["section"] == section:
            a["grade"] = grade
            break

    return redirect(request.referrer)

@main_bp.route('/course/<course_name>/<section_name>/announcement/add', methods=['GET', 'POST'])
@login_required
def add_announcement(course_name, section_name):
    role = request.args.get('role')
    if role != "instructor":
        abort(403) # Only instructors can access

    course = Course.query.filter_by(name=course_name, section=section_name).first()

    if request.method == "POST":
        # Grab the form data
        title = request.form.get("title")
        content = request.form.get("content")

        # Create and save an announcement
        announcement = Announcement(title=title, content=content, course_id=course.id, instructor_id=current_user.id)
        db.session.add(announcement)
        db.session.commit()

        flash("Announcement posted successfully!", "success")
        return redirect(url_for("main.feature", course_name=course_name, section_name=section_name, role=role))

    # GET request --> show the form
    return render_template(
        'main/add_announcements.html',
        course=course_name,
        section=section_name,
        role=role
    )