from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from models import drivers
from schema import driver



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