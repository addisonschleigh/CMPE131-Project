from tests.test_routes import login_test_user, create_test_user

def test_dashboard_shows_submitted_assignment(client, app):
    app.config["WTF_CSRF_ENABLED"] = False

    create_test_user(app, "student1", password="pw", role="student")
    login_test_user(client, "student1", "pw", role="student")

    from app.main import routes as main_routes

    # COURSE MUST EXIST
    main_routes.courses["CS101"] = "1"

    # Active assignment
    main_routes.assignments_by_course["CS101"] = [
        {"name": "HW1", "points": 20, "section": "1"}
    ]

    # Submit assignment
    client.post(
        "/assignment/CS101/1/HW1/submit?role=student",
        follow_redirects=True
    )

    # Dashboard
    resp = client.get("/?role=student")
    page = resp.get_data(as_text=True)

    assert resp.status_code == 200

    # Assignment now visible
    assert "HW1" in page

    # Sanity: it is no longer pending
    assert main_routes.assignments_by_course["CS101"] == []
    assert len(main_routes.completed_assignments_by_course["CS101"]) == 1