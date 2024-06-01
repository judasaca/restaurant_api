import re
from typing import List

from fastapi import HTTPException, status
from pydantic import ValidationError


def validate_password(password: str) -> None:
    """
    Check if password is valid
    returns: None
    Raises: ValidationError with 422 status if password is not valid
    """
    messages: List[str] = []
    if len(password) < 10:
        messages.append("Password must have more than 10 characters")

    if not re.search(r"[a-z]", password):
        messages.append("Passwords must have at least 1 lowercase letter")

    if not re.search(r"[A-Z]", password):
        messages.append("Password must have at least 1 uppercase letter")

    # Check if the password contains at least one of the specified special characters
    if not re.search(r"[!@#?\]]", password):
        messages.append(
            "Password must contain at least one of the following characters: '[!@$?]'"
        )
    if len(messages) > 0:
        raise ValueError(
            f'Invalid password: {" - ".join(messages)}',
        )
