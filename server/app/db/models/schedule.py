from datetime import time
from decimal import Decimal
import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, SmallInteger, String, Time
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Schedule(Base):
    __tablename__ = "schedules"
    __table_args__ = (
        CheckConstraint("cardinality(days_of_week) > 0", name="ck_schedules_days_not_empty"),
        CheckConstraint(
            "days_of_week <@ ARRAY[1, 2, 3, 4, 5, 6, 7]::smallint[]",
            name="ck_schedules_days_in_week_range",
        ),
        CheckConstraint("dose_amount > 0", name="ck_schedules_positive_dose"),
        CheckConstraint("btrim(dose_unit) <> ''", name="ck_schedules_dose_unit_not_empty"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    scheduled_at: Mapped[time] = mapped_column(Time, nullable=False)
    dose_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    dose_unit: Mapped[str] = mapped_column(String(50), nullable=False)
    days_of_week: Mapped[list[int]] = mapped_column(ARRAY(SmallInteger), nullable=False)

    course: Mapped["Course"] = relationship(back_populates="schedules")
    intakes: Mapped[list["Intake"]] = relationship(
        back_populates="schedule", passive_deletes=True
    )


Index("idx_schedules_course_id", Schedule.course_id)
