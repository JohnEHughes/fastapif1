from fastapi import status
from conftest import add_one_driver, test_db, client

from main import app


class TestDrivers:

    def test_healthchecker(self, client):
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK 
        assert response.json()  == {"message": "Welcome to the Formula 1 information repo"}


    def test_get_drivers(self, client, test_db):
        response = client.get("/drivers")
        assert response.status_code == status.HTTP_200_OK 


    def test_create_driver(self, client, test_db, add_one_driver):
        response = add_one_driver
        assert response.status_code == status.HTTP_200_OK 
        assert response.json()["status"] == "success"

        created_driver_id = response.json()["driver"]["id"]
        driver_response = client.get(f"/drivers/{created_driver_id}")
        assert driver_response.status_code == status.HTTP_200_OK 


    def test_delete_driver(self, client, test_db, add_one_driver):
        response = add_one_driver
        assert response.status_code == status.HTTP_200_OK 

        created_driver_id = response.json()["driver"]["id"]
        driver_response = client.get(f"/drivers/{created_driver_id}")
        assert driver_response.status_code == status.HTTP_200_OK 

        deleted_response = client.delete(f"/drivers/{created_driver_id}")
        assert deleted_response.json()["driver"] == "Deleted"

        driver_response_check = client.get(f"/drivers/{created_driver_id}")
        assert driver_response_check.status_code == 404 


    def test_update_driver(self, client, test_db, add_one_driver):
        response = add_one_driver
        assert response.status_code == status.HTTP_200_OK 

        created_driver_id = response.json()["driver"]["id"]
        driver_response = client.get(f"/drivers/{created_driver_id}")
        assert driver_response.status_code == status.HTTP_200_OK 

        new_age = 38
        updated_response = client.patch(f"/drivers/{created_driver_id}", json={"first_name": "Lewis", "last_name": "Hamilton", "age": new_age, "is_active": True})

        assert updated_response.json()["status"] == "success"

        driver_response_check = client.get(f"/drivers/{created_driver_id}")
        assert driver_response_check.json()["driver"]["age"] == new_age