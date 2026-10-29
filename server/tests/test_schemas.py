import pytest
from pydantic import ValidationError

from app.schemas.courses import CourseCreate
from app.schemas.intakes import IntakeCreate
from app.schemas.schedules import ScheduleCreate


def test_course_rejects_invalid_dates():
    with pytest.raises(ValidationError):
        CourseCreate(
            start_date="2026-09-20",
            end_date="2026-09-19",
            encrypted_data="data",
        )


def test_schedule_normalizes_days():
    schedule = ScheduleCreate(
        scheduled_at="09:00",
        days_of_week=[7, 1, 1],
        encrypted_data="data",
    )
    assert schedule.days_of_week == [1, 7]


def test_intake_requires_timezone():
    with pytest.raises(ValidationError):
        IntakeCreate(
            taken_at="2026-09-19T12:00:00",
            encrypted_data="data",
        )


def test_encrypted_data_cannot_be_blank():
    with pytest.raises(ValidationError):
        ScheduleCreate(
            scheduled_at="09:00",
            days_of_week=[1],
            encrypted_data="   ",
        )
