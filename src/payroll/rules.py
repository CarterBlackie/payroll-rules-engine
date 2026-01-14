"""
rules.py

This module contains payroll rules.

Why this exists:
- Keep business rules separate from the engine and models
- Make rules easy to test in isolation
- Make it easy to add more rules later (weekly OT, holidays, etc.)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DailyHoursBreakdown:
    """
    Represents how a single day's worked hours are split.

    Example:
    - worked_hours = 10
    - regular_hours = 8
    - overtime_hours = 2
    """
    worked_hours: float
    regular_hours: float
    overtime_hours: float


def split_daily_overtime(hours_worked: float, regular_limit: float = 8.0) -> DailyHoursBreakdown:
    """
    Splits hours into regular and overtime based on a daily threshold.

    Rules:
    - If hours_worked <= regular_limit: all regular
    - If hours_worked > regular_limit: remainder is overtime
    """
    if regular_limit <= 0:
        raise ValueError("regular_limit must be greater than 0")

    if hours_worked < 0:
        raise ValueError("hours_worked must be 0 or greater")

    regular_hours = min(hours_worked, regular_limit)
    overtime_hours = max(0.0, hours_worked - regular_limit)

    return DailyHoursBreakdown(
        worked_hours=hours_worked,
        regular_hours=regular_hours,
        overtime_hours=overtime_hours,
    )


def split_weekly_overtime(total_hours: float, weekly_limit: float = 44.0) -> tuple[float, float]:
    """
    Splits total weekly hours into weekly regular and weekly overtime.

    Returns:
    - (weekly_regular_hours, weekly_overtime_hours)
    """
    if weekly_limit <= 0:
        raise ValueError("weekly_limit must be greater than 0")
    if total_hours < 0:
        raise ValueError("total_hours must be 0 or greater")

    weekly_regular = min(total_hours, weekly_limit)
    weekly_overtime = max(0.0, total_hours - weekly_limit)

    return weekly_regular, weekly_overtime
