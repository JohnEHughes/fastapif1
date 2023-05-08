import streamlit as st
import pandas as pd

from streamlit_utils.config import get_driver_data


st.set_page_config(
    page_title="F1 Stats",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("F1 Driver stats")
st.text("Simple stats on current Formula 1 drivers")
st.sidebar.image("driver.ico")
driver_data = pd.DataFrame(get_driver_data()).reset_index(drop=True)
driver_data['dob'] = driver_data['dob'].apply(lambda x: x[:10])
st.dataframe(driver_data.set_index('last_name'), height=350)

st.divider()

with st.expander("Race Wins"):
    st.subheader("Race Wins per Driver")

    name_most_wins = driver_data.loc[driver_data['total_race_wins'].idxmax()].last_name
    most_wins = driver_data["total_race_wins"].max()
    ave_wins = driver_data["total_race_wins"].mean().round(1)
    num_winning_drivers = driver_data["total_race_wins"].gt(0).sum()

    col1, col2 = st.columns(spec=[1, 3])

    col1.metric(label=f"Most Wins - {name_most_wins}", value=most_wins)
    col1.metric(label=f"Ave Wins Per Driver", value=ave_wins)
    col1.metric(label=f"No. Winning Drivers", value=num_winning_drivers)
    col2.bar_chart(data=driver_data, x="last_name", y="total_race_wins")

with st.expander("Total Points per Driver"):
    st.subheader("Total Points per Driver")

    name_most_points = driver_data.loc[driver_data['total_points'].idxmax()].last_name
    most_points = driver_data["total_points"].max()
    ave_points = driver_data["total_points"].mean().round(1)
    more_than_thousand = num_winning_drivers = driver_data["total_points"].gt(1000).sum()

    col1, col2 = st.columns(spec=[3, 1])    
    col1.area_chart(data=driver_data, x="last_name", y="total_points")
    col2.metric(label=f"Most Points - {name_most_points}", value=most_points)
    col2.metric(label=f"Ave Points Per Driver", value=ave_points)
    col2.metric(label=f"No. 1000pts+", value=more_than_thousand)