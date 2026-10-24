from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User, UserRole


class UsersQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, *, user_id: UUID) -> User | None:
        return self.db.execute(
            select(User).where(User.id == user_id).limit(1)
        ).scalar_one_or_none()

    def get_by_email(self, *, email: str) -> User | None:
        return self.db.execute(
            select(User).where(User.email == email).limit(1)
        ).scalar_one_or_none()

    def create(self, *, email: str, role: UserRole = UserRole.USER) -> User:
        user = User(email=email, role=role)
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user

    def update(self, *, user: User, values: dict) -> User:
        for field, value in values.items():
            setattr(user, field, value)

        self.db.flush()
        self.db.refresh(user)
        return user

    def set_encrypted_dek(self, *, user: User, encrypted_dek: str) -> User:
        user.encrypted_dek = encrypted_dek
        self.db.flush()
        return user
