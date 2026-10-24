from datetime import date, datetime
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.db.models import UserRole


class UserMeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str | None
    email: EmailStr
    birth_date: date | None
    role: UserRole
    avatar_url: str | None
    timezone: str
    created_at: datetime


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    birth_date: date | None = None
    avatar_url: str | None = Field(default=None, max_length=2048)
    timezone: str | None = Field(default=None, max_length=64)

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str | None) -> str | None:
        if value is None:
            return value

        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as error:
            raise ValueError("Неизвестный часовой пояс") from error

        return value


class EncryptedKeyRequest(BaseModel):
    encrypted_dek: str = Field(min_length=1, max_length=16384)

    @field_validator("encrypted_dek")
    @classmethod
    def validate_encrypted_dek(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Зашифрованный ключ не может быть пустым")
        return value


class EncryptedKeyResponse(BaseModel):
    encrypted_dek: str
