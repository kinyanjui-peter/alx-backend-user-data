#!/usr/bin/env python3
"""authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """ a function that takes in password, and salt and hash it
    args:
        password(str): password to be hashed

    Returns:
        bytes: hashed password
    """
    password_in_byte = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_in_byte, bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """_summary_

    Raises:
        ValueError: description

    Returns:
        str: description
    """
    id = uuid4()
    return str(id)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, Password: str) -> User:
        """Registers a new user with the provided email and password.
        Args:
            email (str): The email address of the new user.
            password (str): The password of the new user.

        Returns:
            User: The newly registered User object.
        """
        try:
            # find the user with the given email
            self._db.find_user_by(email=email)
        except NoResultFound:
            # add user to database
            registered_user = self._db.add_user(
                email, _hash_password(Password))
            return registered_user

        else:
            # if user already exists, throw error
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """_summary_

        Args:
            email (str): description
            password (str): description

        Returns:
            Boolean: description
        """
        try:
            # find the user with the given email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        # check validity of password
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """_summary_

        Args:
            email (str): description

        Returns:
            str: description
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """_summary_

        Args:
            session_id (_type_): description
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: str) -> None:
        """_summary_

        Args:
            user_id (str): description
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            user.session_id = None
            return None

    def get_reset_password_token(self, email: str) -> str:
        """_summary_

        Args:
            email (str): description

        Returns:
            str: description
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            user.reset_token = _generate_uuid()
            return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """_summary_

        Args:
            reset_token (str): description
            password (str): description
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            return None
