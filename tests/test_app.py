from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from app import app


client = TestClient(app)


def test_get_activities_returns_activity_list():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"]


def test_signup_for_activity_adds_participant():
    email = "pyteststudent@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_is_rejected():
    email = "existingstudent@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()
