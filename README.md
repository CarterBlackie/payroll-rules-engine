# Payroll Rules Engine

A small Python payroll calculation engine with automated tests.

This project demonstrates how payroll business rules can be implemented,
tested, and executed in a clean and maintainable way. The focus is on
correctness, separation of concerns, and testability.

---

## Features

- Daily overtime calculation (over 8 hours per day)
- Weekly overtime calculation (over 44 hours per week)
- Gross pay calculation with overtime multiplier
- Input validation to prevent invalid payroll data
- Graceful CLI error handling for invalid input
- Automated unit tests for models, rules, engine, and I/O
- Command-line demo using sample JSON input
- Continuous Integration with GitHub Actions

---

## Payroll Rules Implemented

### Daily Overtime
- First **8 hours per day** are paid at the regular rate
- Hours beyond 8 are paid at **1.5×** the hourly rate

### Weekly Overtime
- Applied **after daily overtime**
- Total weekly hours over **44** are paid at **1.5×**
- Daily and weekly overtime are combined without double-counting

This rule ordering reflects real-world payroll systems and is covered by
unit and integration tests.

---

## Running the Demo

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Run the payroll demo

python -m src.main

### Running Tests
- Run the full automated test suite from the project root:
pytest

- Tests Cover 
    - Data validation
    - Daily and weekly overtime rules
    - Gross pay calculations
    - End-to-end payroll processing
    - JSON input loading
    - Error handling behavior

## Design Decisions

- Business rules are isolated from the payroll engine to keep logic testable and easy to extend  
- Daily overtime is applied before weekly overtime to avoid ambiguity and double-counting  
- Immutable data models prevent accidental state changes during calculations  
- Validation occurs before payroll execution to fail fast on invalid input  
- CLI errors are handled cleanly with clear messages and non-zero exit codes  
- Automated tests focus on high-risk payroll logic and edge cases  
- Continuous Integration runs tests on every push to prevent regressions

## Future Enhancements

- Statutory holiday pay rules  
- Deductions and tax calculations  
- CSV input support  
- JSON output mode for automation and integration testing  
- Configurable overtime thresholds and multipliers  
- REST API wrapper for payroll runs  
- Coverage enforcement in CI
