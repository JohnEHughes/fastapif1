from fastapi import status
import pytest
import datatest as dt
import pandas as pd

class TestTeams:



    def test_get_teams(self, client, test_db):
        response = client.get("/teams")
        assert response.status_code == status.HTTP_200_OK 


    def test_create_team(self, client, test_db, add_one_team):
        response = add_one_team
        assert response.status_code == status.HTTP_200_OK 
        assert response.json()["status"] == "success"

        created_team_id = response.json()["team"]["id"]
        team_response = client.get(f"/teams/{created_team_id}")
        assert team_response.status_code == status.HTTP_200_OK 


    def test_delete_team(self, client, test_db, add_one_team):
        response = add_one_team
        assert response.status_code == status.HTTP_200_OK 

        created_team_id = response.json()["team"]["id"]
        team_response = client.get(f"/teams/{created_team_id}")
        assert team_response.status_code == status.HTTP_200_OK 

        deleted_response = client.delete(f"/teams/{created_team_id}")
        assert deleted_response.json()["team"] == "Deleted"

        team_response_check = client.get(f"/teams/{created_team_id}")
        assert team_response_check.status_code == 404 


    def test_update_team(self, client, test_db, add_one_team, example_team_payload):
        response = add_one_team
        assert response.status_code == status.HTTP_200_OK 

        created_team_id = response.json()["team"]["id"]
        team_response = client.get(f"/teams/{created_team_id}")
        assert team_response.status_code == status.HTTP_200_OK 

        boss_name = "Toto"
        update_team_payload = example_team_payload
        update_team_payload["boss_name"] = boss_name
        updated_response = client.patch(f"/teams/{created_team_id}", json=update_team_payload)

        assert updated_response.json()["status"] == "success"

        team_response_check = client.get(f"/teams/{created_team_id}")
        assert team_response_check.json()["team"]["boss_name"] == boss_name


    def test_get_active_driver_two_active_no_params(self, client, test_db, add_one_team):

        response = add_one_team
        assert response.status_code == status.HTTP_200_OK
        created_team_id = response.json()["team"]["id"]

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
            "is_active": True,
            "team_id":created_team_id,
            "dob": 1999,
            "total_races": 45,
            "total_race_wins": 43,
            "total_podiums": 5,
            "total_points": 40
            }
        second_driver_response = client.post("/drivers", json=driver_payload_2)
        assert second_driver_response.status_code == status.HTTP_200_OK 

        team_response = client.post(f"/teams/active/{1}", json={})
        assert team_response.status_code == status.HTTP_200_OK 


    def test_get_active_driver_csv_two_active_with_losses(self, client, test_db, add_one_team):

        response = add_one_team
        assert response.status_code == status.HTTP_200_OK
        created_team_id = response.json()["team"]["id"]

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
            "is_active": True,
            "team_id":created_team_id,
            "dob": 1999,
            "total_races": 45,
            "total_race_wins": 43,
            "total_podiums": 5,
            "total_points": 40
            }
        second_driver_response = client.post("/drivers", json=driver_payload_2)
        assert second_driver_response.status_code == status.HTTP_200_OK 

        losses = 5
        json = {"losses": losses}
        team_response = client.post(f"/teams/active/{1}", json=json)

        assert team_response.status_code == status.HTTP_200_OK 
        

    def test_get_active_driver_csv_two_active_with_col_heads(self, client, test_db, add_one_team):

        response = add_one_team
        assert response.status_code == status.HTTP_200_OK
        created_team_id = response.json()["team"]["id"]

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
            "is_active": True,
            "team_id":created_team_id,
            "dob": 1999,
            "total_races": 45,
            "total_race_wins": 43,
            "total_podiums": 5,
            "total_points": 40
            }
        second_driver_response = client.post("/drivers", json=driver_payload_2)
        assert second_driver_response.status_code == status.HTTP_200_OK 

        col_heads = ['last_name', 'total_races', 'total_race_wins', 'total_podiums', 'total_points']

        json = {"col_heads": col_heads}
        team_response = client.post(f"/teams/active/{1}", json=json)
        test_csv = pd.read_csv('AMG-Mercedes_-_active_ drivers_list.csv')
        dt.validate(test_csv.columns,
                {'last_name', 'total_races', 'total_race_wins', 'total_podiums', 'total_points', 'id'},)

        assert team_response.status_code == status.HTTP_200_OK 
        

    def test_get_active_driver_one_active_no_params(self, client, test_db, add_one_team):

        response = add_one_team
        assert response.status_code == status.HTTP_200_OK
        created_team_id = response.json()["team"]["id"]

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
            "total_race_wins": 43,
            "total_podiums": 5,
            "total_points": 40
            }
        second_driver_response = client.post("/drivers", json=driver_payload_2)
        assert second_driver_response.status_code == status.HTTP_200_OK 

        team_response = client.post(f"/teams/active/{1}", json={})
        assert team_response.status_code == status.HTTP_200_OK 


    def test_get_team_wins(self, client, test_db, add_one_team):

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
            "total_race_wins": 43,
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
        created_team_3_id = team_response_2.json().get('team').get('id')

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

        teams_response = client.get(f"/team_wins")
        assert teams_response.status_code == status.HTTP_200_OK 

