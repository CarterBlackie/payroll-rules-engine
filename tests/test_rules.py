"""
test_rules.py

Unit tests for payroll rules.

Why this exists:
- Rules are the highest-risk area (business logic bugs cost money)
- These tests prove rule correctness and cover edge cases
"""

import pytest

from src.payroll.rules import split_daily_overtime


def test_split_daily_overtime_all_regular_when_at_limit():
    result = split_daily_overtime(8.0)
    assert result.regular_hours == 8.0
    assert result.overtime_hours == 0.0


def test_split_daily_overtime_splits_when_over_limit():
    result = split_daily_overtime(10.0)
    assert result.regular_hours == 8.0
    assert result.overtime_hours == 2.0


def test_split_daily_overtime_all_regular_when_under_limit():
    result = split_daily_overtime(3.5)
    assert result.regular_hours == 3.5
    assert result.overtime_hours == 0.0


def test_split_daily_overtime_handles_zero_hours():
    result = split_daily_overtime(0.0)
    assert result.regular_hours == 0.0
    assert result.overtime_hours == 0.0


@pytest.mark.parametrize("hours", [-0.1, -5.0])
def test_split_daily_overtime_rejects_negative_hours(hours):
    with pytest.raises(ValueError):
        split_daily_overtime(hours)


@pytest.mark.parametrize("limit", [0.0, -8.0])
def test_split_daily_overtime_rejects_non_positive_regular_limit(limit):
    with pytest.raises(ValueError):
        split_daily_overtime(8.0, regular_limit=limit)
