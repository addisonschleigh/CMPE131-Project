from app.main import routes as main_routes
from tests.test_routes import create_test_user, login_test_user

from app.models import Course, db

def test_course_add_success(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "teacher1", password="pw", role="instructor")
    login_test_user(client, "teacher1", "pw", role="instructor")

    resp = client.post(
        "/auth/course_add?role=instructor",
        data={"name": "CS101", "section": "1"},
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert b"Course added successfully" in resp.data

    from app.models import Course
    with app.app_context():
        assert Course.query.filter_by(name="CS101", section="1").first() is not None

def test_course_add_requires_login(client):
    resp = client.post(
        "/auth/course_add",
        data={"name": "CS101", "section": "1"},
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert b"Sign in" in resp.data

def test_course_enroll_success(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "teacher1", password="secret", role="instructor")
    login_test_user(client, "teacher1", "secret", role="instructor")

    with app.app_context():
        c = Course(name="Math", section="1")
        db.session.add(c)
        db.session.commit()

    resp = client.post(
        "/auth/course_enroll?role=instructor",
        data={"name": "Math", "section": "1"},
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert b"Course enrolled successfully" in resp.data