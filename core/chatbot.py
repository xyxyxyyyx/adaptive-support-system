def get_bot_reply(user_input):
    user_input = user_input.lower()

    if "password" in user_input:
        return "Try resetting your password in settings."

    elif "login" in user_input:
        return "Please check your login credentials and try again."

    elif "help" in user_input:
        return "Sure, what do you need help with?"

    else:
        return "Can you provide more details about your issue?"