import json
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path("data")
PROFILE_FILE = DATA_DIR / "profile.json"
LOG_FILE = DATA_DIR / "workout_log.csv"

DATA_DIR.mkdir(exist_ok=True)


def load_profile() -> dict:
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE) as f:
            return json.load(f)
    return {"name": "", "weekly_plan": ""}


def save_profile(profile: dict) -> None:
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f)


def load_logs() -> pd.DataFrame:
    if LOG_FILE.exists():
        return pd.read_csv(LOG_FILE, parse_dates=["date"])
    return pd.DataFrame(columns=["date", "exercise", "weight", "reps"])


def save_logs(df: pd.DataFrame) -> None:
    df.to_csv(LOG_FILE, index=False)


st.title("Personal Workout Tracker")
page = st.sidebar.radio("Navigate", ["Setup", "Log Workout", "Progress"])

if page == "Setup":
    st.header("User Setup")
    profile = load_profile()
    with st.form("setup"):
        name = st.text_input("Name", value=profile.get("name", ""))
        weekly_plan = st.text_area(
            "Weekly Workout Plan", value=profile.get("weekly_plan", "")
        )
        submitted = st.form_submit_button("Save")
    if submitted:
        save_profile({"name": name, "weekly_plan": weekly_plan})
        st.success("Profile saved")

elif page == "Log Workout":
    st.header("Log Workout")
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

elif page == "Progress":
    st.header("Progress")
    logs = load_logs()
    if logs.empty:
        st.info("No workout data yet")
    else:
        option = st.selectbox("Exercise", sorted(logs["exercise"].unique()))
        subset = logs[logs["exercise"] == option]
        st.line_chart(subset.set_index("date")["weight"])
        st.dataframe(subset.sort_values("date", ascending=False))
