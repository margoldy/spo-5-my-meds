from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.db.models import Medication


class MedicationsQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self,
        *,
        search: str | None,
        category: str | None,
        form: str | None,
        limit: int,
        offset: int,
        include_inactive: bool,
    ) -> tuple[list[Medication], int]:
        filters = []

        if not include_inactive:
            filters.append(Medication.is_active.is_(True))
        if search:
            pattern = f"%{search.strip()}%"
            filters.append(
                or_(
                    Medication.name.ilike(pattern),
                    Medication.international_name.ilike(pattern),
                    Medication.manufacturer.ilike(pattern),
                )
            )
        if category:
            filters.append(Medication.category == category)
        if form:
            filters.append(Medication.form == form)

        items = self.db.execute(
            select(Medication)
            .where(*filters)
            .order_by(Medication.name)
            .limit(limit)
            .offset(offset)
        ).scalars().all()

        total = self.db.execute(
            select(func.count()).select_from(Medication).where(*filters)
        ).scalar_one()

        return list(items), total

    def get_by_id(
        self,
        *,
        medication_id: int,
        include_inactive: bool,
    ) -> Medication | None:
        filters = [Medication.id == medication_id]
        if not include_inactive:
            filters.append(Medication.is_active.is_(True))

        return self.db.execute(
            select(Medication).where(*filters).limit(1)
        ).scalar_one_or_none()

    def create(self, *, values: dict) -> Medication:
        medication = Medication(**values)
        self.db.add(medication)
        self.db.flush()
        self.db.refresh(medication)
        return medication

    def update(self, *, medication: Medication, values: dict) -> Medication:
        for field, value in values.items():
            setattr(medication, field, value)

        self.db.flush()
        self.db.refresh(medication)
        return medication
