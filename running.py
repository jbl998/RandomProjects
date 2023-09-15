import streamlit as st
import pandas as pd
import numpy as np
import datetime


tab1, tab2 = st.tabs(["Pace to Race Time", "Race time to pace"])

now = datetime.datetime.now()
d = now.day
mo = now.month
y = now.year

def pacetotime(min, sec, dist):
    total_seconds = dist * (min * 60 + sec) / 1000
    h = int(np.floor(total_seconds / (60 ** 2)))
    m = int((np.floor(total_seconds) - h * 60 ** 2) / 60)
    s = int(total_seconds - h * 60 ** 2 - m * 60)
    return datetime.datetime(year=y, month=mo, day=d, hour=h, minute=m, second=s)

def timetopace(hrs, min, sec, dist):
    total_seconds = hrs * 3600 + min * 60 + sec
    secperkm = total_seconds / (dist/1000)
    m, s = divmod(secperkm, 60)
    return int(m), np.round(s,1)


dist = [1000,
        5000,
        10000,
        21097.5,
        42195]
record = [datetime.datetime(year=y, month=mo, day=d, hour=0, minute=4, second=33),  # 1000m
          datetime.datetime(year=y, month=mo, day=d, hour=0, minute=23, second=46),  # 5000m
          datetime.datetime(year=y, month=mo, day=d, hour=0, minute=55, second=13),  # 10000m
          datetime.datetime(year=y, month=mo, day=d, hour=6, minute=0, second=0),  # Half
          datetime.datetime(year=y, month=mo, day=d, hour=6, minute=0, second=0)]   # Marathon

with tab1:
    st.subheader("Pace")
    col1, col2 = st.columns(2)
    with col1:
        minutes = st.number_input(label="Minutes", min_value=0, max_value=20, value=6)
    with col2:
        seconds = st.number_input(label="Seconds", min_value=0, max_value=59, value=0)

    st.text(f"This is a speed of {np.round(60 * 60 / (minutes * 60 + seconds), 2)} km/h")

    st.subheader("Time to run")

    time = [pacetotime(minutes, seconds, item) for item in dist]
    d = {"Distance": dist, "Time": time, "Record": record}

    data = pd.DataFrame(data=d, columns=["Distance", "Time", "Record"])
    st.dataframe(data)

    # Plots
    st.line_chart(data=data, x="Distance")

with tab2:
    st.subheader("Time")
    col1, col2, col3 = st.columns(3)
    with col1:
        h = st.number_input(label="H", min_value=0, max_value=23, value=0)
    with col2:
        m = st.number_input(label="M", min_value=0, max_value=59, value=25)
    with col3:
        s = st.number_input(label="S", min_value=0, max_value=59, value=0)

    st.subheader("Pace to run")
    distance = st.radio("Choose distance", options=dist)
    min, sec = timetopace(hrs=h, min=m, sec=s, dist=distance)
    st.text(f"This will require you to run at pace {min}:{sec}")
