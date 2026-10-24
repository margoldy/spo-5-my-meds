from datetime import datetime
import uuid

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Intake(Base):
    __tablename__ = "intakes"
    __table_args__ = (
        CheckConstraint(
            "schedule_id IS NULL OR course_id IS NOT NULL",
            name="ck_intake_schedule",
        ),
        CheckConstraint("btrim(encrypted_data) <> ''", name="ck_intake_data"),
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
    encrypted_data: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship(back_populates="intakes")
    course: Mapped["Course | None"] = relationship(back_populates="intakes")
    schedule: Mapped["Schedule | None"] = relationship(back_populates="intakes")


Index("idx_intakes_user_id", Intake.user_id)
Index("idx_intakes_course_id", Intake.course_id)
Index("idx_intakes_schedule_id", Intake.schedule_id)
Index("idx_intakes_taken_at", Intake.taken_at)
