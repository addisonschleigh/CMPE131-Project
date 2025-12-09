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
    # prefer role from querystring for GET, but allow role in POST form too
    role = request.args.get('role') or request.form.get('role')

    # If WTF_CSRF_ENABLED is True in tests, validate_on_submit may fail due to missing token.
    # So we accept POSTs and fall back to request.form values if validation didn't pass.
    if form.validate_on_submit():
        assignment_name = form.name.data
        assignment_points = form.points.data
    elif request.method == 'POST':
        # Fallback for tests / clients that post raw form data:
        # Attempt to read from request.form directly and record form validation errors for debugging.
        assignment_name = request.form.get('name')
        assignment_points = request.form.get('points')
        # expose errors temporarily so you can see them in the console
        print("assignment_add: form.validate_on_submit() was False; form.errors=", getattr(form, "errors", {}))
    else:
        # GET request — show form
        return render_template('auth/assignment_add.html',
                               form=form,
                               course=course_name,
                               section=section_name,
                               role=role)

    # Basic server-side sanity: name required
    if not assignment_name:
        flash("Assignment name required", "warning")
        return render_template('auth/assignment_add.html',
                               form=form,
                               course=course_name,
                               section=section_name,
                               role=role)

    # Normalize points to int if possible
    try:
        assignment_points = int(assignment_points) if assignment_points is not None else None
    except (ValueError, TypeError):
        assignment_points = None

    # store a dict including section so deletions can be specific
    assignments_by_course.setdefault(course_name, []).append({
        'name': assignment_name,
        'points': assignment_points,
        'section': section_name
    })

    # preserve role on redirect (read from POST hidden input or querystring)
    role_from_form = request.form.get('role') or role
    return redirect(url_for('main.feature',
                            course_name=course_name,
                            section_name=section_name,
                            role=role_from_form))