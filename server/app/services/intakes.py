from datetime import datetime, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.db.models import Course, Intake, User
from app.db.queries.courses import CoursesQueries
from app.db.queries.intakes import IntakesQueries
from app.db.queries.schedules import SchedulesQueries


class IntakesService:
    def __init__(self, db: Session) -> None:
        self.q_c = CoursesQueries(db)
        self.q_i = IntakesQueries(db)
        self.q_s = SchedulesQueries(db)

    def get_all(
        self,
        *,
        current_user: User,
        course_id: UUID | None,
        from_: datetime | None,
        to: datetime | None,
    ) -> list[Intake]:
        if from_ is not None and from_.utcoffset() is None:
            raise ValueError("Параметр from должен содержать часовой пояс")
        if to is not None and to.utcoffset() is None:
            raise ValueError("Параметр to должен содержать часовой пояс")
        if from_ is not None and to is not None and to < from_:
            raise ValueError("Параметр to не может быть раньше from")

        return self.q_i.get_all(
            user_id=current_user.id,
            course_id=course_id,
            from_=from_,
            to=to,
        )

    def get_by_id(
        self,
        *,
        current_user: User,
        intake_id: UUID,
    ) -> Intake:
        intake = self.q_i.get_by_id(
            intake_id=intake_id,
            user_id=current_user.id,
        )
        if intake is None:
            raise LookupError("Приём не найден")
        return intake

    def create(
        self,
        *,
        current_user: User,
        course_id: UUID | None,
        schedule_id: UUID | None,
        taken_at: datetime,
        encrypted_data: str,
    ) -> Intake:
        if current_user.encrypted_dek is None:
            raise ValueError("Сначала сохраните ключ шифрования")

        course = None
        if course_id is not None:
            course = self.q_c.get_by_id(
                course_id=course_id,
                user_id=current_user.id,
            )
            if course is None:
                raise LookupError("Курс не найден")

        if schedule_id is not None:
            schedule = self.q_s.get_by_id(
                schedule_id=schedule_id,
                user_id=current_user.id,
            )
            if schedule is None:
                raise LookupError("Расписание не найдено")
            if schedule.course_id != course_id:
                raise ValueError("Расписание не относится к указанному курсу")
            self._check_duplicate(
                current_user=current_user,
                schedule_id=schedule_id,
                taken_at=taken_at,
            )

        self._check_course_date(
            current_user=current_user,
            course=course,
            taken_at=taken_at,
        )

        return self.q_i.create(
            user_id=current_user.id,
            values={
                "course_id": course_id,
                "schedule_id": schedule_id,
                "taken_at": taken_at,
                "encrypted_data": encrypted_data,
            },
        )

    def update(
        self,
        *,
        current_user: User,
        intake_id: UUID,
        values: dict,
    ) -> Intake:
        intake = self.get_by_id(
            current_user=current_user,
            intake_id=intake_id,
        )
        if "encrypted_data" in values and current_user.encrypted_dek is None:
            raise ValueError("Сначала сохраните ключ шифрования")

        taken_at = values.get("taken_at", intake.taken_at)
        course = None
        if intake.course_id is not None:
            course = self.q_c.get_by_id(
                course_id=intake.course_id,
                user_id=current_user.id,
            )

        self._check_course_date(
            current_user=current_user,
            course=course,
            taken_at=taken_at,
        )
        if intake.schedule_id is not None and "taken_at" in values:
            self._check_duplicate(
                current_user=current_user,
                schedule_id=intake.schedule_id,
                taken_at=taken_at,
                exclude_id=intake.id,
            )

        return self.q_i.update(intake=intake, values=values)

    def delete(self, *, current_user: User, intake_id: UUID) -> None:
        intake = self.get_by_id(
            current_user=current_user,
            intake_id=intake_id,
        )
        self.q_i.delete(intake=intake)

    def _check_duplicate(
        self,
        *,
        current_user: User,
        schedule_id: UUID,
        taken_at: datetime,
        exclude_id: UUID | None = None,
    ) -> None:
        timezone = ZoneInfo(current_user.timezone)
        local_time = taken_at.astimezone(timezone)
        day_start = local_time.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        existing = self.q_i.get_for_schedule_between(
            user_id=current_user.id,
            schedule_id=schedule_id,
            from_=day_start,
            to=day_end,
            exclude_id=exclude_id,
        )
        if existing is not None:
            raise ValueError("Этот плановый приём уже записан")

    @staticmethod
    def _check_course_date(
        *,
        current_user: User,
        course: Course | None,
        taken_at: datetime,
    ) -> None:
        if course is None:
            return

        local_date = taken_at.astimezone(ZoneInfo(current_user.timezone)).date()
        if local_date < course.start_date:
            raise ValueError("Дата приёма находится вне периода курса")
        if course.end_date is not None and local_date > course.end_date:
            raise ValueError("Дата приёма находится вне периода курса")
