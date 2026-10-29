from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.schedules import (
    ScheduleCreate,
    ScheduleDayResponse,
    ScheduleListResponse,
    ScheduleResponse,
    ScheduleUpdate,
)
from app.services.schedules import SchedulesService


router = APIRouter(prefix="/api/v1", tags=["Schedules"])


@router.get(
    "/courses/{course_id}/schedules",
    response_model=ScheduleListResponse,
)
def get_course_schedules(
    course_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ScheduleListResponse:
    try:
        items = SchedulesService(db).get_for_course(
            current_user=current_user,
            course_id=course_id,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    return ScheduleListResponse(items=items)


@router.post(
    "/courses/{course_id}/schedules",
    response_model=ScheduleResponse,
    status_code=201,
)
def create_schedule(
    course_id: UUID,
    body: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return SchedulesService(db).create(
            current_user=current_user,
            course_id=course_id,
            scheduled_at=body.scheduled_at,
            days_of_week=body.days_of_week,
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


@router.patch("/schedules/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(
    schedule_id: UUID,
    body: ScheduleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return SchedulesService(db).update(
            current_user=current_user,
            schedule_id=schedule_id,
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


@router.delete("/schedules/{schedule_id}", status_code=204)
def delete_schedule(
    schedule_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    try:
        SchedulesService(db).delete(
            current_user=current_user,
            schedule_id=schedule_id,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    return Response(status_code=204)


@router.get("/schedules", response_model=ScheduleDayResponse)
def get_schedules(
    day: date = Query(alias="date"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ScheduleDayResponse:
    items = SchedulesService(db).get_for_day(
        current_user=current_user,
        day=day,
    )
    return ScheduleDayResponse(date=day, items=items)
