"""
test_rules.py

Unit tests for payroll rules.
"""

import pytest

from src.payroll.rules import split_daily_overtime, split_weekly_overtime


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


def test_split_weekly_overtime_under_limit():
    regular, overtime = split_weekly_overtime(40.0)
    assert regular == 40.0
    assert overtime == 0.0


def test_split_weekly_overtime_over_limit():
    regular, overtime = split_weekly_overtime(50.0)
    assert regular == 44.0
    assert overtime == 6.0


@pytest.mark.parametrize("hours", [-0.1, -10.0])
def test_split_weekly_overtime_rejects_negative_hours(hours):
    with pytest.raises(ValueError):
        split_weekly_overtime(hours)


@pytest.mark.parametrize("limit", [0.0, -44.0])
def test_split_weekly_overtime_rejects_non_positive_limit(limit):
    with pytest.raises(ValueError):
        split_weekly_overtime(44.0, weekly_limit=limit)
