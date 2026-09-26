from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Intake(Base):
    __tablename__ = "intakes"
    __table_args__ = (
        CheckConstraint("dose_amount > 0", name="ck_intakes_positive_dose"),
        CheckConstraint("btrim(dose_unit) <> ''", name="ck_intakes_dose_unit_not_empty"),
        CheckConstraint(
            "btrim(medication_name) <> ''",
            name="ck_intakes_medication_name_not_empty",
        ),
        CheckConstraint(
            "schedule_id IS NULL OR course_id IS NOT NULL",
            name="ck_intakes_schedule_requires_course",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    course_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("courses.id", ondelete="SET NULL"), nullable=True
    )
    schedule_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("schedules.id", ondelete="SET NULL"), nullable=True
    )
    taken_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    dose_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    dose_unit: Mapped[str] = mapped_column(String(50), nullable=False)
    medication_name: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["User"] = relationship(back_populates="intakes")
    course: Mapped["Course | None"] = relationship(back_populates="intakes")
    schedule: Mapped["Schedule | None"] = relationship(back_populates="intakes")


Index("idx_intakes_user_id", Intake.user_id)
Index("idx_intakes_course_id", Intake.course_id)
Index("idx_intakes_schedule_id", Intake.schedule_id)
Index("idx_intakes_taken_at", Intake.taken_at)
