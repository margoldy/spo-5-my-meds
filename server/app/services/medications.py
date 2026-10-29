from sqlalchemy.orm import Session

from app.db.models import Medication
from app.db.queries.medications import MedicationsQueries


class MedicationsService:
    def __init__(self, db: Session) -> None:
        self.q_m = MedicationsQueries(db)

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
        return self.q_m.get_all(
            search=search,
            category=category,
            form=form,
            limit=limit,
            offset=offset,
            include_inactive=include_inactive,
        )

    def get_by_id(
        self,
        *,
        medication_id: int,
        include_inactive: bool,
    ) -> Medication:
        medication = self.q_m.get_by_id(
            medication_id=medication_id,
            include_inactive=include_inactive,
        )
        if medication is None:
            raise LookupError("Лекарство не найдено")
        return medication

    def create(self, *, values: dict) -> Medication:
        return self.q_m.create(values=self._clean(values))

    def update(self, *, medication_id: int, values: dict) -> Medication:
        medication = self.get_by_id(
            medication_id=medication_id,
            include_inactive=True,
        )
        return self.q_m.update(
            medication=medication,
            values=self._clean(values),
        )

    @staticmethod
    def _clean(values: dict) -> dict:
        cleaned = values.copy()
        for field, value in cleaned.items():
            if isinstance(value, str):
                value = value.strip()
                cleaned[field] = value or None

        if "name" in cleaned and cleaned["name"] is None:
            raise ValueError("Название лекарства не может быть пустым")
        return cleaned
