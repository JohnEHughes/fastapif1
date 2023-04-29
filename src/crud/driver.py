from sqlalchemy.orm import Session

from src.models.drivers import Driver



def get_driver_by_last_and_first_name(db: Session, last_name: str, first_name: str):
    return db.query(Driver).filter(Driver.last_name == last_name and Driver.first_name == first_name).first()