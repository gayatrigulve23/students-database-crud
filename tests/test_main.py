import importlib
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture()
def client(monkeypatch):
    # A separate in-memory database keeps tests isolated from students.db.
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

    from app import database
    from app import main
    from app.models import Student

    database.Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[database.get_db] = override_get_db
    with TestClient(main.app) as test_client:
        yield test_client
    main.app.dependency_overrides.clear()
    test_engine.dispose()


def sample_student(email="aarav.demo@example.com"):
    return {
        "name": "Aarav Patil",
        "date_of_birth": "2005-04-12",
        "email": email,
        "phone": "9876543210",
        "course": "Computer Engineering",
        "address": "Pune, Maharashtra",
        "enrollment_date": "2025-08-01",
    }


def test_create_and_get_student(client):
    response = client.post("/students", json=sample_student())
    assert response.status_code == 201
    student_id = response.json()["id"]
    assert response.json()["name"] == "Aarav Patil"

    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "aarav.demo@example.com"


def test_list_and_filter_students(client):
    client.post("/students", json=sample_student())
    response = client.get("/students?course=Computer")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_patch_student(client):
    created = client.post("/students", json=sample_student()).json()
    response = client.patch(f"/students/{created['id']}", json={"course": "Information Technology"})
    assert response.status_code == 200
    assert response.json()["course"] == "Information Technology"


def test_delete_student(client):
    created = client.post("/students", json=sample_student()).json()
    response = client.delete(f"/students/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/students/{created['id']}").status_code == 404


def test_missing_student_returns_404(client):
    response = client.get("/students/9999")
    assert response.status_code == 404


def test_invalid_email_returns_422(client):
    payload = sample_student(email="not-an-email")
    response = client.post("/students", json=payload)
    assert response.status_code == 422


def test_contact_method_required(client):
    payload = sample_student()
    payload["email"] = None
    payload["phone"] = None
    response = client.post("/students", json=payload)
    assert response.status_code == 422
