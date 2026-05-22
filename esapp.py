import streamlit as st
import time

from core.chatbot import get_bot_reply
from core.frustration import calculate_frustration
from core.escalation import (
    should_escalate,
    classify_escalation_type,
    get_escalation_message
)
from data.database import init_db, save_message

# -------------------------
# INIT DATABASE (IMPORTANT)
# -------------------------
init_db()

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

if "escalation_suggested" not in st.session_state:
    st.session_state.escalation_suggested = False

if "escalation_declined" not in st.session_state:
    st.session_state.escalation_declined = False

if "escalated" not in st.session_state:
    st.session_state.escalated = False

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
    # special command check
    st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": time.time()
        })

    if st.session_state.escalation_suggested or st.session_state.escalation_declined:
            st.session_state.escalated = True
            st.session_state.escalation_suggested = False

            save_message("user", user_input)
            save_message("system", "ESCALATION_TRIGGERED")

            st.session_state.messages.append({
                "role": "assistant",
                "content": "Connecting you to a human support agent..."
            })

    else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "We’ll continue helping here first and try to resolve your issue together."
            })

    st.rerun()


    # save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": time.time()
    })

    save_message("user", user_input)

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

    save_message("assistant", bot_reply)

    st.rerun()

# -------------------------
# DEBUG DISPLAY
# -------------------------
st.write("Frustration score:", st.session_state.frustration_score)

# -------------------------
# ESCALATION LOGIC
# -------------------------
if (
    len(st.session_state.messages) > 0
    and should_escalate(st.session_state.frustration_score)
    and not st.session_state.escalation_declined
    and not st.session_state.escalated
):
    st.session_state.escalation_suggested = True

# -------------------------
# ESCALATION UI (SUGGESTION LAYER)
# -------------------------
if st.session_state.escalation_suggested and not st.session_state.escalated:

    message = get_escalation_message("general")
    st.warning(message)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Connect to human support"):
            st.session_state.escalated = True
            st.session_state.escalation_suggested = False

            save_message("system", "ESCALATION_TRIGGERED")
            st.success("Escalation sent to human support")

    with col2:
        if st.button("No, continue chatting"):
            st.session_state.escalation_declined = True
            st.session_state.escalation_suggested = False

# -------------------------
# FALLBACK MESSAGE AFTER DECLINE
# -------------------------
if st.session_state.escalation_declined:
    st.info(
        "No problem, we’ll continue helping here. "
        "You can type 'contact human support' anytime if you want human assistance."
    )