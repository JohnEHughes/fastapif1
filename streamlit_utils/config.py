import requests
from datetime import datetime, date
from json import JSONEncoder


class DateTimeEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()[:10]

def get_driver_data():
    response = requests.get(url="http://localhost:3000/drivers")
    return response.json().get("data")

def get_team_data():
    response = requests.get(url="http://localhost:3000/teams")
    return response.json().get("data")