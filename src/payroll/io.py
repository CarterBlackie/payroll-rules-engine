"""
io.py

This module handles input/output for the payroll demo.

Why this exists:
- Keeps file parsing separate from payroll rules/engine
- Makes it easy to swap JSON for a database or API later
"""

from __future__ import annotations

import json
from datetime import date

from src.payroll.models import Employee, TimeEntry, Timesheet


def load_timesheet_from_json(path: str) -> Timesheet:
    """
    Loads a Timesheet from a JSON file.

    Expected JSON shape:
    {
      "employee": {"employee_id": "E001", "hourly_rate": 20.0},
      "entries": [{"work_date": "2026-01-10", "hours": 8.0}]
    }
    """
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    emp_data = payload["employee"]
    employee = Employee(
        employee_id=emp_data["employee_id"],
        hourly_rate=float(emp_data["hourly_rate"]),
    )

    entries = []
    for item in payload["entries"]:
        entries.append(
            TimeEntry(
                work_date=date.fromisoformat(item["work_date"]),
                hours=float(item["hours"]),
            )
        )

    return Timesheet(employee=employee, entries=entries)
