from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import (
    AuthCodeRequest,
    AuthCodeVerifyRequest,
    AuthMessageResponse,
    AuthVerifyResponse,
)
from app.schemas.users import UserMeResponse
from app.services.auth import AuthService


router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/code/request", response_model=AuthMessageResponse)
def request_code(
    body: AuthCodeRequest,
    db: Session = Depends(get_db),
) -> AuthMessageResponse:
    try:
        AuthService(db).request_code(email=str(body.email))
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Не удалось отправить код",
        ) from error

    return AuthMessageResponse(message="Код отправлен на email")


@router.post("/code/verify", response_model=AuthVerifyResponse)
def verify_code(
    body: AuthCodeVerifyRequest,
    db: Session = Depends(get_db),
) -> AuthVerifyResponse:
    try:
        access_token, user = AuthService(db).verify_code(
            email=str(body.email),
            code=body.code,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    return AuthVerifyResponse(
        access_token=access_token,
        user=UserMeResponse.model_validate(user),
    )
