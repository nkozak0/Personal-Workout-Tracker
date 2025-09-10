import datetime
import time
import pandas as pd
import streamlit as st

from data import load_logs, load_profile, save_logs

st.title("Log Workout")

profile = load_profile()
rest_seconds = profile.get("rest_seconds", 0)
today = datetime.datetime.now().strftime("%A")
day_workouts = profile.get("workouts", {}).get(today, [])

if st.session_state.get("workout_day") != today:
    st.session_state.workout_day = today
    st.session_state.workout_index = 0
    st.session_state.set_index = 0

logs = load_logs()

if not day_workouts:
    st.info("No workouts scheduled for today.")
else:
    w_idx = st.session_state.get("workout_index", 0)
    if w_idx < len(day_workouts):
        w = day_workouts[w_idx]
        set_idx = st.session_state.get("set_index", 0)
        total_sets = int(w.get("sets", 1))
        st.subheader(
            f"{w['name']} - Set {set_idx + 1} of {total_sets} ({w['reps']} reps)"
        )
        with st.form("log"):
            weight = st.number_input("Weight", min_value=0.0, step=1.0)
            reps = st.number_input("Reps", min_value=0, step=1, value=w["reps"])
            submitted = st.form_submit_button("Log Set")
        if submitted:
            new_log = {
                "date": pd.to_datetime(datetime.date.today()),
                "exercise": w["name"],
                "weight": weight,
                "reps": reps,
            }
            logs = pd.concat([logs, pd.DataFrame([new_log])], ignore_index=True)
            save_logs(logs)
            set_idx += 1
            if set_idx >= total_sets:
                st.session_state.workout_index = w_idx + 1
                st.session_state.set_index = 0
                st.success(f"Completed {w['name']}")
            else:
                st.session_state.set_index = set_idx
                st.success(f"Logged set {set_idx} of {w['name']}")
            if rest_seconds > 0 and set_idx < total_sets:
                placeholder = st.empty()
                for remaining in range(rest_seconds, 0, -1):
                    placeholder.metric("Rest", f"{remaining}s")
                    time.sleep(1)
                placeholder.empty()
            st.experimental_rerun()
    else:
        st.success(
            "All workouts completed for today! Head to the Progress page to review your performance."
        )
        st.markdown("[View progress](./Progress)")

