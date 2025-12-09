from werkzeug.security import generate_password_hash
from app.models import User, db
from app.main import routes as main_routes

def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Courses" in resp.data

def create_test_user(app, username="teacher1", password="secret", role="instructor"):
    with app.app_context():
        u = User(username=username, email=f"{username}@example.com")

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

def login_test_user(client, username="teacher1", password="secret", role="instructor"):
    return client.post(
        "/auth/login",
        data={"username": username, "password": password, "role": role},
        follow_redirects=True
    )

def test_add_course_authenticated(client, app):
    # create user in DB and get the id (int)
    user_id = create_test_user(app, username="teacher1", password="secret", role="instructor")

    # mark the test client as "logged in" by writing the login state into its session
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_id)   # store id as string (flask-login stores strings)
        sess['_fresh'] = True

    # now call the protected route while authenticated
    resp = client.post(
        "/auth/course_add",
        data={"name": "Math", "section": "1"},
        follow_redirects=True
    )

    assert resp.status_code == 200
    assert b"Math" in resp.data

def test_assignment_add_via_form(client, app):
    # 1) create + commit a test user and sign client in via session
    user_id = create_test_user(app, username="teacherx", password="pw", role="instructor")
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_id)
        sess['_fresh'] = True

    # 2) create a course — either via the HTTP endpoint or directly
    # Option A: call the course_add route (preferred to exercise real flow)
    resp = client.post("/auth/course_add", data={"name": "Math", "section": "1"}, follow_redirects=True)
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
    from app.main import routes as main_routes
    assert main_routes.courses.get("Math") == '1'  # or whatever shape you use