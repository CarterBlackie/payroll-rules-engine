from src.payroll.io import load_timesheet_from_json


def test_load_timesheet_from_json(tmp_path):
    p = tmp_path / "ts.json"
    p.write_text(
        """
        {
          "employee": {"employee_id": "E001", "hourly_rate": 20.0},
          "entries": [{"work_date": "2026-01-10", "hours": 8.0}]
        }
        """.strip(),
        encoding="utf-8",
    )

    ts = load_timesheet_from_json(str(p))
    assert ts.employee.employee_id == "E001"
    assert ts.employee.hourly_rate == 20.0
    assert len(ts.entries) == 1
    assert ts.entries[0].hours == 8.0
