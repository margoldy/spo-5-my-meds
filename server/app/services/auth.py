import secrets

from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.core.send_code import send_auth_code
from app.db.models import User
from app.db.queries.auth import AuthQueries
from app.db.queries.users import UsersQueries


mail_sender = send_auth_code


def generate_code() -> str:
    return f"{secrets.randbelow(900_000) + 100_000:06d}"


class AuthService:
    def __init__(self, db: Session) -> None:
        self.auth_queries = AuthQueries(db)
        self.users_queries = UsersQueries(db)

    def request_code(self, *, email: str) -> None:
        normalized_email = email.strip().lower()
        code = generate_code()
        self.auth_queries.create_code(email=normalized_email, code=code)
        mail_sender(normalized_email, code)

    def verify_code(self, *, email: str, code: str) -> tuple[str, User]:
        normalized_email = email.strip().lower()
        row = self.auth_queries.get_valid_code(email=normalized_email, code=code)
        if row is None:
            raise ValueError("Неверный или просроченный код")

        self.auth_queries.use_code(row)

        user = self.users_queries.get_by_email(normalized_email)
        if user is None:
            user = self.users_queries.create(email=normalized_email)

        return create_access_token(user.id), user
