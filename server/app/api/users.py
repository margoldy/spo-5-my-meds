from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.users import (
    EncryptedKeyRequest,
    EncryptedKeyResponse,
    UserMeResponse,
    UserUpdate,
)
from app.services.users import UsersService


router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/me", response_model=UserMeResponse)
def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.patch("/me", response_model=UserMeResponse)
def update_me(
    body: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    return UsersService(db).update(
        user=current_user,
        values=body.model_dump(exclude_unset=True),
    )


@router.get("/me/encryption-key", response_model=EncryptedKeyResponse)
def get_encryption_key(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EncryptedKeyResponse:
    try:
        encrypted_dek = UsersService(db).get_encrypted_dek(user=current_user)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return EncryptedKeyResponse(encrypted_dek=encrypted_dek)


@router.put("/me/encryption-key", response_model=EncryptedKeyResponse)
def set_encryption_key(
    body: EncryptedKeyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EncryptedKeyResponse:
    encrypted_dek = UsersService(db).set_encrypted_dek(
        user=current_user,
        encrypted_dek=body.encrypted_dek,
    )
    return EncryptedKeyResponse(encrypted_dek=encrypted_dek)
