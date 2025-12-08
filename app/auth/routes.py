from . import auth_bp
from flask_login import login_user, logout_user, login_required, current_user
from ..forms import RegisterForm
from ..models import User
from .. import db
from flask import render_template, flash, redirect, url_for, request
from ..forms import LoginForm, CourseForm, AssignmentForm
from ..main.routes import courses, assignments_by_course

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    abc = {'name': 'User'}
    if form.validate_on_submit():
        # We want to be able to look up the user by their username
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            role = form.role.data
            print(role)
            flash('You have been logged in successfully.', category= 'success')
            return redirect(url_for('main.index', role=role))
        else:
            flash('Login unsuccessful. Please check username and password.', category='error')

    # Now check if the user is authenticated after the form submission
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    return render_template('auth/login.html', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('main.index'))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        # Check existing username
        if existing_user:
            flash('Username already taken. Please choose a different one.')
            return render_template("auth/register.html", form=form)

        # Check existing email
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already taken. Please choose a different one.', category='error')
            return render_template("auth/register.html", form=form)

         # create a new user
        user = User(
             username=form.username.data,
             email=form.email.data,
         )
        user.set_password(form.password.data) # hashes the password
        db.session.add(user)
        db.session.commit()

        flash('You have been registered successfully.', category='success')
        return redirect(url_for('auth.login'))

    return render_template("auth/register.html", form=form)

@auth_bp.route("/course_add", methods=["GET", "POST"])
@login_required
def course_add():
    form = CourseForm()
    role = request.args.get('role')
    if form.validate_on_submit():
        course_name = form.name.data
        course_section = form.section.data
        courses[course_name] = course_section

        role_from_form = request.form.get('role')
        return redirect(url_for('main.index', role=role_from_form))
    return render_template('auth/course_add.html', form=form, role=role)

@auth_bp.route("/course/<course_name>/<section_name>/assignment_add", methods=["GET", "POST"])
@login_required
def assignment_add(course_name, section_name):
    form = AssignmentForm()
    role = request.args.get('role')
    if form.validate_on_submit():
        assignment_name = form.name.data
        assignment_points = form.points.data
        # store a dict including section so deletions can be specific
        assignments_by_course.setdefault(course_name, []).append({
            'name': assignment_name,
            'points': assignment_points,
            'section': section_name
        })
        role_from_form = request.form.get('role')
        return redirect(url_for('main.feature', course_name=course_name, section_name=section_name, role=role_from_form))

    return render_template('auth/assignment_add.html', form=form, course=course_name, section=section_name, role=role)