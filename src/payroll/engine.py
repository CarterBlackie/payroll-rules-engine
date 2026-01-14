"""
engine.py

This module contains the payroll engine.

Why this exists:
- Orchestrates payroll processing (validation + rule application)
- Keeps rules pure and reusable
- Produces a single result object that is easy to test and display
"""

from dataclasses import dataclass

from src.payroll.models import Timesheet, validate_timesheet
from src.payroll.rules import split_daily_overtime


@dataclass(frozen=True)
class PayrollResult:
    """
    Output of a payroll calculation for one timesheet.

    Why this exists:
    - Gives a clear, testable result for the engine
    - Keeps calculation details transparent for debugging
    """
    employee_id: str
    hourly_rate: float
    regular_hours: float
    overtime_hours: float
    gross_pay: float


def calculate_gross_pay(
    regular_hours: float,
    overtime_hours: float,
    hourly_rate: float,
    overtime_multiplier: float = 1.5,
) -> float:
    """
    Calculates gross pay using regular and overtime hours.

    Why this exists:
    - Separates pay math from aggregation logic
    - Makes pay calculation easy to unit test

    Raises:
    - ValueError if any hours are negative or hourly_rate is invalid
    """
    if hourly_rate <= 0:
        raise ValueError("hourly_rate must be greater than 0")
    if regular_hours < 0 or overtime_hours < 0:
        raise ValueError("hours must be 0 or greater")
    if overtime_multiplier < 1.0:
        raise ValueError("overtime_multiplier must be at least 1.0")

    regular_pay = regular_hours * hourly_rate
    overtime_pay = overtime_hours * hourly_rate * overtime_multiplier
    return regular_pay + overtime_pay


def run_payroll(timesheet: Timesheet) -> PayrollResult:
    """
    Runs payroll for a single timesheet.

    Steps:
    1) Validate inputs
    2) Apply daily overtime rule per entry
    3) Aggregate totals
    4) Compute gross pay
    """
    validate_timesheet(timesheet)

    total_regular = 0.0
    total_overtime = 0.0

    for entry in timesheet.entries:
        breakdown = split_daily_overtime(entry.hours)
        total_regular += breakdown.regular_hours
        total_overtime += breakdown.overtime_hours

    gross = calculate_gross_pay(
        regular_hours=total_regular,
        overtime_hours=total_overtime,
        hourly_rate=timesheet.employee.hourly_rate,
    )

    return PayrollResult(
        employee_id=timesheet.employee.employee_id,
        hourly_rate=timesheet.employee.hourly_rate,
        regular_hours=total_regular,
        overtime_hours=total_overtime,
        gross_pay=gross,
    )
