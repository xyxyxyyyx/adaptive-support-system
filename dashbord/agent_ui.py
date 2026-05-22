import streamlit as st
from ai.summarizer import generate_summary

st.title("Agent Dashboard")

# fake example data (later from database)
case = {
    "messages": [],
    "frustration": 7
}

st.subheader("Frustration Score")
st.write(case["frustration"])

st.subheader("AI Summary")
st.write(generate_summary(case["messages"]))

st.subheader("Full Chat")
for m in case["messages"]:
    st.write(f"{m['role']}: {m['content']}")