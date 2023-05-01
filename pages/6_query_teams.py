import requests

import streamlit as st
import pandas as pd

from streamlit_utils.config import get_team_data, get_driver_data


st.title("Team Details")
st.subheader("Please enter a Team ID:")

col4, col5 = st.columns(spec=[1, 1])

with col5:
    team_data = pd.DataFrame(get_team_data()).reset_index(drop=True)
    team_and_id = team_data[['name', 'id']].reset_index(drop=True).set_index('name')

    expander = st.expander("Team IDs")
    expander.dataframe(team_and_id, height=400)

with col4:
    team_id = st.text_input('Team Id', key='team_id')
    response = requests.get(url=f"http://localhost:3000/teams/{team_id}")
    team = response.json().get("team")

    if not team:
        st.stop()
    if team_id:
        team_name = response.json().get('team').get('name')

        st.divider()

        st.subheader(f"{team_name}")

        col1, col2 = st.columns(spec=[1, 1])

        col1.write("Team Boss:")
        col1.text(f"{team.get('boss_name')}")

        col2.write("Location:")
        col2.text(f"{team.get('location')}")

        drivers = get_driver_data()
        team_drivers = [driver for driver in drivers if str(driver['team_id']) == team_id]
        st.divider()

        st.subheader("Team Drivers:")

        col3, col4 = st.columns([1,1])

        for driver in team_drivers:

            col3.write(f"{driver['first_name']} {driver['last_name']}")
            col4.write(f"{driver['age']}yrs")

            col3.metric(label="Race starts:", value=driver['total_races'])
            col4.metric(label="Career Points:", value=driver['total_points'])

        st.divider()

        if st.button('Delete Team'):
            delete_response = requests.delete(url=f"http://localhost:3000/teams/{team_id}")
            delete_status = delete_response.json().get('status')
            if delete_status == "success":
                st.experimental_rerun()
            else:
                st.error('Error deleting team')
