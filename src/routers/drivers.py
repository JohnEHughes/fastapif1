from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from utils.requests import get_db
import pandas as pd
from database import get_db
from src.models import drivers
from src.schema import driver
from dateutil.parser import parse


router = APIRouter()


@router.get("/drivers", tags=["drivers"])
async def get_drivers(db: Session = Depends(get_db)):
    all_drivers = db.query(drivers.Driver).all()
    return {"data": all_drivers}


@router.get("/drivers/{id}")
async def get_driver(id: int, db: Session = Depends(get_db)):
    driver_model = db.query(drivers.Driver).filter(drivers.Driver.id == id)
    db_driver_model = driver_model.first()

    if not db_driver_model:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")

    return {"status": "success", "driver": db_driver_model}


@router.post("/drivers")
async def create_driver(payload: driver.DriverSchema, db: Session = Depends(get_db)):
    new_driver = drivers.Driver(**payload.dict())

    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return {"status": "success", "driver": new_driver}


@router.patch("/drivers/{id}")
async def update_driver(id: int, payload: driver.DriverSchema, db: Session = Depends(get_db)):
    driver_model = db.query(drivers.Driver).filter(drivers.Driver.id == id)
    db_driver_model = driver_model.first()

    if not db_driver_model:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")

    update_driver = payload.dict(exclude_unset=True)
    for key, value in update_driver.items():
        setattr(db_driver_model, key, value)
    db.add(db_driver_model)
    db.commit()
    db.refresh(db_driver_model)
    return {"status": "success", "driver": db_driver_model}


@router.delete("/drivers/{id}")
async def delete_driver(id: int, db: Session = Depends(get_db)):
    driver_model = db.query(drivers.Driver).filter(drivers.Driver.id == id)
    db_driver_model = driver_model.first()

    if not db_driver_model:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    
    driver_model.delete(synchronize_session=False)
    db.commit()
    return {"status": "success", "driver": "Deleted"}


@router.get("/driver_wins")
async def get_driver_wins_csv(db: Session = Depends(get_db)):
    all_drivers = db.query(drivers.Driver).all()

    drivers_list = [{
                "first_name": driver.first_name,
                "last_name": driver.last_name, 
                "team_name": driver.team.name,
                "race_wins": driver.total_race_wins
                       } for driver in all_drivers]
    

    drivers_df = pd.DataFrame(drivers_list)

    drivers_df = drivers_df.sort_values(by=['race_wins'], ascending=False)
    drivers_df.to_csv("race_wins_by_driver.csv", index=False, columns=[
        'first_name', 
        'last_name',
        'team_name',
        'race_wins'])

    return {"status": "success"}


@router.get("/driver_input")
async def driver_input(db: Session = Depends(get_db)):
    driver_list = pd.read_csv("/home/john/Documents/repos/learning/fastapif1/drivers.csv")

    for index, driver in driver_list.iterrows():
        # import pdb; pdb.set_trace()
        payload = {
            "first_name": driver['first_name'], 
            "last_name": driver['last_name'], 
            "age": driver['age'], 
            "is_active": driver['is_active'], 
            "team_id": driver['team_id'], 
            "dob": parse(driver['dob']), 
            "total_races": driver['total_races'], 
            "total_race_wins": driver['total_race_wins'], 
            "total_podiums": driver['total_podiums'], 
            "total_points": driver['total_points']
            }

        new_driver = drivers.Driver(**payload)
        db.add(new_driver)
        db.commit()
        db.refresh(new_driver)

    return {"status": "success"}