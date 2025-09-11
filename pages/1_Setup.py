import streamlit as st

from data import clear_data, load_profile, save_profile

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
    user_name = st.text_input("Name", value=profile.get("name", ""))
    rest_seconds = st.number_input(
        "Rest time between sets (seconds)",
        min_value=0,
        step=1,
        value=int(profile.get("rest_seconds", 0)),
    )
    workout_days = st.multiselect(
        "Workout Days", weekdays, default=profile.get("workout_days", [])
    )
    workouts = {}
    existing_workouts = profile.get("workouts", {})
    for day in workout_days:
        st.markdown(f"### {day}")
        count = st.number_input(
            "Number of workouts",
            min_value=1,
            step=1,
            value=len(existing_workouts.get(day, [])) or 1,
            key=f"{day}_count",
        )
        day_workouts = []
        for i in range(int(count)):
            cols = st.columns(3)
            w = existing_workouts.get(day, [])
            w_i = w[i] if i < len(w) else {}
            workout_name = cols[0].text_input(
                "Workout",
                value=w_i.get("name", ""),
                key=f"{day}_{i}_name",
            )
            sets = cols[1].number_input(
                "Sets",
                min_value=1,
                step=1,
                value=int(w_i.get("sets", 1) or 1),
                key=f"{day}_{i}_sets",
            )
            reps = cols[2].number_input(
                "Reps",
                min_value=1,
                step=1,
                value=int(w_i.get("reps", 1) or 1),
                key=f"{day}_{i}_reps",
            )
            day_workouts.append({"name": workout_name, "sets": sets, "reps": reps})
        workouts[day] = day_workouts
    submitted = st.form_submit_button("Save")

if submitted:
    save_profile(
        {
            "name": user_name,
            "rest_seconds": rest_seconds,
            "workout_days": workout_days,
            "workouts": workouts,
        }
    )
    st.success("Profile saved")

if st.button("Clear All Data"):
    clear_data()
    st.success("All data cleared")
    if hasattr(st, "rerun"):
        st.rerun()
    else:  # Streamlit < 1.22
        st.experimental_rerun()
