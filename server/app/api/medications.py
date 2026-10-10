from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse


router = APIRouter(prefix="/api/v1/medications", tags=["Medications"])


@router.get("", response_class=PlainTextResponse)
def get_medications(
    search: str | None = None,
    category: str | None = None,
    form: str | None = None,
    limit: int = 20,
    offset: int = 0,
):
    return "Список лекарств получен"


@router.get("/{medication_id}", response_class=PlainTextResponse)
def get_medication(medication_id: int):
    return "Лекарство получено"


@router.post("", response_class=PlainTextResponse, status_code=201)
def create_medication(body: dict = Body(...)):
    return "Лекарство добавлено"


@router.patch("/{medication_id}", response_class=PlainTextResponse)
def update_medication(medication_id: int, body: dict = Body(...)):
    return "Лекарство обновлено"
