from . import auth_bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from ..forms import LoginForm
from ..forms import RegisterForm
from ..models import User
from .. import db

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    #abc = {'name': 'User'}
    form = LoginForm()
    if form.validate_on_submit():
        # We want to be able to look up the user by their username
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You have been logged in successfully.', category= 'success')
            return redirect(url_for('main.hello'))
        else:
            flash('Login unsuccessful. Please check username and password.', category='error')

    # Now check if the user is authenticated after the form submission
    if current_user.is_authenticated:
        return redirect(url_for('main.hello'))

    return render_template('auth/login.html', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('main.hello'))

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