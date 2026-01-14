# Payroll Rules Engine

A small Python payroll calculation engine with automated tests.

This project demonstrates how payroll business rules can be implemented,
tested, and executed in a clean and maintainable way. The focus is on
correctness, separation of concerns, and testability.

---

## Features

- Daily overtime calculation (over 8 hours per day)
- Gross pay calculation with overtime multiplier
- Input validation to prevent invalid payroll data
- Automated unit tests for models, rules, engine, and I/O
- Command-line demo using sample JSON input

---

## Payroll Rules Implemented

### Daily Overtime
- First **8 hours per day** are paid at the regular rate
- Hours beyond 8 are paid at **1.5×** the hourly rate

The rules are isolated from the payroll engine so they can be tested
independently and extended easily.

---

## Running the Demo

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the payroll demo 
python -m src.main