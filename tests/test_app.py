def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_participant_and_rejects_duplicates(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Signed up student@example.com for Chess Club"}

    duplicate_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@example.com"},
    )

    assert duplicate_response.status_code == 400
    assert duplicate_response.json() == {
        "detail": "Student is already signed up for this activity"
    }


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant_and_handles_missing_signup(client):
    client.post(
        "/activities/Art Club/signup",
        params={"email": "student@example.com"},
    )

    response = client.delete(
        "/activities/Art Club/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered student@example.com from Art Club"
    }

    missing_response = client.delete(
        "/activities/Art Club/signup",
        params={"email": "student@example.com"},
    )

    assert missing_response.status_code == 404
    assert missing_response.json() == {
        "detail": "Student is not signed up for this activity"
    }


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Activity/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}