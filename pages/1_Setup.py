import streamlit as st

from data import load_profile, save_profile

st.title("User Setup")

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
