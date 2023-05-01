from typing import List
from pydantic import BaseModel
from datetime import datetime, date


class DriverSchema(BaseModel):
    first_name: str
    last_name: str
    age: int
    is_active: bool = False
    team_id: int
    dob: date
    total_races: int = 0
    total_race_wins: int = 0
    total_podiums: int = 0
    total_points: float = 0.0

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListDriverResponse(BaseModel):
    status: str
    results: int
    drivers: List[DriverSchema]
