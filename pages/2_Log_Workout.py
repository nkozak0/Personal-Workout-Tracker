import pandas as pd
import streamlit as st

from data import load_logs, save_logs

st.title("Log Workout")

logs = load_logs()
with st.form("log"):
    date = st.date_input("Date")
    exercise = st.text_input("Exercise")
    weight = st.number_input("Weight", min_value=0.0, step=1.0)
    reps = st.number_input("Reps", min_value=0, step=1)
    submitted = st.form_submit_button("Add")
if submitted:
    new_log = {
        "date": pd.to_datetime(date),
        "exercise": exercise,
        "weight": weight,
        "reps": reps,
    }
    logs = pd.concat([logs, pd.DataFrame([new_log])], ignore_index=True)
    save_logs(logs)
    st.success("Workout added")
