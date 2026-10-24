from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Course


class CoursesQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, *, user_id: UUID) -> list[Course]:
        rows = self.db.execute(
            select(Course)
            .where(Course.user_id == user_id)
            .options(selectinload(Course.schedules))
            .order_by(Course.is_active.desc(), Course.start_date.desc())
        ).scalars().all()
        return list(rows)

    def get_by_id(self, *, course_id: UUID, user_id: UUID) -> Course | None:
        return self.db.execute(
            select(Course)
            .where(Course.id == course_id, Course.user_id == user_id)
            .options(selectinload(Course.schedules))
            .limit(1)
        ).scalar_one_or_none()

    def create(
        self,
        *,
        user_id: UUID,
        start_date: date,
        end_date: date | None,
        encrypted_data: str,
    ) -> Course:
        course = Course(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            encrypted_data=encrypted_data,
        )
        self.db.add(course)
        self.db.flush()
        self.db.refresh(course)
        return course

    def update(self, *, course: Course, values: dict) -> Course:
        for field, value in values.items():
            setattr(course, field, value)

        self.db.flush()
        return course

    def delete(self, *, course: Course) -> None:
        self.db.delete(course)
        self.db.flush()
