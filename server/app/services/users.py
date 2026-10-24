from sqlalchemy.orm import Session

from app.db.models import User
from app.db.queries.users import UsersQueries


class UsersService:
    def __init__(self, db: Session) -> None:
        self.q_u = UsersQueries(db)

    def update(self, *, user: User, values: dict) -> User:
        if values.get("timezone") is None:
            values.pop("timezone", None)
        return self.q_u.update(user=user, values=values)

    def get_encrypted_dek(self, *, user: User) -> str:
        if user.encrypted_dek is None:
            raise ValueError("Зашифрованный ключ ещё не сохранён")
        return user.encrypted_dek

    def set_encrypted_dek(self, *, user: User, encrypted_dek: str) -> str:
        self.q_u.set_encrypted_dek(user=user, encrypted_dek=encrypted_dek)
        return encrypted_dek
