from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def reset_activities():
    # Restore the initial in-memory state for tests
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
    })


def test_get_activities_has_expected_structure():
    # Arrange
    reset_activities()

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant_and_prevents_duplicate():
    # Arrange
    reset_activities()
    email = "newstudent@mergington.edu"
    activity = "Chess Club"

    # Act: sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Act: sign up again (duplicate)
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert duplicate is rejected
    assert resp2.status_code == 400


def test_delete_participant_removes_student():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"
    activity = "Chess Club"
    assert email in activities[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_delete_nonexistent_participant_returns_404():
    # Arrange
    reset_activities()
    email = "unknown@mergington.edu"
    activity = "Chess Club"

    # Act
    resp = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert resp.status_code == 404
