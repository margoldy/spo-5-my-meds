from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ScheduleCreate(BaseModel):
    scheduled_at: time
    days_of_week: list[int] = Field(min_length=1)
    encrypted_data: str = Field(min_length=1, max_length=16384)

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, value: list[int]) -> list[int]:
        days = sorted(set(value))
        if any(day < 1 or day > 7 for day in days):
            raise ValueError("Дни недели должны быть от 1 до 7")
        return days

    @field_validator("encrypted_data")
    @classmethod
    def validate_encrypted_data(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Зашифрованные данные не могут быть пустыми")
        return value


class ScheduleUpdate(BaseModel):
    scheduled_at: time | None = None
    days_of_week: list[int] | None = Field(default=None, min_length=1)
    encrypted_data: str | None = Field(default=None, min_length=1, max_length=16384)

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, value: list[int] | None) -> list[int] | None:
        if value is None:
            raise ValueError("Дни недели не могут быть пустыми")

        days = sorted(set(value))
        if any(day < 1 or day > 7 for day in days):
            raise ValueError("Дни недели должны быть от 1 до 7")
        return days

    @field_validator("scheduled_at", "encrypted_data")
    @classmethod
    def validate_required_values(cls, value):
        if value is None:
            raise ValueError("Переданное поле не может быть пустым")
        return value

    @field_validator("encrypted_data")
    @classmethod
    def validate_encrypted_data(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Зашифрованные данные не могут быть пустыми")
        return value


class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    scheduled_at: time
    days_of_week: list[int]
    encrypted_data: str


class ScheduleListResponse(BaseModel):
    items: list[ScheduleResponse]


class ScheduleIntakeResponse(BaseModel):
    id: UUID
    taken_at: datetime
    encrypted_data: str


class ScheduleDayItem(BaseModel):
    schedule_id: UUID
    course_id: UUID
    planned_at: datetime
    course_data: str
    schedule_data: str
    status: str
    intake: ScheduleIntakeResponse | None


class ScheduleDayResponse(BaseModel):
    date: date
    items: list[ScheduleDayItem]
