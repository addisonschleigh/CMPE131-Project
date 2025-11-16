from . import auth_bp
from flask import render_template, flash, redirect
from ..forms import LoginForm

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    abc = {'name': 'User'}
    if form.validate_on_submit():
        flash("Not Implemented")
        return redirect('/')
    return render_template('auth/login.html', users=abc, form=form)