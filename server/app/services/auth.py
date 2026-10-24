import secrets
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    validate_refresh_token,
)
from app.core.send_code import send_auth_code
from app.db.models import User
from app.db.queries.auth import AuthQueries
from app.db.queries.users import UsersQueries


mail_sender = send_auth_code


def generate_code() -> str:
    return f"{secrets.randbelow(900_000) + 100_000:06d}"


class AuthService:
    def __init__(self, db: Session) -> None:
        self.q_a = AuthQueries(db)
        self.q_u = UsersQueries(db)

    def request_code(self, *, email: str) -> None:
        normalized_email = email.strip().lower()
        latest = self.q_a.get_latest_active(email=normalized_email)
        if latest is not None:
            seconds = (datetime.now(timezone.utc) - latest.created_at).total_seconds()
            if seconds < 60:
                raise ValueError("Повторный код можно запросить через минуту")

        code = generate_code()
        self.q_a.create_code(email=normalized_email, code=code)
        mail_sender(normalized_email, code)

    def verify_code(self, *, email: str, code: str) -> tuple[str, str, User]:
        normalized_email = email.strip().lower()
        row = self.q_a.get_latest_active(email=normalized_email)
        if row is None or not self.q_a.code_matches(row=row, code=code):
            if row is not None:
                self.q_a.add_failed_attempt(row=row)
            raise ValueError("Неверный или просроченный код")

        self.q_a.use_code(row=row)

        user = self.q_u.get_by_email(email=normalized_email)
        if user is None:
            user = self.q_u.create(email=normalized_email)

        return create_access_token(user.id), create_refresh_token(user.id), user

    def refresh_access_token(self, *, refresh_token: str) -> str:
        user_id = validate_refresh_token(refresh_token)
        user = self.q_u.get_by_id(user_id=user_id)
        if user is None:
            raise ValueError("Пользователь не найден")

        return create_access_token(user.id)
