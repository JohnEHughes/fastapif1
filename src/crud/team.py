from sqlalchemy.orm import Session

from src.models.teams import Team



def get_team_by_name(db: Session, name: str):
    return db.query(Team).filter(Team.name == name).first()