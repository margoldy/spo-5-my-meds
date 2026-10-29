from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.intakes import (
    IntakeCreate,
    IntakeListResponse,
    IntakeResponse,
    IntakeUpdate,
)
from app.services.intakes import IntakesService


router = APIRouter(prefix="/api/v1/intakes", tags=["Intakes"])


@router.post("", response_model=IntakeResponse, status_code=201)
def create_intake(
    body: IntakeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return IntakesService(db).create(
            current_user=current_user,
            course_id=body.course_id,
            schedule_id=body.schedule_id,
            taken_at=body.taken_at,
            encrypted_data=body.encrypted_data,
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


@router.get("", response_model=IntakeListResponse)
def get_intakes(
    course_id: UUID | None = None,
    from_: datetime | None = Query(default=None, alias="from"),
    to: datetime | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> IntakeListResponse:
    try:
        items = IntakesService(db).get_all(
            current_user=current_user,
            course_id=course_id,
            from_=from_,
            to=to,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    return IntakeListResponse(items=items)


@router.patch("/{intake_id}", response_model=IntakeResponse)
def update_intake(
    intake_id: UUID,
    body: IntakeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return IntakesService(db).update(
            current_user=current_user,
            intake_id=intake_id,
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


@router.delete("/{intake_id}", status_code=204)
def delete_intake(
    intake_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    try:
        IntakesService(db).delete(
            current_user=current_user,
            intake_id=intake_id,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    return Response(status_code=204)
