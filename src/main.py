import json
from pathlib import Path

from fastapi import FastAPI, HTTPException

from src.models import Employee

app = FastAPI(title="Employee Management API")

EMPLOYEES_FILE = Path(__file__).parent / "employees.json"


def read_employees():
    with open(EMPLOYEES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_employees(employees):
    with open(EMPLOYEES_FILE, "w", encoding="utf-8") as file:
        json.dump(employees, file, indent=4)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/employees")
def get_employees():
    return read_employees()


@app.get("/employees/{name}")
def get_employee(name: str):
    employees = read_employees()

    for employee in employees:
        if employee["name"].lower() == name.lower():
            return employee

    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=201)
def create_employee(employee: Employee):
    employees = read_employees()

    employees.append(employee.model_dump())

    save_employees(employees)

    return {"message": "Employee created successfully", "employee": employee}
