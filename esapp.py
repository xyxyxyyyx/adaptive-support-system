import streamlit as st
import time

from core.chatbot import get_bot_reply
from core.frustration import calculate_frustration
from core.escalation import (
    should_escalate,
    classify_escalation_type,
    get_escalation_message,
    requests_human_support,
    create_case
)
from data.database import init_db, save_message, save_case

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

if "escalation_type" not in st.session_state:
    st.session_state.escalation_type = "general"

if "escalation_unlocked" not in st.session_state:
    st.session_state.escalation_unlocked = False

# -------------------------
# DISPLAY CHAT HISTORY
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------------
# HANDLE ESCALATION
# -------------------------
def handle_escalation():
    st.session_state.escalated = True
    st.session_state.escalation_suggested = False

    save_message("system", "ESCALATION_TRIGGERED")

    case = create_case(
        st.session_state.messages,
        st.session_state.frustration_score
    )

    save_case(
        case["frustration"],
        case["summary"],
        case["messages"]
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": "Connecting you to human support...",
        "time": time.time()
    })

# -------------------------
# INPUT
# -------------------------
if not st.session_state.escalated:
    user_input = st.chat_input("Type your message...")
else:
    user_input = None
    st.info("Your conversation has been sent to human support.")

if user_input:
    # Save user message
    user_message = {
        "role": "user",
        "content": user_input,
        "time": time.time()
    }

    # Messages before the current user input
    previous_messages = st.session_state.messages.copy()

    st.session_state.messages.append(user_message)
    save_message("user", user_input)

    # -------------------------
    # DIRECT ESCALATION
    # Only available after escalation has been unlocked
    # -------------------------
    if (
        st.session_state.escalation_unlocked
        and requests_human_support(user_input)
    ):
        handle_escalation()
        st.rerun()

    # -------------------------
    # NORMAL CHAT FLOW
    # -------------------------
    change = calculate_frustration(
        user_input,
        previous_messages
    )

    st.session_state.frustration_score += change

    st.session_state.escalation_type = classify_escalation_type(
        user_input,
        previous_messages
    )

    bot_reply = get_bot_reply(user_input)

    # Small simulated typing delay based on response length
    typing_delay = min(0.1 + len(bot_reply) * 0.002, 0.4)

    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.write("Typing...")
        time.sleep(typing_delay)
        typing_placeholder.empty()

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
    st.session_state.escalation_unlocked = True

# -------------------------
# ESCALATION UI (SUGGESTION LAYER)
# -------------------------
if st.session_state.escalation_suggested and not st.session_state.escalated:

    message = get_escalation_message(
        st.session_state.escalation_type
    )
    st.warning(message)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Connect to human support"):
            handle_escalation()
            st.rerun()

    with col2:
        if st.button("No, continue chatting"):
            st.session_state.escalation_declined = True
            st.session_state.escalation_suggested = False

# -------------------------
# FALLBACK MESSAGE AFTER DECLINE
# -------------------------
if (
    st.session_state.escalation_unlocked
    and st.session_state.escalation_declined
    and not st.session_state.escalated
):
    st.info(
        "No problem, we’ll continue helping here. "
        "You can type 'contact human support' anytime if you want human assistance."
    )