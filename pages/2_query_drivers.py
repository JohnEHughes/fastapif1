import streamlit as st
import pandas as pd
import requests
from full_stream import get_data
from datetime import datetime
from database import get_db
from sqlalchemy.orm import Session
from src.models import drivers
from fastapi import Depends, HTTPException, APIRouter


st.title("Driver Race Details")

st.subheader("Please enter a driver ID:")



col4, col5 = st.columns(spec=[3, 2])

with col4:
    driver_id = st.text_input('Driver Id', key='driver_id')

    if driver_id:
        response = requests.get(url=f"http://localhost:3000/drivers/{driver_id}")
        driver = response.json().get("driver")

        team_id = driver['team_id']
        team_response = requests.get(url=f"http://localhost:3000/teams/{team_id}")

        team_name = team_response.json().get('team').get('name')

        st.subheader(f"{driver['first_name']} {driver['last_name']}")
        st.write(f"{team_name}")

        col1, col2, col3 = st.columns(spec=[1, 1, 1])
        col1.metric(label=f"Race Wins", value=driver['total_race_wins'])
        col2.metric(label=f"Podiums", value=driver['total_podiums'])
        col3.metric(label=f"Total Points", value=f"{driver['total_points']:,}")

        win_perc = f"{(driver['total_race_wins'] / driver['total_races']):.1%}"
        podium_perc = f"{(driver['total_podiums'] / driver['total_races']):.1%}"
        points_per_race = f"{(driver['total_points'] / driver['total_races']):.1f}"

        col1.metric(label=f"Win Percentage", value=win_perc)
        col2.metric(label=f"Podium Percentage", value=podium_perc)
        col3.metric(label=f"Points Per Race", value=points_per_race)
        

with col5:
    driver_data = pd.DataFrame(get_data()).reset_index(drop=True)
    driver_and_id = driver_data[['last_name', 'id']].reset_index(drop=True).set_index('last_name')

    st.dataframe(driver_and_id, height=735)