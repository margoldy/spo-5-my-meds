from fastapi import APIRouter, Body, Query
from fastapi.responses import PlainTextResponse


router = APIRouter(prefix="/api/v1/intakes", tags=["Intakes"])


@router.post("", response_class=PlainTextResponse, status_code=201)
def create_intake(body: dict = Body(...)):
    return "Приём лекарства записан"


@router.get("", response_class=PlainTextResponse)
def get_intakes(
    course_id: str | None = None,
    from_: str | None = Query(default=None, alias="from"),
    to: str | None = None,
):
    return "История приёмов получена"


@router.patch("/{intake_id}", response_class=PlainTextResponse)
def update_intake(intake_id: str, body: dict = Body(...)):
    return "Приём лекарства обновлён"


@router.delete("/{intake_id}", response_class=PlainTextResponse)
def delete_intake(intake_id: str):
    return "Приём лекарства удалён"
