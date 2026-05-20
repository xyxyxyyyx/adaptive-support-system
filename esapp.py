import streamlit as st
import time

from core.chatbot import get_bot_reply
from core.frustration import calculate_frustration
from core.escalation import (
    should_escalate,
    classify_escalation_type,
    get_escalation_message
)

# -------------------------
# PAGE SETUP
# -------------------------
st.title("Adaptive Support System")

# -------------------------
# STATE INIT
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "frustration_score" not in st.session_state:
    st.session_state.frustration_score = 0

# -------------------------
# DISPLAY CHAT HISTORY
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------------
# INPUT
# -------------------------
user_input = st.chat_input("Type your message...")

if user_input:

    # save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": time.time()
    })

    # frustration update
    previous_messages = st.session_state.messages[:-1]

    change = calculate_frustration(
        user_input,
        previous_messages,
    )

    st.session_state.frustration_score += change

    # bot response
    bot_reply = get_bot_reply(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply,
        "time": time.time()
    })

    st.rerun()

# -------------------------
# DEBUG DISPLAY
# -------------------------
st.write("Frustration score:", st.session_state.frustration_score)

# -------------------------
# ESCALATION LOGIC
# -------------------------
if len(st.session_state.messages) > 0:

    last_user = None

    for msg in reversed(st.session_state.messages):
        if msg["role"] == "user":
            last_user = msg
            break

    if last_user and should_escalate(st.session_state.frustration_score):

        esc_type = classify_escalation_type(
            last_user["content"],
            st.session_state.messages
        )

        message = get_escalation_message(esc_type)

        st.warning(message)

        if st.button("Connect to human support"):
            st.success("Escalation sent to human support")