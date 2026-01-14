"""
test_engine.py

Tests for the payroll engine.
"""

import pytest
from datetime import date

from src.payroll.engine import calculate_gross_pay, run_payroll
from src.payroll.models import Employee, TimeEntry, Timesheet


def test_calculate_gross_pay_regular_only():
    gross = calculate_gross_pay(regular_hours=8.0, overtime_hours=0.0, hourly_rate=20.0)
    assert gross == 160.0


def test_calculate_gross_pay_with_overtime():
    # 8 regular at $20 = 160
    # 2 overtime at $20 * 1.5 = 60
    gross = calculate_gross_pay(regular_hours=8.0, overtime_hours=2.0, hourly_rate=20.0)
    assert gross == 220.0


@pytest.mark.parametrize("rate", [0.0, -10.0])
def test_calculate_gross_pay_rejects_invalid_rate(rate):
    with pytest.raises(ValueError):
        calculate_gross_pay(regular_hours=1.0, overtime_hours=0.0, hourly_rate=rate)


@pytest.mark.parametrize("regular,overtime", [(-1.0, 0.0), (0.0, -2.0)])
def test_calculate_gross_pay_rejects_negative_hours(regular, overtime):
    with pytest.raises(ValueError):
        calculate_gross_pay(regular_hours=regular, overtime_hours=overtime, hourly_rate=20.0)


def test_run_payroll_aggregates_multiple_days():
    employee = Employee(employee_id="E001", hourly_rate=20.0)

    # Day 1: 8 hours => 8 regular, 0 OT
    # Day 2: 10 hours => 8 regular, 2 OT
    timesheet = Timesheet(
        employee=employee,
        entries=[
            TimeEntry(work_date=date(2026, 1, 10), hours=8.0),
            TimeEntry(work_date=date(2026, 1, 11), hours=10.0),
        ],
    )

    result = run_payroll(timesheet)

    assert result.employee_id == "E001"
    assert result.regular_hours == 16.0
    assert result.overtime_hours == 2.0
    assert result.gross_pay == 380.0  # 16*20 + 2*20*1.5 = 320 + 60


def test_run_payroll_applies_weekly_overtime_after_daily():
    employee = Employee(employee_id="E002", hourly_rate=20.0)

    # 5 days × 10 hours = 50 total
    # Daily OT: 2/day × 5 = 10
    # Weekly OT: 50 - 44 = 6
    # Total OT = 16
    # Regular = 44 - 10 = 34
    timesheet = Timesheet(
        employee=employee,
        entries=[
            TimeEntry(work_date=date(2026, 1, d), hours=10.0)
            for d in range(1, 6)
        ],
    )

    result = run_payroll(timesheet)

    assert result.regular_hours == 34.0
    assert result.overtime_hours == 16.0
    assert result.gross_pay == (34 * 20) + (16 * 20 * 1.5)
