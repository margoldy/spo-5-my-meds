from fastapi import APIRouter, Body, Query
from fastapi.responses import PlainTextResponse


router = APIRouter(prefix="/api/v1", tags=["Schedules"])


@router.get("/courses/{course_id}/schedules", response_class=PlainTextResponse)
def get_course_schedules(course_id: str):
    return "Расписания курса получены"


@router.post(
    "/courses/{course_id}/schedules",
    response_class=PlainTextResponse,
    status_code=201,
)
def create_schedule(course_id: str, body: dict = Body(...)):
    return "Расписание добавлено"


@router.patch("/schedules/{schedule_id}", response_class=PlainTextResponse)
def update_schedule(schedule_id: str, body: dict = Body(...)):
    return "Расписание обновлено"


@router.delete("/schedules/{schedule_id}", response_class=PlainTextResponse)
def delete_schedule(schedule_id: str):
    return "Расписание удалено"


@router.get("/schedules", response_class=PlainTextResponse)
def get_schedules(date: str = Query(...)):
    return "Расписание на выбранный день получено"
