from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from database import get_db, Base
from main import app
from sqlalchemy.orm import sessionmaker, Session
from fastapi import status
import pytest
import models


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

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client


def test_healthchecker(client):
    response = client.get("/healthchecker")
    assert response.status_code == status.HTTP_200_OK 
    assert response.json()  == {"message": "Welcome to the Formula 1 information repo"}


def test_get_drivers(client, test_db):
    response = client.get("/drivers")
    assert response.status_code == status.HTTP_200_OK 


def test_create_driver(client, test_db):
    response = client.post("/drivers", json={"first_name": "Lewis", "last_name": "Hamilton", "age": 37, "is_active": True})
    assert response.status_code == status.HTTP_200_OK 
    assert response.json()["status"] == "success"

    created_driver_id = response.json()["driver"]["id"]
    driver_response = client.get(f"/drivers/{created_driver_id}")
    assert driver_response.status_code == status.HTTP_200_OK 


def test_delete_driver(client, test_db):
    response = client.post("/drivers", json={"first_name": "Lewis", "last_name": "Hamilton", "age": 37, "is_active": True})
    assert response.status_code == status.HTTP_200_OK 

    created_driver_id = response.json()["driver"]["id"]
    driver_response = client.get(f"/drivers/{created_driver_id}")
    assert driver_response.status_code == status.HTTP_200_OK 

    deleted_response = client.delete(f"/drivers/{created_driver_id}")
    assert deleted_response.json()["driver"] == "Deleted"

    driver_response_check = client.get(f"/drivers/{created_driver_id}")
    assert driver_response_check.status_code == 404 


def test_update_driver(client, test_db):
    response = client.post("/drivers", json={"first_name": "Lewis", "last_name": "Hamilton", "age": 37, "is_active": True})
    assert response.status_code == status.HTTP_200_OK 

    created_driver_id = response.json()["driver"]["id"]
    driver_response = client.get(f"/drivers/{created_driver_id}")
    assert driver_response.status_code == status.HTTP_200_OK 

    new_age = 38
    updated_response = client.patch(f"/drivers/{created_driver_id}", json={"first_name": "Lewis", "last_name": "Hamilton", "age": new_age, "is_active": True})

    # import pdb; pdb.set_trace()
    assert updated_response.json()["status"] == "success"

    driver_response_check = client.get(f"/drivers/{created_driver_id}")
    assert driver_response_check.json()["driver"]["age"] == new_age