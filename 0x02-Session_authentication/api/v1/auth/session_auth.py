#!/usr/bin/env python3
"""
Module for authentication using Session auth
"""

from .auth import Auth  # Import the base Auth class
from models.user import User  # Import the User model class
from uuid import uuid4  # Import uuid4 for generating session IDs


class SessionAuth(Auth):
    """Handles user authentication using session IDs.

    Attributes:
        user_id_by_session_id (dict): A dictionary mapping session IDs to user IDs.

    Methods:
        create_session:
            Creates a new session for the given user ID and returns the session ID.
        user_id_for_session_id:
            Retrieves the user ID associated with a given session ID.
        current_user:
            Retrieves the User object for the authenticated session.
        destroy_session:
            Destroys the session associated with the given request.

    """

    user_id_by_session_id = {}  # Dictionary to store session IDs mapped to user IDs

    def create_session(self, user_id: str = None) -> str:
        """Creates a new session for the given user ID.

        Args:
            user_id (str): The user ID for which the session is created.

        Returns:
            str: The generated session ID.

        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())  # Generate a new UUID as the session ID
        self.user_id_by_session_id[session_id] = user_id  # Map session ID to user ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID associated with a session ID.

        Args:
            session_id (str): The session ID for which to retrieve the user ID.

        Returns:
            str: The user ID associated with the given session ID.

        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)  # Retrieve user ID from session ID

    def current_user(self, request=None):
        """Retrieves the User object for the authenticated session.

        Args:
            request (Any): The request object containing the session cookie.

        Returns:
            User: The User object associated with the authenticated session.

        """
        session_cookie = self.session_cookie(request)  # Retrieve session cookie from request
        user_id = self.user_id_for_session_id(session_cookie)  # Retrieve user ID from session ID
        user = User.get(user_id)  # Retrieve User object using user ID
        return user

    def destroy_session(self, request=None) -> bool:
        """Destroys the session associated with the given request.

        Args:
            request (Any): The request object containing the session cookie.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.

        """
        if request is None:
            return False

        session_cookie = self.session_cookie(request)  # Retrieve session cookie from request
        if session_cookie is None:
            return False

        user_id = self.user_id_for_session_id(session_cookie)  # Retrieve user ID from session ID
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_cookie]  # Delete session entry
        return True  # Return True indicating successful session destruction