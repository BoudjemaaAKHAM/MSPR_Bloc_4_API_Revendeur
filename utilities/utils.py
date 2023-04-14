import re


def is_valid_email(email: str) -> bool:
    """
    Check if an email is valid
    :param email:
    :return:
    """
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return bool(re.match(pattern, email))
