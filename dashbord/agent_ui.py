import streamlit as st

from data.database import init_db, get_latest_case

init_db()

st.title("Agent Dashboard")

case = get_latest_case()

if case is None:
    st.info("No escalated cases available yet.")

else:
    st.subheader("Frustration Score")
    st.write(case["frustration"])

    st.subheader("AI Summary")
    st.write(case["summary"])

    st.subheader("Full Chat")
    st.text(case["raw_chat"])