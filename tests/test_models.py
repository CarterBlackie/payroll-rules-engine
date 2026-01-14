"""
test_models.py

Tests for payroll data models and validation logic.

Why this file exists:
- Verifies that invalid data is caught early
- Ensures models behave correctly before business rules run
- Protects against regressions when code changes

"""

import pytest
from datetime import date

from src.payroll.models import (
    Employee,
    TimeEntry,
    Timesheet,
    validate_timesheet,
)


def test_validate_timesheet_accepts_valid_data():
    """
    Happy path test.

    Why this test exists:
    - Confirms valid payroll data passes validation
    - Ensures no false positives from validation logic
    
    """
    employee = Employee(employee_id="E001", hourly_rate=25.0)

    timesheet = Timesheet(
        employee=employee,
        entries=[
            TimeEntry(work_date=date(2026, 1, 10), hours=8.0)
        ],
    )

    validate_timesheet(timesheet)


@pytest.mark.parametrize("rate", [0, -1, -10.5])
def test_validate_timesheet_rejects_non_positive_hourly_rate(rate):
    """
    Negative test.

    Why this test exists:
    - Ensures payroll never runs with invalid pay rates
    - Covers multiple invalid values using parameterization

    """
    employee = Employee(employee_id="E001", hourly_rate=rate)
    timesheet = Timesheet(employee=employee, entries=[])

    with pytest.raises(ValueError):
        validate_timesheet(timesheet)


@pytest.mark.parametrize("hours", [-0.1, -5])
def test_validate_timesheet_rejects_negative_hours(hours):
    """
    Negative test.

    Why this test exists:
    - Ensures negative work hours are rejected
    - Protects payroll calculations from invalid inputs

    """
    employee = Employee(employee_id="E001", hourly_rate=20.0)

    timesheet = Timesheet(
        employee=employee,
        entries=[
            TimeEntry(work_date=date(2026, 1, 10), hours=hours)
        ],
    )

    with pytest.raises(ValueError):
        validate_timesheet(timesheet)
