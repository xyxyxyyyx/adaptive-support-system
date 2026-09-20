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
        "I'm sorry my answers haven't been as helpful as they should be. "
        "If you'd like, I can connect you with one of our team members who can listen and get this sorted out for you right away."
    ),

    "urgency": (
        "Your time is important, and I want to make sure we fix this for you quickly. "
        "Would you like me to hand you over to someone on our team who can help you right now?"
    ),

    "confusion": (
        "This looks like a situation that needs a human touch to get exactly right. "
        "I can help connect you with one of our team members if you'd like."
    ),

    "general": (
        "This looks like something that needs a bit more care than I can provide by myself. "
        "Would you like to talk directly with one of our friendly team members?"
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

def requests_human_support(user_input):
    text = user_input.lower()

    trigger_phrases = [
        "contact human support",
        "human support",
        "talk to a human",
        "speak to a human"
    ]

    return any(phrase in text for phrase in trigger_phrases)
        