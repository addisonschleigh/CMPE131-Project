from . import auth_bp
from flask import render_template, flash, redirect, url_for, request
from ..forms import LoginForm, CourseForm, AssignmentForm
from ..main.routes import courses, assignments_by_course

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    abc = {'name': 'User'}
    if form.validate_on_submit():
        flash("Not Implemented")
        return redirect('/')
    return render_template('auth/login.html', users=abc, form=form)

@auth_bp.route("/course_add", methods=["GET", "POST"])
def course_add():
    form = CourseForm()
    if form.validate_on_submit():
        course_name = form.name.data
        course_section = form.section.data
        courses[course_name] = course_section
        return redirect('/')
    return render_template('auth/course_add.html', form=form)

@auth_bp.route("/course/<course_name>/<section_name>/assignment_add", methods=["GET", "POST"])
def assignment_add(course_name, section_name):
    form = AssignmentForm()
    if form.validate_on_submit():
        assignment_name = form.name.data
        assignment_points = form.points.data
        assignments_by_course.setdefault(course_name, []).append({
            'name': assignment_name,
            "points": assignment_points
        })
        return redirect('/course/' + course_name)
    print(form.errors)
    print(request.form.get('due_date'))
    return render_template('auth/assignment_add.html', form=form, course=course_name, section=section_name)
