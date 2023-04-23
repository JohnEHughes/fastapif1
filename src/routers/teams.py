from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from models import teams
from schema import team



router = APIRouter()


@router.get("/teams", tags=["teams"])
async def get_teams(db: Session = Depends(get_db)):
    all_teams = db.query(teams.Team).all()
    return {"data": all_teams}


@router.get("/teams/{id}")
async def get_team(id: int, db: Session = Depends(get_db)):
    team_model = db.query(teams.Team).filter(teams.Team.id == id)
    db_team_model = team_model.first()

    if not db_team_model:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")

    return {"status": "success", "team": db_team_model}


@router.post("/teams")
async def create_team(payload: team.TeamSchema, db: Session = Depends(get_db)):
    new_team = teams.Team(**payload.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return {"status": "success", "team": new_team}


@router.patch("/teams/{id}")
async def update_team(id: int, payload: team.TeamSchema, db: Session = Depends(get_db)):
    team_model = db.query(teams.Team).filter(teams.Team.id == id)
    db_team_model = team_model.first()

    if not db_team_model:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")

    update_team = payload.dict(exclude_unset=True)
    for key, value in update_team.items():
        setattr(db_team_model, key, value)
    db.add(db_team_model)
    db.commit()
    db.refresh(db_team_model)
    return {"status": "success", "drivteamer": db_team_model}


@router.delete("/teams/{id}")
async def delete_team(id: int, db: Session = Depends(get_db)):
    team_model = db.query(teams.Team).filter(teams.Team.id == id)
    db_team_model = team_model.first()

    if not db_team_model:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    
    db_team_model.delete(synchronize_session=False)
    db.commit()
    return {"status": "success", "team": "Deleted"}