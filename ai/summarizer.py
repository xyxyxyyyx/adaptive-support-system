def generate_summary(messages):
    user_msgs = [m["content"] for m in messages if m["role"] == "user"]

    summary = "User issue summary:\n"

    if any("error" in m.lower() for m in user_msgs):
        summary += "- Error-related issue\n"

    if any("not working" in m.lower() for m in user_msgs):
        summary += "- Feature malfunction\n"

    summary += "\nRecent messages:\n"
    summary += "\n".join(user_msgs[-5:])

    return summary