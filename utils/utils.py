import re


def validate_project_input(user_input: str) -> str | None:
    # Strip whitespace
    user_input = user_input.strip()

    # Check length
    if len(user_input) == 0 or len(user_input) > 500:
        return None

    # Allow only letters, numbers, spaces, dash and underscore
    if not re.fullmatch(r"[A-Za-z0-9 _-]+", user_input):
        return None

    return user_input
