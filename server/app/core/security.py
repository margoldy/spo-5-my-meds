from datetime import datetime, timedelta, timezone
import os
from uuid import UUID

from dotenv import load_dotenv
from jose import JWTError, jwt


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30


def _secret_key() -> str:
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not set")
    return SECRET_KEY


def _create_token(user_id: UUID, token_type: str, expires_at: datetime) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    return jwt.encode(payload, _secret_key(), algorithm=ALGORITHM)


def create_access_token(user_id: UUID) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return _create_token(user_id, "access", expires_at)


def create_refresh_token(user_id: UUID) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    return _create_token(user_id, "refresh", expires_at)


def decode_token(token: str) -> dict:
    return jwt.decode(token, _secret_key(), algorithms=[ALGORITHM])


def validate_access_token(token: str) -> UUID:
    return _validate_token(token, "access")


def validate_refresh_token(token: str) -> UUID:
    return _validate_token(token, "refresh")


def _validate_token(token: str, expected_type: str) -> UUID:
    payload = decode_token(token)

    if payload.get("type") != expected_type:
        raise JWTError("Invalid token type")

    subject = payload.get("sub")
    if not subject:
        raise JWTError("Token payload is incomplete")

    try:
        return UUID(subject)
    except ValueError as error:
        raise JWTError("Invalid token payload") from error
