#!/usr/bin/env python3
"""authentication
"""
import bcrypt
from db import DB
from user import User



def _hash_password(Password: str, ) -> bytes:
    """ a function that takes in password, and salt and hash it
    args:
        password(str): password to be hashed

    Returns:
        bytes: hashed password
    """
    password_in_byte = Password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_in_byte, bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
        
    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the provided email and password."""
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")

            hashed_password = _hash_password(password)

            new_user = self._db.add_user(email=email, hashed_password=hashed_password)
            return new_user
        except Exception as e:
            raise ValueError("User could not be registered") from e