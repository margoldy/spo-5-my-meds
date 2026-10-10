from datetime import datetime, timedelta, timezone
import os
from uuid import UUID

from dotenv import load_dotenv
from jose import JWTError, jwt


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def _secret_key() -> str:
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not set")
    return SECRET_KEY


def create_access_token(user_id: UUID) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, _secret_key(), algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, _secret_key(), algorithms=[ALGORITHM])


def validate_access_token(token: str) -> UUID:
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise JWTError("Invalid token type")

    subject = payload.get("sub")
    if not subject:
        raise JWTError("Token payload is incomplete")

    try:
        return UUID(subject)
    except ValueError as error:
        raise JWTError("Invalid token payload") from error
