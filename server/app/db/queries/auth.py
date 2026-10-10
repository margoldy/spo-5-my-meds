from datetime import datetime, timedelta, timezone
import hashlib

from sqlalchemy import and_, desc, select, update
from sqlalchemy.orm import Session

from app.db.models import AuthCode


class AuthQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_code(self, *, email: str, code: str, ttl_minutes: int = 5) -> AuthCode:
        now = datetime.now(timezone.utc)

        self.db.execute(
            update(AuthCode)
            .where(and_(AuthCode.email == email, AuthCode.used_at.is_(None)))
            .values(used_at=now)
        )

        row = AuthCode(
            email=email,
            code_hash=self._hash_code(code),
            expires_at=now + timedelta(minutes=ttl_minutes),
        )
        self.db.add(row)
        self.db.flush()
        return row

    def get_valid_code(self, *, email: str, code: str) -> AuthCode | None:
        now = datetime.now(timezone.utc)
        stmt = (
            select(AuthCode)
            .where(
                and_(
                    AuthCode.email == email,
                    AuthCode.code_hash == self._hash_code(code),
                    AuthCode.used_at.is_(None),
                    AuthCode.expires_at > now,
                )
            )
            .order_by(desc(AuthCode.created_at), desc(AuthCode.id))
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def use_code(self, row: AuthCode) -> None:
        row.used_at = datetime.now(timezone.utc)
        self.db.flush()

    @staticmethod
    def _hash_code(code: str) -> str:
        return hashlib.sha256(code.encode("utf-8")).hexdigest()
