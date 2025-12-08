from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired, Optional
import datetime
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    role = SelectField('Role', choices=[('student', 'Student'), ('instructor', 'Instructor')], validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    submit = SubmitField('Create Course')

class AssignmentForm(FlaskForm):
    name = StringField('Assignment Name', validators=[DataRequired()])
    points = IntegerField('Assignment Points', validators=[DataRequired()])
#    due_date = DateTimeLocalField('Assignment Due Date', format='%y-%m-%d%H:%M:%S', validators=[Optional()], default=datetime.datetime.now)
    submit = SubmitField('Create Assignment')