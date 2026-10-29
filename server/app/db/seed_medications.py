import json
from pathlib import Path

from app.db.models import Medication
from app.db.session import SessionLocal


DATA_FILE = Path(__file__).with_name("medications.json")


def medication_key(name: str, form: str | None, strength: str | None):
    return name.casefold(), (form or "").casefold(), (strength or "").casefold()


def seed_medications():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    with SessionLocal.begin() as db:
        existing = {
            medication_key(name, form, strength)
            for name, form, strength in db.query(
                Medication.name,
                Medication.form,
                Medication.strength,
            ).all()
        }
        medications = [
            Medication(**item)
            for item in data["items"]
            if medication_key(
                item["name"],
                item.get("form"),
                item.get("strength"),
            ) not in existing
        ]
        db.add_all(medications)

    return len(medications)
