from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class IntakeCreate(BaseModel):
    course_id: UUID | None = None
    schedule_id: UUID | None = None
    taken_at: datetime
    encrypted_data: str = Field(min_length=1, max_length=16384)

    @field_validator("encrypted_data")
    @classmethod
    def validate_encrypted_data(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Зашифрованные данные не могут быть пустыми")
        return value

    @model_validator(mode="after")
    def validate_links(self):
        if self.schedule_id is not None and self.course_id is None:
            raise ValueError("Расписание можно указать только вместе с курсом")
        if self.taken_at.utcoffset() is None:
            raise ValueError("Время приёма должно содержать часовой пояс")
        return self


class IntakeUpdate(BaseModel):
    taken_at: datetime | None = None
    encrypted_data: str | None = Field(default=None, min_length=1, max_length=16384)

    @field_validator("encrypted_data")
    @classmethod
    def validate_encrypted_data(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Зашифрованные данные не могут быть пустыми")
        return value

    @model_validator(mode="after")
    def validate_time(self):
        if "taken_at" in self.model_fields_set and self.taken_at is None:
            raise ValueError("Время приёма не может быть пустым")
        if "encrypted_data" in self.model_fields_set and self.encrypted_data is None:
            raise ValueError("Зашифрованные данные не могут быть пустыми")
        if self.taken_at is not None and self.taken_at.utcoffset() is None:
            raise ValueError("Время приёма должно содержать часовой пояс")
        return self


class IntakeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    course_id: UUID | None
    schedule_id: UUID | None
    taken_at: datetime
    encrypted_data: str


class IntakeListResponse(BaseModel):
    items: list[IntakeResponse]
