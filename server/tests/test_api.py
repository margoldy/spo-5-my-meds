from datetime import date, datetime, time, timezone
from types import SimpleNamespace
from uuid import UUID

import pytest

from app.api import auth as auth_api
from app.api import courses as courses_api
from app.api import intakes as intakes_api
from app.api import medications as medications_api
from app.api import schedules as schedules_api
from app.api import users as users_api
from app.db.models import UserRole
from app.schemas.schedules import ScheduleDayItem


USER_ID = UUID("11111111-1111-1111-1111-111111111111")
COURSE_ID = UUID("22222222-2222-2222-2222-222222222222")
SCHEDULE_ID = UUID("33333333-3333-3333-3333-333333333333")
INTAKE_ID = UUID("44444444-4444-4444-4444-444444444444")
NOW = datetime(2026, 9, 19, 12, 3, tzinfo=timezone.utc)


def medication():
    return SimpleNamespace(
        id=1,
        name="Витрум",
        international_name="Vitrum",
        manufacturer="Unipharm",
        category="Витамины",
        instruction_url=None,
        form="Таблетки",
        strength="1 таблетка",
        is_active=True,
    )


def schedule():
    return SimpleNamespace(
        id=SCHEDULE_ID,
        course_id=COURSE_ID,
        scheduled_at=time(15, 0),
        days_of_week=[1, 2, 3, 4, 5, 6, 7],
        encrypted_data="schedule-data",
    )


def course():
    return SimpleNamespace(
        id=COURSE_ID,
        start_date=date(2026, 9, 1),
        end_date=None,
        is_active=True,
        encrypted_data="course-data",
        taking_mode="scheduled",
        schedules=[schedule()],
        created_at=NOW,
    )


def intake():
    return SimpleNamespace(
        id=INTAKE_ID,
        user_id=USER_ID,
        course_id=COURSE_ID,
        schedule_id=SCHEDULE_ID,
        taken_at=NOW,
        encrypted_data="intake-data",
    )


class FakeAuthService:
    def __init__(self, db):
        pass

    def request_code(self, *, email):
        pass

    def verify_code(self, *, email, code):
        user = SimpleNamespace(
            id=USER_ID,
            name=None,
            email=email,
            birth_date=None,
            role=UserRole.USER,
            avatar_url=None,
            timezone="Europe/Moscow",
            created_at=NOW,
        )
        return "access", "refresh", user

    def refresh_access_token(self, *, refresh_token):
        return "new-access"


class FakeUsersService:
    def __init__(self, db):
        pass

    def update(self, *, user, values):
        for field, value in values.items():
            setattr(user, field, value)
        return user

    def get_encrypted_dek(self, *, user):
        return user.encrypted_dek

    def set_encrypted_dek(self, *, user, encrypted_dek):
        user.encrypted_dek = encrypted_dek
        return encrypted_dek


class FakeMedicationsService:
    def __init__(self, db):
        pass

    def get_all(self, **kwargs):
        return [medication()], 1

    def get_by_id(self, **kwargs):
        return medication()

    def create(self, *, values):
        return SimpleNamespace(**medication().__dict__ | values)

    def update(self, *, medication_id, values):
        return SimpleNamespace(**medication().__dict__ | values)


class FakeCoursesService:
    def __init__(self, db):
        pass

    def get_all(self, *, current_user):
        return [course()]

    def get_by_id(self, *, current_user, course_id):
        return course()

    def create(self, **kwargs):
        return course()

    def update(self, **kwargs):
        item = course()
        for field, value in kwargs["values"].items():
            setattr(item, field, value)
        return item

    def delete(self, **kwargs):
        pass


class FakeSchedulesService:
    def __init__(self, db):
        pass

    def get_for_course(self, **kwargs):
        return [schedule()]

    def create(self, **kwargs):
        return schedule()

    def update(self, **kwargs):
        item = schedule()
        for field, value in kwargs["values"].items():
            setattr(item, field, value)
        return item

    def delete(self, **kwargs):
        pass

    def get_for_day(self, **kwargs):
        return [
            ScheduleDayItem(
                schedule_id=SCHEDULE_ID,
                course_id=COURSE_ID,
                planned_at=NOW,
                course_data="course-data",
                schedule_data="schedule-data",
                status="pending",
                intake=None,
            )
        ]


class FakeIntakesService:
    def __init__(self, db):
        pass

    def create(self, **kwargs):
        return intake()

    def get_all(self, **kwargs):
        return [intake()]

    def update(self, **kwargs):
        item = intake()
        for field, value in kwargs["values"].items():
            setattr(item, field, value)
        return item

    def delete(self, **kwargs):
        pass


@pytest.fixture(autouse=True)
def services(monkeypatch):
    monkeypatch.setattr(auth_api, "AuthService", FakeAuthService)
    monkeypatch.setattr(users_api, "UsersService", FakeUsersService)
    monkeypatch.setattr(medications_api, "MedicationsService", FakeMedicationsService)
    monkeypatch.setattr(courses_api, "CoursesService", FakeCoursesService)
    monkeypatch.setattr(schedules_api, "SchedulesService", FakeSchedulesService)
    monkeypatch.setattr(intakes_api, "IntakesService", FakeIntakesService)


def test_health(client):
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_auth(client):
    request = client.post(
        "/api/v1/auth/code/request",
        json={"email": "user@example.com"},
    )
    verify = client.post(
        "/api/v1/auth/code/verify",
        json={"email": "user@example.com", "code": "123456"},
    )
    refresh = client.post(
        "/api/v1/auth/token/refresh",
        json={"refresh_token": "refresh"},
    )

    assert request.status_code == 200
    assert verify.json()["refresh_token"] == "refresh"
    assert refresh.json()["access_token"] == "new-access"


def test_profile_and_key(client):
    profile = client.patch("/api/v1/users/me", json={"name": "Новое имя"})
    key = client.put(
        "/api/v1/users/me/encryption-key",
        json={"encrypted_dek": "new-key"},
    )

    assert profile.status_code == 200
    assert profile.json()["name"] == "Новое имя"
    assert key.json() == {"encrypted_dek": "new-key"}


def test_medications(client, user):
    listed = client.get("/api/v1/medications?search=витрум")
    detail = client.get("/api/v1/medications/1")
    user.role = UserRole.ADMIN
    created = client.post(
        "/api/v1/medications",
        json={"name": "Витрум"},
    )

    assert listed.json()["total"] == 1
    assert detail.json()["name"] == "Витрум"
    assert created.status_code == 201


def test_courses(client):
    listed = client.get("/api/v1/courses")
    created = client.post(
        "/api/v1/courses",
        json={
            "start_date": "2026-09-01",
            "end_date": None,
            "encrypted_data": "course-data",
        },
    )
    deleted = client.delete(f"/api/v1/courses/{COURSE_ID}")

    assert listed.json()["items"][0]["taking_mode"] == "scheduled"
    assert created.status_code == 201
    assert deleted.status_code == 204


def test_schedules(client):
    listed = client.get(f"/api/v1/courses/{COURSE_ID}/schedules")
    created = client.post(
        f"/api/v1/courses/{COURSE_ID}/schedules",
        json={
            "scheduled_at": "15:00",
            "days_of_week": [1, 2, 3, 4, 5, 6, 7],
            "encrypted_data": "schedule-data",
        },
    )
    day = client.get("/api/v1/schedules?date=2026-09-19")

    assert listed.json()["items"][0]["scheduled_at"] == "15:00:00"
    assert created.status_code == 201
    assert day.json()["items"][0]["status"] == "pending"


def test_intakes(client):
    created = client.post(
        "/api/v1/intakes",
        json={
            "course_id": str(COURSE_ID),
            "schedule_id": str(SCHEDULE_ID),
            "taken_at": "2026-09-19T15:03:00+03:00",
            "encrypted_data": "intake-data",
        },
    )
    listed = client.get("/api/v1/intakes")
    deleted = client.delete(f"/api/v1/intakes/{INTAKE_ID}")

    assert created.status_code == 201
    assert listed.json()["items"][0]["encrypted_data"] == "intake-data"
    assert deleted.status_code == 204
