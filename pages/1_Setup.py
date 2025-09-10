import streamlit as st

from data import load_profile, save_profile

st.title("User Setup")

profile = load_profile()
weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

with st.form("setup"):
    name = st.text_input("Name", value=profile.get("name", ""))
    workout_days = st.multiselect(
        "Workout Days", weekdays, default=profile.get("workout_days", [])
    )
    workouts = {}
    existing_workouts = profile.get("workouts", {})
    for day in workout_days:
        st.markdown(f"### {day}")
        cols = st.columns(3)
        w = existing_workouts.get(day, {})
        workout_name = cols[0].text_input(
            "Workout", value=w.get("name", ""), key=f"{day}_name"
        )
        sets = cols[1].number_input(
            "Sets", min_value=1, step=1, value=int(w.get("sets", 1) or 1), key=f"{day}_sets"
        )
        reps = cols[2].number_input(
            "Reps", min_value=1, step=1, value=int(w.get("reps", 1) or 1), key=f"{day}_reps"
        )
        workouts[day] = {"name": workout_name, "sets": sets, "reps": reps}
    submitted = st.form_submit_button("Save")

if submitted:
    save_profile({"name": name, "workout_days": workout_days, "workouts": workouts})
    st.success("Profile saved")
