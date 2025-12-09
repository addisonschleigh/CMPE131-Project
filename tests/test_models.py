from app.models import Course, Assignment, db

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