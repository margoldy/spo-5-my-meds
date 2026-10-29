from sqlalchemy import case, func, or_, select
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
        search_term = search.strip() if search else ""
        relevance = None
        if search_term:
            pattern = f"%{search_term}%"
            starts_with = f"{search_term}%"
            filters.append(
                or_(
                    Medication.name.ilike(pattern),
                    Medication.international_name.ilike(pattern),
                    Medication.manufacturer.ilike(pattern),
                )
            )
            relevance = case(
                (func.lower(Medication.name) == search_term.lower(), 0),
                (Medication.name.ilike(starts_with), 1),
                (Medication.name.ilike(pattern), 2),
                (
                    func.lower(Medication.international_name)
                    == search_term.lower(),
                    3,
                ),
                (Medication.international_name.ilike(starts_with), 4),
                (Medication.international_name.ilike(pattern), 5),
                else_=6,
            )
        if category:
            filters.append(Medication.category == category)
        if form:
            filters.append(Medication.form == form)

        query = select(Medication).where(*filters)
        if relevance is not None:
            query = query.order_by(relevance, Medication.name)
        else:
            query = query.order_by(Medication.name)

        items = self.db.execute(query.limit(limit).offset(offset)).scalars().all()

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
