from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_optional_user, require_roles
from app.db.models import User, UserRole
from app.db.session import get_db
from app.schemas.medications import (
    MedicationCreate,
    MedicationListResponse,
    MedicationResponse,
    MedicationUpdate,
)
from app.services.medications import MedicationsService


router = APIRouter(prefix="/api/v1/medications", tags=["Medications"])


@router.get("", response_model=MedicationListResponse)
def get_medications(
    search: str | None = None,
    category: str | None = None,
    form: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> MedicationListResponse:
    include_inactive = (
        current_user is not None and current_user.role == UserRole.ADMIN
    )
    items, total = MedicationsService(db).get_all(
        search=search,
        category=category,
        form=form,
        limit=limit,
        offset=offset,
        include_inactive=include_inactive,
    )
    return MedicationListResponse(items=items, total=total)


@router.get("/{medication_id}", response_model=MedicationResponse)
def get_medication(
    medication_id: int,
    current_user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    include_inactive = (
        current_user is not None and current_user.role == UserRole.ADMIN
    )
    try:
        return MedicationsService(db).get_by_id(
            medication_id=medication_id,
            include_inactive=include_inactive,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post("", response_model=MedicationResponse, status_code=201)
def create_medication(
    body: MedicationCreate,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    try:
        return MedicationsService(db).create(values=body.model_dump())
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.patch("/{medication_id}", response_model=MedicationResponse)
def update_medication(
    medication_id: int,
    body: MedicationUpdate,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    try:
        return MedicationsService(db).update(
            medication_id=medication_id,
            values=body.model_dump(exclude_unset=True),
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
