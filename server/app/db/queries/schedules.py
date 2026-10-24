from datetime import date, time
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.db.models import Course, Schedule


class SchedulesQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_for_course(self, *, course_id: UUID, user_id: UUID) -> list[Schedule]:
        rows = self.db.execute(
            select(Schedule)
            .join(Course)
            .where(Schedule.course_id == course_id, Course.user_id == user_id)
            .order_by(Schedule.scheduled_at)
        ).scalars().all()
        return list(rows)

    def get_by_id(self, *, schedule_id: UUID, user_id: UUID) -> Schedule | None:
        return self.db.execute(
            select(Schedule)
            .join(Course)
            .where(Schedule.id == schedule_id, Course.user_id == user_id)
            .options(joinedload(Schedule.course))
            .limit(1)
        ).scalar_one_or_none()

    def get_for_day(self, *, user_id: UUID, day: date) -> list[Schedule]:
        rows = self.db.execute(
            select(Schedule)
            .join(Course)
            .where(
                Course.user_id == user_id,
                Course.is_active.is_(True),
                Course.start_date <= day,
                or_(Course.end_date.is_(None), Course.end_date >= day),
                Schedule.days_of_week.contains([day.isoweekday()]),
            )
            .options(joinedload(Schedule.course))
            .order_by(Schedule.scheduled_at)
        ).scalars().all()
        return list(rows)

    def create(
        self,
        *,
        course_id: UUID,
        scheduled_at: time,
        days_of_week: list[int],
        encrypted_data: str,
    ) -> Schedule:
        schedule = Schedule(
            course_id=course_id,
            scheduled_at=scheduled_at,
            days_of_week=days_of_week,
            encrypted_data=encrypted_data,
        )
        self.db.add(schedule)
        self.db.flush()
        self.db.refresh(schedule)
        return schedule

    def update(self, *, schedule: Schedule, values: dict) -> Schedule:
        for field, value in values.items():
            setattr(schedule, field, value)

        self.db.flush()
        self.db.refresh(schedule)
        return schedule

    def delete(self, *, schedule: Schedule) -> None:
        self.db.delete(schedule)
        self.db.flush()
