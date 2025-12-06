from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired, Optional
import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    submit = SubmitField('Create Course')

class AssignmentForm(FlaskForm):
    name = StringField('Assignment Name', validators=[DataRequired()])
    points = IntegerField('Assignment Points', validators=[DataRequired()])
#    due_date = DateTimeLocalField('Assignment Due Date', format='%y-%m-%d%H:%M:%S', validators=[Optional()], default=datetime.datetime.now)
    submit = SubmitField('Assign Course')