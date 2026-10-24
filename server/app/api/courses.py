from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.courses import (
    CourseCreate,
    CourseListResponse,
    CourseResponse,
    CourseUpdate,
)
from app.services.courses import CoursesService


router = APIRouter(prefix="/api/v1/courses", tags=["Courses"])


@router.get("", response_model=CourseListResponse)
def get_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CourseListResponse:
    items = CoursesService(db).get_all(current_user=current_user)
    return CourseListResponse(items=items)


@router.post("", response_model=CourseResponse, status_code=201)
def create_course(
    body: CourseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return CoursesService(db).create(
            current_user=current_user,
            start_date=body.start_date,
            end_date=body.end_date,
            encrypted_data=body.encrypted_data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return CoursesService(db).get_by_id(
            current_user=current_user,
            course_id=course_id,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.patch("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: UUID,
    body: CourseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return CoursesService(db).update(
            current_user=current_user,
            course_id=course_id,
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


@router.delete("/{course_id}", status_code=204)
def delete_course(
    course_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    try:
        CoursesService(db).delete(
            current_user=current_user,
            course_id=course_id,
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    return Response(status_code=204)
