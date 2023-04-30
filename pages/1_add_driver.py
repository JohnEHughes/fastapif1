import streamlit as st
import pandas as pd
import requests
import json
from full_stream import get_data
from datetime import datetime, date
from database import get_db
from sqlalchemy.orm import Session
from src.models import drivers
from fastapi import Depends, HTTPException, APIRouter


st.title("Add Driver To Database")

st.subheader("Please enter new driver:")





teams_response = requests.get(url=f"http://localhost:3000/teams")

teams = teams_response.json().get('data')

teams_df = pd.DataFrame(teams)
team_names = teams_df['name']

with st.form("driver_form"):

    col1, col2 = st.columns([1, 1])

    first_name = col1.text_input('First Name')
    last_name = col2.text_input('Last Name')

    option_team_name = st.selectbox('Which team?', (team_names))
    team_id = teams_df[teams_df['name']==option_team_name]['id'].values[0]





    col2.text('Is the Driver active?')
    is_active = col2.checkbox(label='Active', value=True)

    dob = col1.date_input("Date of birth:", datetime.now(), min_value=date(1920,1,1))
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    col3, col4, col5, col6 = st.columns([1,1,1,1])

    total_races = col3.number_input('Total Races:', format='%i', min_value=0, step=1)
    total_race_wins = col4.number_input('Total Wins:', format='%i', min_value=0, step=1)
    total_podiums = col5.number_input('Total Podiums:', format='%i', min_value=0, step=1)
    total_points = col6.number_input('Total Points:', format='%.1f', min_value=0.0, step=0.5)

    submitted = st.form_submit_button("Submit")
    if submitted:

        st.write(f"{first_name}{type(team_id)}{is_active}{type(dob)}{age}")
        def json_serial(obj):
            """JSON serializer for objects not serializable by default json code"""

            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            raise TypeError ("Type %s not serializable" % type(obj))
        
        json_dob = json.dumps(dob, default=json_serial)

        payload = {
            "first_name": first_name, 
            "last_name": last_name, 
            "age": age, 
            "is_active": is_active,
            "team_id": int(team_id),
            "dob": json_dob,
            "total_races": int(total_races),
            "total_race_wins": int(total_race_wins),
            "total_podiums": int(total_podiums),
            "total_points": float(total_points)
        }
        # import pdb; pdb.set_trace()

        json_payload = json.dumps(payload, default=str)
        driver_response = requests.post(url=f"http://localhost:3000/drivers", json=json_payload)
        # import pdb; pdb.set_trace()
        st.write(f"{driver_response.json()} - {driver_response.status_code}")

