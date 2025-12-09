from app.models import Course, Assignment, db, User

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

'''
def test_assignment_model_create(app):
    # run inside app context provided by fixture
    with app.app_context():
        # create a Course first if Assignment requires course_id
        c = Course(name="Science", section="1")
        db.session.add(c)
        db.session.commit()

        # create Assignment linked to course
        a = Assignment(name="Homework 1", points=10)
        db.session.add(a)
        db.session.commit()

        fetched = Assignment.query.filter_by(name="Homework 1").first()
        assert fetched is not None
        assert fetched.points == 10
'''