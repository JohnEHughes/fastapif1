from fastapi import status


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
        # import pdb; pdb.set_trace()
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


    def test_update_driver(self, client, test_db, add_one_driver, example_driver_payload):
        response = add_one_driver
        assert response.status_code == status.HTTP_200_OK 

        created_driver_id = response.json()["driver"]["id"]
        driver_response = client.get(f"/drivers/{created_driver_id}")
        assert driver_response.status_code == status.HTTP_200_OK 

        new_age = 38
        update_driver_payload = example_driver_payload
        update_driver_payload["age"] = new_age
        updated_response = client.patch(f"/drivers/{created_driver_id}", json=update_driver_payload)

        assert updated_response.json()["status"] == "success"

        driver_response_check = client.get(f"/drivers/{created_driver_id}")
        assert driver_response_check.json()["driver"]["age"] == new_age


    def test_get_driver_wins(self, client, test_db, add_one_team):

        response = add_one_team
        assert response.status_code == status.HTTP_200_OK
        created_team_id = response.json().get('team').get('id')


        driver_payload_1 = {
            "first_name": "Lewis", 
            "last_name": "Hamilton", 
            "age": 37, 
            "is_active": True,
            "team_id":created_team_id,
            "dob": 1985,
            "total_races": 100,
            "total_race_wins": 50,
            "total_podiums": 61,
            "total_points": 400
            }

        first_driver_response = client.post("/drivers", json=driver_payload_1)
        assert first_driver_response.status_code == status.HTTP_200_OK 

        driver_payload_2 = {
            "first_name": "George", 
            "last_name": "Russell", 
            "age": 24, 
            "is_active": False,
            "team_id":created_team_id,
            "dob": 1999,
            "total_races": 45,
            "total_race_wins": 3,
            "total_podiums": 5,
            "total_points": 40
            }
        second_driver_response = client.post("/drivers", json=driver_payload_2)
        assert second_driver_response.status_code == status.HTTP_200_OK 


        team_payload_2 = {
            "name": "Red Bull Racing", 
            "boss_name": "Christian Horner", 
            "location": "UK"
            }

        team_response_2 = client.post("/teams", json=team_payload_2)
        # import pdb; pdb.set_trace()
        created_team_2_id = team_response_2.json().get('team').get('id')

        driver_payload_3 = {
            "first_name": "Max", 
            "last_name": "Verstappen", 
            "age": 25, 
            "is_active": True,
            "team_id":created_team_2_id,
            "dob": 1998,
            "total_races": 60,
            "total_race_wins": 34,
            "total_podiums": 40,
            "total_points": 250
            }

        first_driver_response = client.post("/drivers", json=driver_payload_3)
        assert first_driver_response.status_code == status.HTTP_200_OK 

        driver_payload_4 = {
            "first_name": "Checo", 
            "last_name": "Perez", 
            "age": 28, 
            "is_active": True,
            "team_id":created_team_2_id,
            "dob": 1995,
            "total_races": 82,
            "total_race_wins": 12,
            "total_podiums": 21,
            "total_points": 56
            }
        second_driver_response = client.post("/drivers", json=driver_payload_4)
        assert second_driver_response.status_code == status.HTTP_200_OK 


        team_payload_3 = {
            "name": "McLaren Racing", 
            "boss_name": "Zak Brown", 
            "location": "UK"
            }

        team_response_3 = client.post("/teams", json=team_payload_3)
        created_team_3_id = team_response_3.json().get('team').get('id')

        driver_payload_5 = {
            "first_name": "Lando", 
            "last_name": "Norris", 
            "age": 24, 
            "is_active": True,
            "team_id":created_team_3_id,
            "dob": 1999,
            "total_races": 24,
            "total_race_wins": 0,
            "total_podiums": 2,
            "total_points": 25
            }

        first_driver_response = client.post("/drivers", json=driver_payload_5)
        assert first_driver_response.status_code == status.HTTP_200_OK 

        driver_payload_6 = {
            "first_name": "Oscar", 
            "last_name": "Piastri", 
            "age": 27, 
            "is_active": True,
            "team_id":created_team_3_id,
            "dob": 1996,
            "total_races": 3,
            "total_race_wins": 0,
            "total_podiums": 0,
            "total_points": 4
            }
        second_driver_response = client.post("/drivers", json=driver_payload_6)
        assert second_driver_response.status_code == status.HTTP_200_OK 

        teams_response = client.get("/driver_wins")
        assert teams_response.status_code == status.HTTP_200_OK 
