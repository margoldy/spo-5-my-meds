from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import Course, User
from app.db.queries.courses import CoursesQueries


class CoursesService:
    def __init__(self, db: Session) -> None:
        self.q_c = CoursesQueries(db)

    def get_all(self, *, current_user: User) -> list[Course]:
        return self.q_c.get_all(user_id=current_user.id)

    def get_by_id(self, *, current_user: User, course_id: UUID) -> Course:
        course = self.q_c.get_by_id(
            course_id=course_id,
            user_id=current_user.id,
        )
        if course is None:
            raise LookupError("Курс не найден")
        return course

    def create(
        self,
        *,
        current_user: User,
        start_date: date,
        end_date: date | None,
        encrypted_data: str,
    ) -> Course:
        if current_user.encrypted_dek is None:
            raise ValueError("Сначала сохраните ключ шифрования")

        return self.q_c.create(
            user_id=current_user.id,
            start_date=start_date,
            end_date=end_date,
            encrypted_data=encrypted_data,
        )

    def update(
        self,
        *,
        current_user: User,
        course_id: UUID,
        values: dict,
    ) -> Course:
        course = self.get_by_id(
            current_user=current_user,
            course_id=course_id,
        )
        if "encrypted_data" in values and current_user.encrypted_dek is None:
            raise ValueError("Сначала сохраните ключ шифрования")

        start_date = values.get("start_date", course.start_date)
        end_date = values.get("end_date", course.end_date)

        if end_date is not None and end_date < start_date:
            raise ValueError("Дата окончания не может быть раньше даты начала")

        return self.q_c.update(course=course, values=values)

    def delete(self, *, current_user: User, course_id: UUID) -> None:
        course = self.get_by_id(
            current_user=current_user,
            course_id=course_id,
        )
        self.q_c.delete(course=course)
