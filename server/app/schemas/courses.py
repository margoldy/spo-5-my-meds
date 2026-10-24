from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.schemas.schedules import ScheduleResponse


class CourseCreate(BaseModel):
    start_date: date
    end_date: date | None = None
    encrypted_data: str = Field(min_length=1, max_length=16384)

    @field_validator("encrypted_data")
    @classmethod
    def validate_encrypted_data(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Зашифрованные данные не могут быть пустыми")
        return value

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("Дата окончания не может быть раньше даты начала")
        return self


class CourseUpdate(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None
    encrypted_data: str | None = Field(default=None, min_length=1, max_length=16384)

    @model_validator(mode="after")
    def validate_required_values(self):
        if "start_date" in self.model_fields_set and self.start_date is None:
            raise ValueError("Дата начала не может быть пустой")
        if "encrypted_data" in self.model_fields_set and self.encrypted_data is None:
            raise ValueError("Зашифрованные данные не могут быть пустыми")
        if "is_active" in self.model_fields_set and self.is_active is None:
            raise ValueError("Состояние курса не может быть пустым")
        return self

    @field_validator("encrypted_data")
    @classmethod
    def validate_encrypted_data(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Зашифрованные данные не могут быть пустыми")
        return value


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    start_date: date
    end_date: date | None
    is_active: bool
    encrypted_data: str
    taking_mode: str
    schedules: list[ScheduleResponse]
    created_at: datetime


class CourseListResponse(BaseModel):
    items: list[CourseResponse]
