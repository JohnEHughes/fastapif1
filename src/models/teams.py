from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=True)
    boss_name = Column(String(50), nullable=True)
    location = Column(String(50), nullable=True)

    drivers = relationship("Driver", back_populates="team")