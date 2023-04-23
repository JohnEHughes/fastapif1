from typing import List
from pydantic import BaseModel


class TeamSchema(BaseModel):
    name: str
    boss_name: str
    location: str


    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListTeamResponse(BaseModel):
    status: str
    results: int
    teams: List[TeamSchema]
