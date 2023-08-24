import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import pytz
#from streamlit_autorefresh import st_autorefresh

tab1, tab2 = st.tabs(["Pace to Race Time", "tab2"])


with tab1:
    st.subheader("Pace")
    col1, col2 = st.columns(2)
    with col1:
        minutes = st.number_input(label="Minutes", min_value=0, max_value=10, value=6)
    with col2:
        seconds = st.number_input(label="Seconds", min_value=0, max_value=59, value=0)

    st.text(f"This is a speed of {np.round(60 * 60 / (minutes * 60 + seconds), 2)} km/h")

    st.subheader("Time to run")
    # chosen_distance = st.number_input("Distance", min_value=0, max_value=42195, value=10000)
    def timetorun(min, sec, dist):
        total_seconds = dist * (min * 60 + sec) / 1000
        h = int(np.floor(total_seconds / (60 ** 2)))
        m = int((np.floor(total_seconds) - h * 60 ** 2) / 60)
        s = int(total_seconds - h * 60 ** 2 - m * 60)
        return datetime.time(hour=h, minute=m, second=s)

    dist = [1000,
            5000,
            10000,
            21097.5,
            42195]

    time = [timetorun(minutes, seconds, item) for item in dist]
    record = [datetime.time(hour=0, minute=4, second=51), # 1000m
              datetime.time(hour=0, minute=25, second=20), # 5000m
              datetime.time(hour=0, minute=56, second=58), # 10000m
              datetime.time(hour=23, minute=59, second=59), # Half
              datetime.time(hour=23, minute=59, second=59)] # Marathon
    d = {"Distance": dist, "Time": time, "Record": record}
    data = d
    st.dataframe(data)
