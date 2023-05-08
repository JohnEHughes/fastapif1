import datetime

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=False)
    team_id = Column(Integer, ForeignKey("team.id"))
    dob = Column(DateTime, nullable=True)
    total_races = Column(Integer, nullable=True)
    total_race_wins = Column(Integer, nullable=True)
    total_podiums = Column(Integer, nullable=True)
    total_points = Column(Float, nullable=True)

    team = relationship("Team", back_populates="drivers")


    def __repr__(self):
        return f"{self.first_name} {self.last_name}, driver for {self.team}"
    
