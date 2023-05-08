
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pytest
import datatest as dt
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from fastapi.testclient import TestClient
from src.main import app


from database import Base, get_db


SQLITE_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLITE_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    SQLITE_DATABASE_URL = "sqlite:///./test.db"

    engine = create_engine(
        SQLITE_DATABASE_URL, connect_args={"check_same_thread": False}
    )

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client



@pytest.fixture()
def example_driver_payload():
    return {
            "first_name": "Lewis", 
            "last_name": "Hamilton", 
            "age": 37, 
            "is_active": True,
            "team_id":1,
            "dob": 1985,
            "total_races": 100,
            "total_race_wins": 50,
            "total_podiums": 61,
            "total_points": 400
            }

@pytest.fixture()
def add_one_driver(client, example_driver_payload):
    return client.post("/drivers", json=example_driver_payload)


@pytest.fixture()
def example_team_payload():
    return {
            "name": "AMG-Mercedes", 
            "boss_name": "Toto Wolff", 
            "location": "UK"
            }

@pytest.fixture()
def add_one_team(client, example_team_payload):
    return client.post("/teams", json=example_team_payload)


@pytest.mark.mandatory
def test_columns(df):
    dt.validate(
        df.columns,
        {'first_name', 'last_name', 'team_name', 'race_wins'},
    )