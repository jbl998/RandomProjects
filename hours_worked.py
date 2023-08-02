import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import pytz
#from streamlit_autorefresh import st_autorefresh

# Adds feature for PowerBI-like interface
# https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb
# from st_aggrid import (GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode)

st.set_page_config(
    page_title="Hours worked today", layout="centered", page_icon="⌛"
)  # Fit wide page
st.title("Hours worked")  # Set title of streamlit app
link = "[TimeOut](https://timeout.cloud/be)"
st.markdown(link, unsafe_allow_html=True)
# test = st.slider("Test", datetime.time(0, 0), datetime.time(23, 59), datetime.time(8, 30), datetime.timedelta(seconds=60))
start = st.time_input("What time did you clock in?", datetime.time(8, 30))

Frokostpause = st.checkbox("Do/did you have lunch break today?", value=True)
pause = st.time_input(
    "How long was/is your lunch break?", datetime.time(0, 30), disabled=not Frokostpause
)

lunchtime = st.time_input(
    "When did/does your lunch break start?",
    datetime.time(11, 30),
    disabled=not Frokostpause,
)

lunchbreak_over = datetime.datetime.combine(
    datetime.date.today(), lunchtime
) + datetime.timedelta(
    seconds=((pause.hour * 60 + pause.minute) * 60 + pause.second) * Frokostpause
)

slut = st.time_input("When did/do you clock out?", datetime.datetime.now(pytz.timezone('Europe/Copenhagen')))

dateTimeA = datetime.datetime.combine(datetime.date.today(), start)
dateTimeB = datetime.datetime.combine(datetime.date.today(), lunchtime)
dateTimeC = lunchbreak_over
dateTimeD = datetime.datetime.combine(datetime.date.today(), slut)

seconds = max(
    min(
        (dateTimeB - dateTimeA).total_seconds(),
        (dateTimeD - dateTimeA).total_seconds(),
    ),
    0,
) + max((dateTimeD - dateTimeC).total_seconds(), 0)

hours = np.round(seconds / (60**2), 2)

st.text(
    "You have worked " + str(hours) + " hours today asof " + dateTimeD.strftime("%H:%M")
)

#st_autorefresh(interval=60 * 1000, key="api_update")

# To run, enter the following in a cmd window
# streamlit run "C:\Users\kmo\OneDrive - Better Energy\Documents\Python\hours_worked.py"
