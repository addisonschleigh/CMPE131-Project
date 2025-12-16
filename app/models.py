from email.policy import default
from time import timezone

from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import pytz
from flask_sqlalchemy import SQLAlchemy

class User(db.Model, UserMixin):
    id =  db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable= False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    section = db.Column(db.String(32), nullable=False)
#    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    points = db.Column(db.Integer, nullable=False)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(pytz.timezone('America/Los_Angeles')), nullable=False)

    course = db.relationship('Course', backref='announcements')
    instructor = db.relationship('User', backref='announcements')