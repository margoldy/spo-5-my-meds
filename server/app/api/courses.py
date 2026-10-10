from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse


router = APIRouter(prefix="/api/v1/courses", tags=["Courses"])


@router.get("", response_class=PlainTextResponse)
def get_courses():
    return "Список курсов получен"


@router.post("", response_class=PlainTextResponse, status_code=201)
def create_course(body: dict = Body(...)):
    return "Курс добавлен"


@router.get("/{course_id}", response_class=PlainTextResponse)
def get_course(course_id: str):
    return "Курс получен"


@router.patch("/{course_id}", response_class=PlainTextResponse)
def update_course(course_id: str, body: dict = Body(...)):
    return "Курс обновлён"


@router.delete("/{course_id}", response_class=PlainTextResponse)
def delete_course(course_id: str):
    return "Курс удалён"
