from sqlalchemy import Column, String, Boolean, Integer

from database.database import Base



class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=False)
