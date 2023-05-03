from fastapi import Depends, HTTPException, APIRouter, Request, Query
from sqlalchemy.orm import Session
from pathlib import Path
import pandas as pd
import numpy as np
import os
from typing import List
# from utils.requests import get_db
from database import get_db
from src.models import teams
from src.schema import team
from src.crud.team import get_team_by_name

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
    try:
        name = new_team.name

    except KeyError:
        return {"status": "key error"}
    
    check_team = get_team_by_name(db, name)
    if check_team:
        return {"status": "Team already exists"}
    
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
    return {"status": "success", "team": db_team_model}


@router.delete("/teams/{id}")
async def delete_team(id: int, db: Session = Depends(get_db)):    
    team_model = db.query(teams.Team).filter(teams.Team.id == id)
    db_team_model = team_model.first()

    if not db_team_model:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    
    team_model.delete(synchronize_session=False)
    db.commit()
    return {"status": "success", "team": "Deleted"}


# new route team_id as path param
# by default return csv with all the active drivers for the team

# add arg - List of col headings - 
# construct csv with these columns but always include the id col

# in addition to the col headings, if the arg total race losses is passed, return that
# via pandas calculating win from total

@router.post("/teams/active/{id}")
async def get_active_driver_csv(id: int, request: Request = None, db: Session = Depends(get_db)):
    team = db.query(teams.Team).filter(teams.Team.id == id).first()
    payload = await request.json()

    active_drivers = [{
                "id": driver.id,
                "first_name": driver.first_name, 
                "last_name": driver.last_name,
                "age":driver.age,
                "is_active": driver.is_active,
                "team_id": driver.team_id,
                "dob": driver.dob,
                "total_races": driver.total_races,
                "total_race_wins": driver.total_race_wins,
                "total_podiums": driver.total_podiums,
                "total_points": driver.total_points
                       } for driver in team.drivers if driver.is_active == True]
    
    all_col_names = [
        'id', 
        'first_name', 
        'last_name', 
        'age', 
        'is_active', 
        'team_id', 
        'dob', 
        'total_races', 
        'total_race_wins', 
        'total_podiums', 
        'total_points']
    
    active_df = pd.DataFrame(active_drivers)
    col_heads = payload.get("col_heads", None)

    if col_heads:
        col_heads = desired_column_headings(col_heads)
    else:
        col_heads = all_col_names
    losses = payload.get("losses", False)
    if losses:
        col_loss_name = f"no_losses"
        active_df[col_loss_name] = active_df['total_races'] - active_df['total_race_wins']
        col_heads.append(col_loss_name)

    active_df.to_csv(f"{team.name}_-_active_ drivers_list.csv", index=False, columns=col_heads)

    return {"status": "success", "drivers": active_drivers}


def desired_column_headings(requested_headings) -> list[str]:
    columns = requested_headings
    if type(requested_headings) != list:
        columns = set(eval(requested_headings))
    else:
        columns = set(requested_headings)
    all_col_names = set([
        'id', 
        'first_name', 
        'last_name', 
        'age', 
        'is_active', 
        'team_id', 
        'dob', 
        'total_races', 
        'total_race_wins', 
        'total_podiums', 
        'total_points'])
    
    desired_cols = columns.intersection(all_col_names)
    desired_cols.add('id')
    col_list = [col for col in desired_cols]
    return col_list


# second endpoint - no path params
# return a csv showing total no. of race wins per team, separated by team and ordered from
# highest to lowest


@router.get("/team_wins")
async def get_team_wins_csv(db: Session = Depends(get_db)):
    all_teams = db.query(teams.Team).all()

    teams_list = [{
                "name": team.name,
                "boss_name": team.boss_name, 
                "location": team.location,
                "drivers": team.drivers
                       } for team in all_teams]
    
    teams_df = pd.DataFrame(teams_list)
    race_wins = [sum([i.total_race_wins for i in item]) for item in teams_df.drivers]

    teams_df['race_wins'] = race_wins
    teams_df = teams_df.sort_values(by=['race_wins'], ascending=False)

    teams_df.to_csv("wins_by_team.csv", index=False, columns=['name', 'race_wins'])

    return {"status": "success"}


@router.get("/team_input")
async def team_input(db: Session = Depends(get_db)):
    team_list = pd.read_csv("/home/john/Documents/repos/learning/fastapif1/teams.csv")

    for index, team in team_list.iterrows():
        payload = {
            "name": team['name'], 
            "boss_name": team['boss_name'], 
            "location": team['location']
            }
        
        try:
            name = payload.get("name")

        except KeyError:
            return {"status": "key error"}
    
        check_team = get_team_by_name(db, name)
        if check_team:
            return {"status": "Team already exists"}

        new_team = teams.Team(**payload)
        db.add(new_team)
        db.commit()
        db.refresh(new_team)

    return {"status": "success"}

