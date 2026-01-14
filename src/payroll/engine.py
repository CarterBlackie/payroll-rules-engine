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
from src.payroll.rules import split_daily_overtime, split_weekly_overtime


@dataclass(frozen=True)
class PayrollResult:
    """
    Output of a payroll calculation for one timesheet.
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
    2) Apply daily overtime per entry
    3) Apply weekly overtime after daily overtime
    4) Prevent double-counting overtime
    5) Compute gross pay
    """
    validate_timesheet(timesheet)

    total_regular = 0.0
    total_daily_overtime = 0.0

    # 1) Daily overtime first
    for entry in timesheet.entries:
        breakdown = split_daily_overtime(entry.hours)
        total_regular += breakdown.regular_hours
        total_daily_overtime += breakdown.overtime_hours

    total_hours = total_regular + total_daily_overtime

    # 2) Weekly overtime based on total hours
    weekly_regular, weekly_overtime = split_weekly_overtime(total_hours)

    # 3) Adjust regular/overtime to avoid double-counting:
    # weekly_regular includes both regular + daily overtime up to the weekly limit
    # so regular hours become "weekly_regular minus daily overtime"
    adjusted_regular = max(0.0, weekly_regular - total_daily_overtime)
    adjusted_overtime = total_daily_overtime + weekly_overtime

    gross = calculate_gross_pay(
        regular_hours=adjusted_regular,
        overtime_hours=adjusted_overtime,
        hourly_rate=timesheet.employee.hourly_rate,
    )

    return PayrollResult(
        employee_id=timesheet.employee.employee_id,
        hourly_rate=timesheet.employee.hourly_rate,
        regular_hours=adjusted_regular,
        overtime_hours=adjusted_overtime,
        gross_pay=gross,
    )
