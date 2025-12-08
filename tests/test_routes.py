def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Courses" in resp.data

def test_add_course(client):
    resp = client.post(
        "/auth/course_add",
        data={"name": "Math", "section": "1"},
        follow_redirects=True
    )

    # After redirect, homepage should include the new course
    assert resp.status_code == 200
    assert b"Math" in resp.data