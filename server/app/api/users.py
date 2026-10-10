from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse


router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/me", response_class=PlainTextResponse)
def get_me():
    return "Профиль пользователя получен"


@router.patch("/me", response_class=PlainTextResponse)
def update_me(body: dict = Body(...)):
    return "Профиль пользователя обновлён"
