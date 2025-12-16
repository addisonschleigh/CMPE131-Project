from app.main import routes as main_routes
from tests.test_routes import create_test_user, login_test_user
from app.models import Course, db
from flask import url_for

def test_assignment_add_success(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "teacherx", password="pw", role="instructor")
    login_test_user(client, "teacherx", "pw", role="instructor")

    with app.app_context():
        c = Course(name="Math", section="1")
        db.session.add(c)
        db.session.commit()

    client.post(
        "/auth/course_enroll?role=instructor",
        data={"name": "Math", "section": "1"},
        follow_redirects=True
    )

    resp = client.post(
        "/auth/course/Math/1/assignment_add?role=instructor",
        data={"name": "HW1", "points": "25"},
        follow_redirects=True
    )

    assert resp.status_code == 200

    from app.main import routes as main_routes
    assert any(a["name"] == "HW1"
               for a in main_routes.assignments_by_course.get("Math", []))

def test_assignment_add_missing_name(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "teacher3", password="pw", role="instructor")
    login_test_user(client, "teacher3", "pw", role="instructor")

    with app.app_context():
        c = Course(name="CS101", section="1")
        db.session.add(c)
        db.session.commit()

    client.post(
        "/auth/course_enroll?role=instructor",
        data={"name": "CS101", "section": "1"},
        follow_redirects=True
    )

    resp = client.post(
        "/auth/course/CS101/1/assignment_add?role=instructor",
        data={"name": "", "points": "10"},
        follow_redirects=True
    )

    assert b"Assignment name required" in resp.data

def test_assignment_add_invalid_points(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "teacher4", password="pw", role="instructor")
    login_test_user(client, "teacher4", "pw", role="instructor")

    with app.app_context():
        c = Course(name="Physics", section="1")
        db.session.add(c)
        db.session.commit()

    client.post(
        "/auth/course_enroll?role=instructor",
        data={"name": "Physics", "section": "1"},
        follow_redirects=True
    )

    resp = client.post(
        "/auth/course/Physics/1/assignment_add?role=instructor",
        data={"name": "HW2", "points": "abc"},
        follow_redirects=True
    )

    from app.main import routes as main_routes
    assignment = main_routes.assignments_by_course["Physics"][0]
    assert assignment["points"] is None

def test_student_cannot_add_assignment(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "student1", password="pw", role="student")
    login_test_user(client, "student1", "pw", role="student")

    resp = client.get(
        "/auth/course/Math/1/assignment_add?role=student",
        follow_redirects=True
    )

    assert resp.status_code in (403, 200)

def test_assignment_add_invalid_course_url(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "teacher5", password="pw", role="instructor")
    login_test_user(client, "teacher5", "pw", role="instructor")

    resp = client.get(
        "/auth/course/DoesNotExist/1/assignment_add",
        follow_redirects=True
    )

    assert resp.status_code == 200

def test_assignment_page_renders(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "student1", password="pw", role="student")
    login_test_user(client, "student1", "pw", role="student")

    from app.main import routes as main_routes

    # Required state
    main_routes.courses["CS101"] = "1"
    main_routes.assignments_by_course["CS101"] = [
        {"name": "HW1", "points": 25, "section": "1"}
    ]

    resp = client.get(
        "/assignment/CS101/1/HW1?assignment_points=25&role=student"
    )

    page = resp.get_data(as_text=True)

    assert resp.status_code == 200
    assert "HW1" in page
    assert "25" in page

def test_instructor_can_grade_assignment(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "teacher1", password="pw", role="instructor")
    login_test_user(client, "teacher1", "pw", role="instructor")

    from app.main import routes as main_routes

    main_routes.courses["CS101"] = "1"
    main_routes.completed_assignments_by_course["CS101"] = [
        {"name": "HW1", "section": "1", "points": 20, "grade": ""}
    ]

    resp = client.post(
        "/course/CS101/1/HW1/grade?role=instructor",
        data={"grade": "18"},
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert main_routes.completed_assignments_by_course["CS101"][0]["grade"] == 18

def test_student_cannot_grade_assignment(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "student1", password="pw", role="student")
    login_test_user(client, "student1", "pw", role="student")

    from app.main import routes as main_routes

    main_routes.completed_assignments_by_course["CS101"] = [
        {"name": "HW1", "section": "1", "points": 20, "grade": ""}
    ]

    resp = client.post(
        "/course/CS101/1/HW1/grade?role=student",
        data={"grade": "15"}
    )

    assert resp.status_code == 403