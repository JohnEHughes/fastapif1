import datetime
from datetime import datetime, date

import streamlit as st
import pandas as pd
import requests
import json

from streamlit_utils.config import (get_driver_data, DateTimeEncoder)


st.title("Update a Driver")
st.subheader("Please enter a Driver ID:")

col4, col5 = st.columns(spec=[3, 1])

with col5:
    driver_data = pd.DataFrame(get_driver_data()).reset_index(drop=True)
    driver_and_id = driver_data[['last_name', 'id']].reset_index(drop=True).set_index('last_name')

    expander = st.expander("Driver IDs")
    expander.dataframe(driver_and_id, height=400)

with col4:
    driver_id = st.text_input('Driver ID', key='driver_id')
    response = requests.get(url=f"http://localhost:3000/drivers/{driver_id}")
    driver = response.json().get("driver")

    if not driver:
        st.stop()

    if driver_id:
        response = requests.get(url=f"http://localhost:3000/drivers/{driver_id}")
        driver = response.json().get("driver")

        teams_response = requests.get(url=f"http://localhost:3000/teams")

        teams = teams_response.json().get('data')

        teams_df = pd.DataFrame(teams)
        team_names = teams_df['name']

        with st.form("driver_form"):

            col1, col2 = st.columns([1, 1])

            first_name = col1.text_input('First Name', value=f"{driver.get('first_name')}")
            last_name = col2.text_input('Last Name', value=f"{driver.get('last_name')}")

            option_team_name = st.selectbox('Which team?', (team_names), index=driver.get('team_id')-1)
            team_id = teams_df[teams_df['name']==option_team_name]['id'].values[0]

            col2.text('Is the Driver active?')
            is_active = col2.checkbox(label='Active', value=driver.get('is_active'))

            dob_date = driver.get('dob').split('T')
            dob_str = datetime.strptime(dob_date[0], '%Y-%m-%d').date()
        
            today = date.today()

            dob = col1.date_input("Date of birth:", dob_str, min_value=date(1920,1,1), max_value=today)
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            col3, col4= st.columns([1,1])

            total_races = col3.number_input('Total Races:', format='%i', min_value=0, step=1, value=driver.get('total_races'))
            total_race_wins = col4.number_input('Total Wins:', format='%i', min_value=0, step=1, value=driver.get('total_race_wins'))
            
            col5, col6 = st.columns([1,1])
            total_podiums = col5.number_input('Total Podiums:', format='%i', min_value=0, step=1, value=driver.get('total_podiums'))
            total_points = col6.number_input('Total Points:', format='%.1f', min_value=0.0, step=0.5, value=driver.get('total_points'))

            submitted = st.form_submit_button("Update Driver")
            if submitted:

                create_update(f"http://localhost:3000/drivers/{driver_id}", "Driver updated.")

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
                driver_response = requests.patch(
                    url=f"http://localhost:3000/drivers/{driver_id}", 
                    headers=headers, 
                    json=json_payload
                    )

                if driver_response.json().get("status") == "success":
                    st.write("Driver updated.")
                elif driver_response.json().get("status") == "Driver already exists":
                    st.write("Driver already exists.")
                else:
                    st.write("Driver errored")
                    
