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

    Why this exists:
    - Daily overtime is a common payroll rule
    - The engine can apply this rule per TimeEntry

    Rules:
    - If hours_worked <= regular_limit: all regular
    - If hours_worked > regular_limit: remainder is overtime

    Raises:
    - ValueError if hours_worked is negative
    - ValueError if regular_limit is <= 0
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
