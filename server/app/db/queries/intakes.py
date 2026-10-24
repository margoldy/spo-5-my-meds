from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Intake


class IntakesQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self,
        *,
        user_id: UUID,
        course_id: UUID | None,
        from_: datetime | None,
        to: datetime | None,
    ) -> list[Intake]:
        filters = [Intake.user_id == user_id]
        if course_id is not None:
            filters.append(Intake.course_id == course_id)
        if from_ is not None:
            filters.append(Intake.taken_at >= from_)
        if to is not None:
            filters.append(Intake.taken_at <= to)

        rows = self.db.execute(
            select(Intake)
            .where(*filters)
            .order_by(Intake.taken_at.desc())
        ).scalars().all()
        return list(rows)

    def get_by_id(self, *, intake_id: UUID, user_id: UUID) -> Intake | None:
        return self.db.execute(
            select(Intake)
            .where(Intake.id == intake_id, Intake.user_id == user_id)
            .limit(1)
        ).scalar_one_or_none()

    def get_between(
        self,
        *,
        user_id: UUID,
        from_: datetime,
        to: datetime,
    ) -> list[Intake]:
        rows = self.db.execute(
            select(Intake)
            .where(
                Intake.user_id == user_id,
                Intake.taken_at >= from_,
                Intake.taken_at < to,
                Intake.schedule_id.is_not(None),
            )
            .order_by(Intake.taken_at)
        ).scalars().all()
        return list(rows)

    def get_for_schedule_between(
        self,
        *,
        user_id: UUID,
        schedule_id: UUID,
        from_: datetime,
        to: datetime,
        exclude_id: UUID | None = None,
    ) -> Intake | None:
        filters = [
            Intake.user_id == user_id,
            Intake.schedule_id == schedule_id,
            Intake.taken_at >= from_,
            Intake.taken_at < to,
        ]
        if exclude_id is not None:
            filters.append(Intake.id != exclude_id)

        return self.db.execute(
            select(Intake).where(*filters).limit(1)
        ).scalar_one_or_none()

    def create(self, *, user_id: UUID, values: dict) -> Intake:
        intake = Intake(user_id=user_id, **values)
        self.db.add(intake)
        self.db.flush()
        self.db.refresh(intake)
        return intake

    def update(self, *, intake: Intake, values: dict) -> Intake:
        for field, value in values.items():
            setattr(intake, field, value)

        self.db.flush()
        self.db.refresh(intake)
        return intake

    def delete(self, *, intake: Intake) -> None:
        self.db.delete(intake)
        self.db.flush()
