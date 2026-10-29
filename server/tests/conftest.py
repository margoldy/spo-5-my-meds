from contextlib import asynccontextmanager
from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.core.deps import get_current_user, get_optional_user
from app.db.models import UserRole
from app.db.session import get_db
from app.main import app


def fake_db():
    yield None


@asynccontextmanager
async def empty_lifespan(app):
    yield


@pytest.fixture
def user():
    return SimpleNamespace(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        name="Макан",
        email="user@example.com",
        birth_date=None,
        role=UserRole.USER,
        avatar_url=None,
        timezone="Europe/Moscow",
        encrypted_dek="encrypted-key",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


@pytest.fixture
def client(monkeypatch, user):
    monkeypatch.setattr(app.router, "lifespan_context", empty_lifespan)
    app.dependency_overrides[get_db] = fake_db
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_optional_user] = lambda: user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
