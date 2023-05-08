import requests
import json

import streamlit as st
import pandas as pd

from datetime import datetime, date
from streamlit_utils.config import DateTimeEncoder


st.title("Add Team")

st.subheader("Please enter new Team:")

with st.form("team_form", True):

    team_name = st.text_input('Team Name')
    boss_name = st.text_input('Team Principal')
    location = st.text_input('Location')

    submitted = st.form_submit_button("Submit")

    if submitted:

        payload = {
            "name": team_name, 
            "boss_name": boss_name, 
            "location": location
        }

        team_response = requests.post(
            url="http://localhost:3000/teams", 
            json=payload
            )

        if team_response.json().get("status") == "success":
            st.success("Team added successfully.")
        elif team_response.json().get("status") == "Team already exists":
            st.warning("Team already exists.")
        else:
            st.error("Team errored")
                