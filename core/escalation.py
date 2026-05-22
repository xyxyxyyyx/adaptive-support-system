def should_escalate(frustration_score, threshold = 5):

    return frustration_score >= threshold

def classify_escalation_type(user_input, previous_messages):
    text = user_input.lower()

    # repeatition heavy frustration
    repeated_keywords = ["huh"]

    if any(k in text for k in repeated_keywords):
        return "repetition"
    
    # urgency / emotional escalation
    if user_input.isupper() or "!!!" in user_input:
        return "urgency"
    
    # disengagement pattern (could be empty or vague)
    if len(text.split()) < 3:
        return "confusion"
    
    # default
    return "general"

def get_escalation_message(escalation_type):
    messages = {
        "repetition": (
            "It looks like this issue might still not be resolving clearly. "
            "Would you like me to connect you with a human support agent who can take a closer look?"
        ),

        "urgency": (
            "I want to make sure you get the help you need as quickly as possible. "
            "Would you like to speak with a human support representative?"
        ),

        "confusion": (
             "It seems like things might be a bit unclear right now. "
            "I can connect you with someone who can walk through this with you step by step."
        ),

        "general": (
            "It looks like this issue might need a bit more support. "
            "Would you like to talk to a human agent?"
        )
    }

    return messages.get(escalation_type, messages["general"])

from ai.summarizer import generate_summary

def create_case(messages, score):

    return {
        "messages": messages,
        "frustration": score,
        "summary": generate_summary(messages)
    }
        