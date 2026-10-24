from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import (
    AuthAccessTokenResponse,
    AuthCodeRequest,
    AuthCodeVerifyRequest,
    AuthMessageResponse,
    AuthRefreshRequest,
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
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(error),
        ) from error
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
        access_token, refresh_token, user = AuthService(db).verify_code(
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
        refresh_token=refresh_token,
        user=UserMeResponse.model_validate(user),
    )


@router.post("/token/refresh", response_model=AuthAccessTokenResponse)
def refresh_access_token(
    body: AuthRefreshRequest,
    db: Session = Depends(get_db),
) -> AuthAccessTokenResponse:
    try:
        access_token = AuthService(db).refresh_access_token(
            refresh_token=body.refresh_token,
        )
    except (ValueError, JWTError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный или просроченный refresh-токен",
        ) from error

    return AuthAccessTokenResponse(access_token=access_token)
