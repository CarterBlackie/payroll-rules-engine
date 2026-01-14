"""
models.py 

This module defines the data models for the payroll application.

Why this exists: 
- Seperate data (models) from business rules and calculations.
- Make the system easier to test and extend
- Keep payroll logic readable and maintainable

"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass(frozen=True)
class Employee:
    """
    Represents an employee in the payroll system.
    
    Why? 
    - Groups employee-related data together in one place. 
    - Prevents passing loose dictionaries around the codebase.
    - Makes test data easier to create and manage.
    
    """
    employee_id: str 
    hourly_rate: float

@dataclass(frozen=True)
class TimeEntry:
    """
    Represents a time entry for an employee.
    
    Why? 
    - Captures how many hours were worked on a specific date
    - Allows payroll rules to operate per day (ex: overtime calculations)

    """
    work_date: date
    hours: float

@dataclass(frozen=True)
class Timesheet: 
    """
    Represents a timesheet for an employee over a period of time.
    
    Why? 
    - Groups multiple time entries for an employee
    - Acts as the main inpput to the payroll engine

    """
    employee: Employee
    entries: List[TimeEntry]    

def validate_employee(employee: Employee) -> None:
    """
    Validates employee data before payroll processing.

    Why validation matters:
    - Prevents invalid payroll calculations
    - Fails early with clear error messages

    """
    if not employee.employee_id.strip():
        raise ValueError("employee_id must not be empty")

    if employee.hourly_rate <= 0:
        raise ValueError("hourly_rate must be greater than 0")


def validate_time_entry(entry: TimeEntry) -> None:
    """
    Validates a single time entry.

    Why this exists:
    - Ensures negative hours never reach payroll logic
    - Keeps rule calculations simple and safe

    """
    if entry.hours < 0:
        raise ValueError("hours must be 0 or greater")


def validate_timesheet(timesheet: Timesheet) -> None:
    """
    Validates the entire timesheet.

    Why this exists:
    - Centralizes validation logic
    - Guarantees payroll rules always receive clean data

    """
    validate_employee(timesheet.employee)

    for entry in timesheet.entries:
        validate_time_entry(entry)