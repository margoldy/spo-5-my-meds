from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse


router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/code/request", response_class=PlainTextResponse)
def request_code(body: dict = Body(...)):
    return "Код отправлен на email"


@router.post("/code/verify", response_class=PlainTextResponse)
def verify_code(body: dict = Body(...)):
    return "Код подтверждён, пользователь авторизован"
