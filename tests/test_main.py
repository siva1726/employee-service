import json

from fastapi.testclient import TestClient

from src import main

client = TestClient(main.app)


def setup_employees(tmp_path, monkeypatch):
    file_path = tmp_path / "employees.json"

    data = [{"name": "Kumar", "salary": 30000}, {"name": "Siva", "salary": 35000}]

    file_path.write_text(json.dumps(data), encoding="utf-8")

    monkeypatch.setattr(main, "EMPLOYEES_FILE", file_path)

    return file_path


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_employees(tmp_path, monkeypatch):
    setup_employees(tmp_path, monkeypatch)

    response = client.get("/employees")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_employee_success(tmp_path, monkeypatch):
    setup_employees(tmp_path, monkeypatch)

    response = client.get("/employees/Kumar")

    assert response.status_code == 200
    assert response.json()["name"] == "Kumar"


def test_get_employee_not_found(tmp_path, monkeypatch):
    setup_employees(tmp_path, monkeypatch)

    response = client.get("/employees/Ravi")

    assert response.status_code == 404


def test_create_employee(tmp_path, monkeypatch):
    file_path = setup_employees(tmp_path, monkeypatch)

    response = client.post("/employees", json={"name": "Arun", "salary": 40000})

    assert response.status_code == 201
    assert response.json()["employee"]["name"] == "Arun"

    saved_data = json.loads(file_path.read_text(encoding="utf-8"))

    assert len(saved_data) == 3


def test_invalid_salary(tmp_path, monkeypatch):
    setup_employees(tmp_path, monkeypatch)

    response = client.post("/employees", json={"name": "Arun", "salary": -5})

    assert response.status_code == 422


def test_empty_name(tmp_path, monkeypatch):
    setup_employees(tmp_path, monkeypatch)

    response = client.post("/employees", json={"name": "", "salary": 25000})

    assert response.status_code == 422
