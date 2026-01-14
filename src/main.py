"""
main.py

Command-line entry point for the payroll rules engine demo.
"""

import sys

from src.payroll.engine import run_payroll
from src.payroll.io import load_timesheet_from_json


def main() -> int:
    # Default demo file if none is provided
    path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_timesheets.json"

    timesheet = load_timesheet_from_json(path)
    result = run_payroll(timesheet)

    print("Payroll Result")
    print("-------------")
    print(f"Employee:     {result.employee_id}")
    print(f"Hourly rate:  ${result.hourly_rate:.2f}")
    print(f"Regular hrs:  {result.regular_hours:.2f}")
    print(f"OT hrs:       {result.overtime_hours:.2f}")
    print(f"Gross pay:    ${result.gross_pay:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
