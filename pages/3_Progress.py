import streamlit as st
import altair as alt
import pandas as pd

from data import load_logs, load_profile

st.title("Progress")

profile = load_profile()
logs = load_logs()
if logs.empty:
    st.info("No workout data yet")
else:
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    workouts_by_day = profile.get("workouts", {})
    days = [d for d in day_order if d in workouts_by_day]
    if not days:
        st.info("No workouts configured. Please set up your profile.")
    else:
        day = st.selectbox("Workout Day", days)
        for w in workouts_by_day.get(day, []):
            name = w["name"]
            target_reps = w.get("reps", 1) or 1
            subset = logs[logs["exercise"] == name].copy()
            if subset.empty:
                st.write(f"No data for {name}")
                continue
            subset = subset.sort_values("date")
            subset["set_idx"] = subset.groupby("date").cumcount()
            subset["date_time"] = subset["date"] + pd.to_timedelta(
                subset["set_idx"], unit="s"
            )
            subset["ratio"] = (subset["reps"] / target_reps).clip(0, 1)

            st.subheader(name)

            reps_chart = (
                alt.Chart(subset)
                .mark_line(color="white")
                .encode(x=alt.X("date_time:T", title="Date"), y="reps:Q")
                + alt.Chart(subset)
                .mark_circle(size=80)
                .encode(
                    x=alt.X("date_time:T", title="Date"),
                    y="reps:Q",
                    color=alt.Color(
                        "ratio:Q",
                        scale=alt.Scale(domain=[0, 1], range=["red", "green"]),
                        legend=None,
                    ),
                )
            )
            weight_chart = (
                alt.Chart(subset)
                .mark_line(point=True, color="white")
                .encode(x=alt.X("date_time:T", title="Date"), y="weight:Q")
            )

            st.altair_chart(reps_chart, use_container_width=True)
            st.altair_chart(weight_chart, use_container_width=True)
