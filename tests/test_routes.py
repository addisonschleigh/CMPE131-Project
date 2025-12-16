from werkzeug.security import generate_password_hash
from app.models import User, Course, db
from app.main import routes as main_routes

def test_register_success(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    resp = client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "pw",
            "confirm_password": "pw",
        },
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert b"registered successfully" in resp.data

    from app.models import User
    with app.app_context():
        assert User.query.filter_by(username="newuser").first() is not None

def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Courses" in resp.data

def create_test_user(app, username="teacher1", password="secret", role="instructor"):
    with app.app_context():
        u = User(
            username=username,
            email=f"{username}@example.com")

        # set password according to model API
        if hasattr(u, "set_password") and callable(getattr(u, "set_password")):
            u.set_password(password)
        elif hasattr(u, "password_hash"):
            u.password_hash = generate_password_hash(password)
        else:
            setattr(u, "password", password)

        if hasattr(u, "role"):
            setattr(u, "role", role)

        db.session.add(u)
        db.session.commit()

        # capture id while still attached to session
        user_id = int(u.id)

    # return the id (NOT the detached model instance)
    return user_id

def login_test_user(client, username, password, role="instructor"):
    return client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
            "role": role
        },
        follow_redirects=True
    )

def test_protected_route_requires_login(client):
    resp = client.get("/auth/course_enroll", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Login" in resp.data

def test_login_page_renders(client):
    resp = client.get("/auth/login")
    assert resp.status_code == 200
    assert b"Login" in resp.data

def test_logout_redirects(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "u1", password="pw")
    login_test_user(client, "u1", "pw")

    resp = client.get("/auth/logout", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Courses" in resp.data

def test_add_course_authenticated(client, app):
    # create user in DB and get the id (int)
    user_id = create_test_user(app, username="teacher1", password="secret", role="instructor")

    # mark the test client as "logged in" by writing the login state into its session
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_id)   # store id as string (flask-login stores strings)
        sess['_fresh'] = True

    # now call the protected route while authenticated
    resp = client.post(
        "/auth/course_enroll",
        data={"name": "Math", "section": "1"},
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert b"Math" in resp.data

def test_delete_course(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "teacher", password="pw", role="instructor")
    login_test_user(client, "teacher", "pw", role="instructor")

    # Create course in DB and memory
    with app.app_context():
        c = Course(name="Math", section="1")
        db.session.add(c)
        db.session.commit()

    from app.main import routes as main_routes
    main_routes.courses["Math"] = "1"

    resp = client.post(
        "/course/Math/1/delete?role=instructor",
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert "Math" not in main_routes.courses

    with app.app_context():
        assert Course.query.filter_by(name="Math").first() is None

def test_assignment_add_via_form(client, app):
    # 1) create + commit a test user and sign client in via session
    user_id = create_test_user(app, username="teacherx", password="pw", role="instructor")
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_id)
        sess['_fresh'] = True

    # 2) create a course — either via the HTTP endpoint or directly
    # Option A: call the course_add route (preferred to exercise real flow)
    resp = client.post("/auth/course_enroll", data={"name": "Math", "section": "1"}, follow_redirects=True)
    assert resp.status_code == 200

    # 3) POST to add assignment
    add_url = "/auth/course/Math/1/assignment_add"
    resp = client.post(add_url, data={"name": "HW1", "points": "25", "role": "instructor"}, follow_redirects=True)

    from app.main import routes as main_routes
    assert any(a.get("name") == "HW1" for a in main_routes.assignments_by_course.get("Math", []))
    # 4) Assert we were redirected to course page and the page shows assignment
    assert resp.status_code == 200
    page = resp.get_data(as_text=True)
    assert "HW1" in page or "Homework 1" in page

    # 5a) If you use an in-memory store (assignments_by_course), assert it contains the entry
    store_list = main_routes.assignments_by_course.get("Math", [])
    assert any(a.get("name") == "HW1" for a in store_list)

    # If you don't persist Course to DB, assert the in-memory courses dict:
#    from app.main import routes as main_routes
#    assert main_routes.courses.get("Math") == '1'  # or whatever shape you use

def test_delete_assignment(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "teacher", password="pw", role="instructor")
    login_test_user(client, "teacher", "pw", role="instructor")

    from app.main import routes as main_routes
    main_routes.assignments_by_course["CS101"] = [
        {"name": "HW1", "points": 10, "section": "1", "grade": ""}
    ]

    resp = client.post(
        "/assignment/CS101/1/HW1/delete?role=instructor",
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert main_routes.assignments_by_course["CS101"] == []

def test_submit_assignment(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "student", password="pw", role="student")
    login_test_user(client, "student", "pw", role="student")

    from app.main import routes as main_routes
    main_routes.assignments_by_course["CS101"] = [
        {"name": "HW1", "points": 20, "section": "1"}
    ]

    resp = client.post(
        "/assignment/CS101/1/HW1/submit?role=student",
        follow_redirects=True
    )

    assert resp.status_code == 200

    # Assignment removed from active list
    assert main_routes.assignments_by_course["CS101"] == []

    # Assignment added to completed list
    completed = main_routes.completed_assignments_by_course["CS101"][0]
    assert completed["name"] == "HW1"
    assert completed["section"] == "1"

def test_search_course(client):
    from app.main import routes as main_routes

    main_routes.courses["Math"] = "1"

    resp = client.get("/search?query=math")

    assert resp.status_code == 200
    assert b"Math" in resp.data