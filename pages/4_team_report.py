import streamlit as st
import pandas as pd
import requests


st.title("Team Report")

teams_response = requests.get(url=f"http://localhost:3000/teams")
teams = teams_response.json().get('data')
teams_df = pd.DataFrame(teams)
team_names = teams_df['name']

response = requests.get(url=f"http://localhost:3000/drivers")
driver = response.json().get('data')
drivers_df = pd.DataFrame(driver)
col_headings_full = list(drivers_df)
col_headings_full.remove("id")

with st.expander("Team Wins"):
    st.subheader("Team Wins Report CSV")
    st.write("Press submit to produce a csv showing the number of wins by team sorted in descending order.")

    with st.form("team_wins", True):

        submitted = st.form_submit_button("Submit")

        if submitted:
            col1, col2 = st.columns([1,2])

            response = requests.get(url="http://localhost:3000/team_wins")
            response_json = response.json().get("status")
            col1.text(f"wins_by_team.csv")

            team_wins_csv = pd.read_csv("./static/wins_by_team.csv")

            csv_df = pd.DataFrame(team_wins_csv).reset_index(drop=True)
            col1.dataframe(csv_df.set_index('name'))

            col2.bar_chart(data=csv_df, x="name", y="race_wins", height=400)

with st.expander("Individual Team Reports"):
    st.subheader("Individual Team Report CSV")

    with st.form("driver_form", True):

        option_team_name = st.selectbox('Which team?', (team_names))
        team_id = teams_df[teams_df['name']==option_team_name]['id'].values[0]

        col_heads = st.multiselect(
        'Please choose required column names:', col_headings_full, col_headings_full)

        st.text('Show number of losses?')
        losses = st.checkbox(label='Losses', value=False)

        payload = {
                "col_heads": col_heads, 
                "losses": losses, 
                "team_id": int(team_id),
        }

        response = requests.post(url=f"http://localhost:3000/teams/active/{team_id}", json=payload)
        response_json = response.json().get("status")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.text(f"CSV produced - {option_team_name}_-_active_ drivers_list.csv")

            team_csv = pd.read_csv(f"./static/{option_team_name}_-_active_ drivers_list.csv")
            csv_df = pd.DataFrame(team_csv).reset_index(drop=True)
            st.dataframe(csv_df.set_index('id'))
