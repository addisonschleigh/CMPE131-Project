from app.models import Course, Assignment, db, User
from app.models import Announcement
from datetime import datetime
import pytz
import pytest

def test_course_model_create(app):
    c = Course(name="Math", section="1")
    db.session.add(c)
    db.session.commit()

    fetched = Course.query.filter_by(name="Math").first()
    assert fetched is not None
    assert fetched.section == "1"


def test_assignment_model_create(app):
    c = Course(name="Science", section="1")
    db.session.add(c)
    db.session.commit()

    a = Assignment(name="Homework 1", points=10)
    db.session.add(a)
    db.session.commit()

    fetched = Assignment.query.filter_by(name="Homework 1").first()
    assert fetched is not None
    assert fetched.points == 10

def test_user_model_create(app):
    """
    Test creating a new User and verifying the data and password hashing.
    """
    # Create a user instance and set a password
    user = User(username="johndoe", email="john@example.com")
    user.set_password("SecureP@ss123")

    # Add the user to the session and commit to the test database
    db.session.add(user)
    db.session.commit()

    # Fetch the user back from the database
    fetched_user = User.query.filter_by(username="johndoe").first()

    # Assert that the user was found and data matches
    assert fetched_user is not None
    assert fetched_user.email == "john@example.com"
    # Assert that the stored password hash is not the original plain-text password
    assert fetched_user.password_hash != "SecureP@ss123"
    # Assert that the check_password method works correctly
    assert fetched_user.check_password("SecureP@ss123")

def test_announcement_creation(app):
    with app.app_context():
        instructor = User(
            username="Prof1",
            email="Prof1@sjsu.edu"
        )
        instructor.set_password("GoldenEra456!")

        course = Course(
            name="CS151",
            section="6"
        )
        db.session.add_all([instructor, course])
        db.session.commit()

        announcement = Announcement(
            title="Test Announcement",
            content="Unit test for announcement",
            course_id=course.id,
            instructor_id=instructor.id
        )
        db.session.add(announcement)
        db.session.commit()

        saved_announcement = Announcement.query.first()
        assert saved_announcement.title == "Test Announcement"
        assert saved_announcement.content == "Unit test for announcement"
        assert saved_announcement is not None

def test_announcement_auto_set_timestamp(app):
    # For this test, we are checking to see if the timestamp is automatically set
    with app.app_context():
        instructor = User(
        username="Prof2",
        email="Prof2@sjsu.edu"
    )
    instructor.set_password("GoldenBond234")

    course = Course(
     name="CS151",
     section="6"
    )
    db.session.add_all([instructor, course])
    db.session.commit()

    announcement = Announcement(
        title="Test Timestamp",
        content="Checking if the timestamp is correct",
        course_id=course.id,
        instructor_id=instructor.id
     )
    db.session.add(announcement)
    db.session.commit()

    assert announcement.timestamp is not None
    assert isinstance(announcement.timestamp, datetime)

def test_announcement_requires_title(app):
    with app.app_context():
        instructor = User(
            username="Prof3",
            email="prof3@sjsu.edu"
        )
        instructor.set_password("GoldenKnight123!")

        course = Course(
            name="CS151",
            section="6"
        )
        db.session.add_all([instructor, course])
        db.session.commit()

        bad_announcement = Announcement(
            title=None,
            content="Title is missing",
            course_id = course.id,
            instructor_id=instructor.id
        )
        db.session.add(bad_announcement)

        with pytest.raises(Exception):
            db.session.commit()