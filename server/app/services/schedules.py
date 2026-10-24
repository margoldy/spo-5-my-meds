from datetime import date, datetime, time, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.db.models import Schedule, User
from app.db.queries.courses import CoursesQueries
from app.db.queries.intakes import IntakesQueries
from app.db.queries.schedules import SchedulesQueries
from app.schemas.schedules import (
    ScheduleDayItem,
    ScheduleIntakeResponse,
)


class SchedulesService:
    def __init__(self, db: Session) -> None:
        self.q_c = CoursesQueries(db)
        self.q_i = IntakesQueries(db)
        self.q_s = SchedulesQueries(db)

    def get_for_course(
        self,
        *,
        current_user: User,
        course_id: UUID,
    ) -> list[Schedule]:
        if self.q_c.get_by_id(
            course_id=course_id,
            user_id=current_user.id,
        ) is None:
            raise LookupError("Курс не найден")
        return self.q_s.get_for_course(
            course_id=course_id,
            user_id=current_user.id,
        )

    def get_by_id(
        self,
        *,
        current_user: User,
        schedule_id: UUID,
    ) -> Schedule:
        schedule = self.q_s.get_by_id(
            schedule_id=schedule_id,
            user_id=current_user.id,
        )
        if schedule is None:
            raise LookupError("Расписание не найдено")
        return schedule

    def create(
        self,
        *,
        current_user: User,
        course_id: UUID,
        scheduled_at: time,
        days_of_week: list[int],
        encrypted_data: str,
    ) -> Schedule:
        if current_user.encrypted_dek is None:
            raise ValueError("Сначала сохраните ключ шифрования")

        course = self.q_c.get_by_id(
            course_id=course_id,
            user_id=current_user.id,
        )
        if course is None:
            raise LookupError("Курс не найден")
        if not course.is_active:
            raise ValueError("Нельзя добавить расписание в завершённый курс")

        return self.q_s.create(
            course_id=course.id,
            scheduled_at=scheduled_at,
            days_of_week=days_of_week,
            encrypted_data=encrypted_data,
        )

    def update(
        self,
        *,
        current_user: User,
        schedule_id: UUID,
        values: dict,
    ) -> Schedule:
        schedule = self.get_by_id(
            current_user=current_user,
            schedule_id=schedule_id,
        )
        if not schedule.course.is_active:
            raise ValueError("Нельзя изменить расписание завершённого курса")
        if "encrypted_data" in values and current_user.encrypted_dek is None:
            raise ValueError("Сначала сохраните ключ шифрования")
        return self.q_s.update(schedule=schedule, values=values)

    def delete(self, *, current_user: User, schedule_id: UUID) -> None:
        schedule = self.get_by_id(
            current_user=current_user,
            schedule_id=schedule_id,
        )
        self.q_s.delete(schedule=schedule)

    def get_for_day(
        self,
        *,
        current_user: User,
        day: date,
    ) -> list[ScheduleDayItem]:
        timezone = ZoneInfo(current_user.timezone)
        day_start = datetime.combine(day, datetime.min.time(), timezone)
        day_end = day_start + timedelta(days=1)
        schedules = self.q_s.get_for_day(user_id=current_user.id, day=day)
        intakes = self.q_i.get_between(
            user_id=current_user.id,
            from_=day_start,
            to=day_end,
        )
        intakes_by_schedule = {
            intake.schedule_id: intake
            for intake in intakes
            if intake.schedule_id is not None
        }

        items = []
        for schedule in schedules:
            intake = intakes_by_schedule.get(schedule.id)
            intake_response = None
            if intake is not None:
                intake_response = ScheduleIntakeResponse(
                    id=intake.id,
                    taken_at=intake.taken_at,
                    encrypted_data=intake.encrypted_data,
                )

            items.append(
                ScheduleDayItem(
                    schedule_id=schedule.id,
                    course_id=schedule.course_id,
                    planned_at=datetime.combine(
                        day,
                        schedule.scheduled_at,
                        timezone,
                    ),
                    course_data=schedule.course.encrypted_data,
                    schedule_data=schedule.encrypted_data,
                    status="taken" if intake is not None else "pending",
                    intake=intake_response,
                )
            )

        return items
