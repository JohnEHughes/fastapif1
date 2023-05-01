import requests
import json

import streamlit as st
import pandas as pd

from datetime import datetime, date
from streamlit_utils.config import DateTimeEncoder

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

        payload = {
            "first_name": first_name, 
            "last_name": last_name, 
            "age": age, 
            "is_active": is_active,
            "team_id": int(team_id),
            "total_races": int(total_races),
            "total_race_wins": int(total_race_wins),
            "total_podiums": int(total_podiums),
            "total_points": float(total_points),
            "dob": dob,
        }

        json_payload = json.loads(DateTimeEncoder().encode(payload))

        headers = {'Content-type':'application/json', 'Accept':'text/plain'}
        driver_response = requests.post(
             url="http://localhost:3000/drivers", 
             headers=headers, 
             json=json_payload
             )

        if driver_response.json().get("status") == "success":
            st.write("Driver added successfully.")
        elif driver_response.json().get("status") == "Driver already exists":
            st.write("Driver already exists.")
        else:
            st.write("Driver errored")
             
