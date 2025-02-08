import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal, Base
from app.db.session import engine

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c