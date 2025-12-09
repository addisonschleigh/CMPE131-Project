import pytest
from app import create_app, db
from app.main import routes as main_routes

@pytest.fixture
def app():
    app = create_app()  # loads normal config from file
    # override values needed for tests
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clear_in_memory_stores():
    # runs before each test
    main_routes.courses.clear()
    main_routes.assignments_by_course.clear()
    main_routes.completed_assignments_by_course.clear()
    yield
    # optional cleanup after test
    main_routes.courses.clear()
    main_routes.assignments_by_course.clear()
    main_routes.completed_assignments_by_course.clear()