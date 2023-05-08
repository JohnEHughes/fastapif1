import datetime
from datetime import datetime, date

import streamlit as st
import pandas as pd
import requests
import json

from streamlit_utils.config import (get_team_data, DateTimeEncoder)


st.title("Update a Team")
st.subheader("Please enter a Team ID:")

col4, col5 = st.columns(spec=[2, 1])

with col5:
    team_data = pd.DataFrame(get_team_data()).reset_index(drop=True)
    team_and_id = team_data[['name', 'id']].reset_index(drop=True).set_index('name')

    expander = st.expander("Team IDs")
    expander.dataframe(team_and_id, height=400)

with col4:
    team_id = st.text_input('Team ID', key='team_id')
    response = requests.get(url=f"http://localhost:3000/teams/{team_id}")
    team = response.json().get("team")

    if not team:
        st.stop()

    if team_id:

        st.divider()

        with st.form("team_form", True):

            col1, col2, col3 = st.columns([1, 1, 1])

            team_name = col1.text_input('Team Name', value=f"{team.get('name')}")
            boss_name = col2.text_input('Team Principal', value=f"{team.get('boss_name')}")
            location = col3.text_input('Location', value=f"{team.get('location')}")

            submitted = st.form_submit_button("Update Team")

            if submitted:

                payload = {
                        "name": team_name, 
                        "boss_name": boss_name, 
                        "location": location
                }

                team_response = requests.patch(
                    url=f"http://localhost:3000/teams/{team_id}", 
                    json=payload
                    )

                if team_response.json().get("status") == "success":
                    st.success("Team updated.")
                elif team_response.json().get("status") == "Team already exists":
                    st.warning("Team already exists.")
                else:
                    st.error("Team errored")
                        
