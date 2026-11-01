from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.migrate import apply_migrations
from app.db.session import get_session
from app.main import app


@pytest.fixture
def engine() -> Iterator[Engine]:
    engine = create_engine(
        "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )
    apply_migrations(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    with Session(engine, expire_on_commit=False) as session:
        yield session


@pytest.fixture
def client(engine: Engine) -> Iterator[TestClient]:
    def session_override() -> Iterator[Session]:
        with Session(engine, expire_on_commit=False) as session:
            yield session

    app.dependency_overrides[get_session] = session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
