import datetime
import pandas as pd
import streamlit as st

from data import load_logs, load_profile, save_logs

st.title("Log Workout")

profile = load_profile()
today = datetime.datetime.now().strftime("%A")
day_workouts = profile.get("workouts", {}).get(today, [])

if st.session_state.get("workout_day") != today:
    st.session_state.workout_day = today
    st.session_state.workout_index = 0

logs = load_logs()

if not day_workouts:
    st.info("No workouts scheduled for today.")
else:
    idx = st.session_state.get("workout_index", 0)
    if idx < len(day_workouts):
        w = day_workouts[idx]
        st.subheader(f"{w['name']} - {w['sets']} sets x {w['reps']} reps")
        with st.form("log"):
            weight = st.number_input("Weight", min_value=0.0, step=1.0)
            reps = st.number_input("Reps", min_value=0, step=1, value=w["reps"])
            submitted = st.form_submit_button("Complete Workout")
        if submitted:
            new_log = {
                "date": pd.to_datetime(datetime.date.today()),
                "exercise": w["name"],
                "weight": weight,
                "reps": reps,
            }
            logs = pd.concat([logs, pd.DataFrame([new_log])], ignore_index=True)
            save_logs(logs)
            st.session_state.workout_index = idx + 1
            st.success(f"Completed {w['name']}")
    else:
        st.success(
            "All workouts completed for today! Head to the Progress page to review your performance."
        )
        st.markdown("[View progress](./Progress)")

