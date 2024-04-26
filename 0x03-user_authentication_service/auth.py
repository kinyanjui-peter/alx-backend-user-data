#!/usr/bin/env python3
"""authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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

    def register_user(self, email: str, Password: str) -> User:
        """Registers a new user with the provided email and password."""
        try:
            # find the user with the given email
            self._db.find_user_by(email=email)
        except NoResultFound:
            # add user to database
            return self._db.add_user(email, _hash_password(Password))

        else:
            # if user already exists, throw error
            raise ValueError('User {} already exists'.format(email))
