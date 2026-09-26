from datetime import date, datetime
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Course(Base):
    __tablename__ = "courses"
    __table_args__ = (
        CheckConstraint(
            "(medication_id IS NULL) <> (custom_name IS NULL)",
            name="ck_courses_exactly_one_name_source",
        ),
        CheckConstraint(
            "end_date IS NULL OR end_date >= start_date",
            name="ck_courses_valid_date_range",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    custom_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    medication_id: Mapped[int | None] = mapped_column(
        ForeignKey("medications.id", ondelete="SET NULL"),
        nullable=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(back_populates="courses")
    medication: Mapped["Medication | None"] = relationship(back_populates="courses")
    schedules: Mapped[list["Schedule"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    intakes: Mapped[list["Intake"]] = relationship(
        back_populates="course",
        passive_deletes=True,
    )


Index("idx_courses_user_id", Course.user_id)
Index("idx_courses_medication_id", Course.medication_id)
