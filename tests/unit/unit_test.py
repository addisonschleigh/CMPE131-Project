import pytest
from app import create_app
from flask import url_for

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clear_in_memory_data():
    """
    Run before each test to ensure in-memory stores are empty.
    Adjust import path if your blueprint module sits in a different module.
    """
    # import here so tests don't import app.main.routes at collection time
    try:
        from app.main import routes as main_routes
        # Clear both stores if present
        if hasattr(main_routes, "courses"):
            main_routes.courses.clear()
        if hasattr(main_routes, "assignments_by_course"):
            main_routes.assignments_by_course.clear()
    except Exception:
        # if your module path differs, adapt import; tests will still run but warn.
        pass

    yield

    # cleanup again after test
    try:
        from app.main import routes as main_routes
        if hasattr(main_routes, "courses"):
            main_routes.courses.clear()
        if hasattr(main_routes, "assignments_by_course"):
            main_routes.assignments_by_course.clear()
    except Exception:
        pass

def test_create_course_success(client, app):
    with app.test_request_context():
        path = url_for('auth.course_add')   # or url_for('main.create_course') if you added that route
    resp = client.post(path, data={'name': 'Math', 'section': '1'}, follow_redirects=True)
    assert resp.status_code == 200
    assert 'Math' in resp.get_data(as_text=True)