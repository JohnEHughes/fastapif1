from datetime import datetime
from typing import List
from pydantic import BaseModel


class DriverSchema(BaseModel):
    first_name: str
    last_name: str
    age: int
    is_active: bool = False


    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListDriverResponse(BaseModel):
    status: str
    results: int
    drivers: List[DriverSchema]
