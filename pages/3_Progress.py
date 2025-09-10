import streamlit as st

from data import load_logs

st.title("Progress")

logs = load_logs()
if logs.empty:
    st.info("No workout data yet")
else:
    option = st.selectbox("Exercise", sorted(logs["exercise"].unique()))
    subset = logs[logs["exercise"] == option]
    st.line_chart(subset.set_index("date")["weight"])
    st.dataframe(subset.sort_values("date", ascending=False))
