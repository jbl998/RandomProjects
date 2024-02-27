import streamlit as st
import pandas as pd
import numpy as np
import datetime

tab1, tab2 = st.tabs(["Race time to pace", "Pace to Race Time"])

now = datetime.datetime.now()
d = now.day
mo = now.month
y = now.year


def pacetotime(min, sec, dist):
    total_seconds = dist * (min * 60 + sec) / 1000
    h = int(np.floor(total_seconds / (60**2)))
    m = int((np.floor(total_seconds) - h * 60**2) / 60)
    s = int(total_seconds - h * 60**2 - m * 60)
    return datetime.datetime(year=y, month=mo, day=d, hour=h, minute=m, second=s)


def timetopace(hrs, min, sec, dist):
    total_seconds = hrs * 3600 + min * 60 + sec
    secperkm = total_seconds / (dist / 1000)
    h, rest = divmod(secperkm, 3600)
    m, s = divmod(rest, 60)
    s2, mys = divmod(s, 1)
    return int(h), int(m), int(s2), int(mys * 1000000)


def speed(hrs, min, sec, dist):
    total_hours = hrs + min / 60 + sec / 3600
    speed = dist / total_hours
    return round(speed, 2)


dist_m = [1000, 5000, 10000, 21097.5, 42195]
dist_km = [x / 1000 for x in dist_m]
record = [
    datetime.datetime(year=y, month=mo, day=d, hour=0, minute=4, second=23),  # 1000m
    datetime.datetime(year=y, month=mo, day=d, hour=0, minute=23, second=22),  # 5000m
    datetime.datetime(year=y, month=mo, day=d, hour=0, minute=47, second=52),  # 10000m
    datetime.datetime(year=y, month=mo, day=d, hour=2, minute=30, second=0),  # Half
    datetime.datetime(year=y, month=mo, day=d, hour=7, minute=0, second=0),
]  # Marathon

record_pace = [0 * i for i in range(len(record))]
for i in range(len(dist_m)):
    time = record[i]
    h, m, s, mys = timetopace(
        hrs=time.hour, min=time.minute, sec=time.second, dist=dist_m[i]
    )
    record_pace[i] = datetime.time(
        hour=h, minute=m, second=s, microsecond=mys
    ).strftime("%M:%S.%f")[:8]

record2 = [item.strftime("%H:%M:%S") for item in record]

with tab1:
    st.subheader("Time")
    col1, col2, col3 = st.columns(3)
    with col1:
        h = st.number_input(label="H", min_value=0, max_value=23, value=1)
    with col2:
        m = st.number_input(label="M", min_value=0, max_value=59, value=49)
    with col3:
        s = st.number_input(label="S", min_value=0, max_value=59, value=59)
    time = datetime.time(hour=h, minute=m, second=s)
    st.subheader("Pace to run")
    d_choice_km = st.radio("Choose distance", options=dist_km, index=3)
    d_choice_m = int(d_choice_km * 1000)
    hour, min, sec, mys = timetopace(hrs=h, min=m, sec=s, dist=d_choice_m)
    timezero = datetime.datetime(
        year=y, month=mo, day=d, hour=0, minute=0, second=0, microsecond=0
    )
    pace = datetime.datetime(
        year=y, month=mo, day=d, hour=hour, minute=min, second=int(sec), microsecond=mys
    )
    spd = speed(hrs=h, min=m, sec=s, dist=d_choice_km)
    delta = datetime.timedelta(hours=hour, minutes=min, seconds=sec, microseconds=mys)
    st.text(
        f"This will require you to run at pace {pace.strftime('%M:%S.%f')[:7]} or {spd}km/h"
    )

    st.subheader("Split times")
    d_split = st.radio("Choose split (km)", options=[1, 2, 5], index=0)
    antal, rest = divmod(d_choice_m, 1000 * d_split)
    d_range = [d_split * x for x in range(1, antal + 1)]

    t_range = [
        (timezero + d_split * x * delta).strftime("%H:%M:%S.%f")[:10]
        for x in range(1, antal + 1)
    ]
    if rest > 0:
        d_range.append(d_choice_km)
        t_range.append(time.strftime("%H:%M:%S.%f")[:10])
    data_pace = pd.DataFrame(
        data={"Distance (km)": d_range, "Time (HH:MM:SS.N)": t_range}
    )
    st.dataframe(data_pace, hide_index=True, use_container_width=True)

with tab2:
    st.subheader("Pace")
    col1, col2 = st.columns(2)
    with col1:
        minutes = st.number_input(label="Minutes", min_value=0, max_value=20, value=6)
    with col2:
        seconds = st.number_input(label="Seconds", min_value=0, max_value=59, value=0)

    st.text(
        f"This is a speed of {np.round(60 * 60 / (minutes * 60 + seconds), 2)} km/h"
    )

    st.subheader("Time to run")

    time = [pacetotime(minutes, seconds, item) for item in dist_m]
    data = pd.DataFrame(
        data={"Distance": dist_m, "Time": time, "Record": record},
        columns=["Distance", "Time", "Record"],
    )

    time2 = [item.strftime("%H:%M:%S") for item in time]
    data2 = pd.DataFrame(
        data={
            "Distance": dist_m,
            "Time": time2,
            "Record": record2,
            "Record pace": record_pace,
        },
        columns=["Distance", "Time", "Record", "Record pace"],
    )

    st.dataframe(data2)

    # Plots
    st.line_chart(data=data, x="Distance")
