import re

WEIGHTS = {
    "caps": 2,
    "punctuation": 1,
    "repetition": 3,
    "inactivity": 2,
    "spam_penalty": -3
}

def calculate_frustration(user_input, previous_messages):

    score = 0

    # -------------------------
    # SIGNAL 1: CAPS LOCK
    # -------------------------
    if user_input.isupper():
        score += WEIGHTS["caps"]

    # -------------------------
    # SIGNAL 2: Aggressive punctuation
    # -------------------------
    if "!!!" in user_input or "???" in user_input:
        score += WEIGHTS["punctuation"]

    # -------------------------
    # SIGNAL 3: Repetition (behavioral)
    # -------------------------
    score += repetition_score(user_input, previous_messages)

    # -------------------------
    # SIGNAL 4: Spam detection
    # -------------------------
    if is_spam(user_input):
        score += WEIGHTS["spam_penalty"]

    # -------------------------
    # SIGNAL 5: Inactivity (contextual)
    # -------------------------
    score += inactivity_score(previous_messages)

    return score


def is_spam(text):

    # too many symbols
    symbol_count = len(re.findall(r'[^a-zA-Z0-9\s]', text))

    if len(text) > 0:
        symbol_ratio = symbol_count / len(text)

        if symbol_ratio > 0.6:
            return True

    # random keyboard smash
    if len(text.split()) == 1 and len(text) > 12:
        return True

    return False

# Repetition detection
def repetition_score(user_input, previous_messages):
    current = set(user_input.lower().strip().split())

    # check if user repeats similar messages
    for msg in previous_messages[-5:]:
        if msg["role"] == "user":
            past = set(msg["content"].lower().strip().split())

            # exact repetition
            if user_input.lower().strip() == msg["content"].lower().strip():
                return 3

            # partial semantic overlap (safe version)
            elif len(current) > 0:
                overlap = current & past
                overlap_ratio = len(overlap) / len(current)

                if overlap_ratio > 0.7:
                    return 2

    return 0

# Inactivity detection
def inactivity_score(previous_messages, threshold_seconds=60):

    if len(previous_messages) < 2:
        return 0
    
    last_msg = previous_messages[-1]

    # check if last message was assistant
    if last_msg["role"] == "assistant":
        last_time = last_msg.get("time", None)

        if last_time:
            import time
            delay = time.time() - last_time

            if delay > threshold_seconds:
                return 2
            
    return 0