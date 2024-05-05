#!/usr/bin/env python3
"""
Module for authentication using Basic auth
"""


from typing import TypeVar
from api.v1.auth.auth import Auth
import base64

from models.user import User


class BasicAuth(Auth):
    """A class for handling Basic Authentication.

    This class implements methods to handle Basic Authentication
    by extracting credentials from authorization headers and
    validating them against user objects.

    Inherits:
        Auth: Base class for authentication.

    Attributes:
        None

    Methods:
        extract_base64_authorization_header:
            Extracts the base64-encoded authorization token from the header.
        decode_base64_authorization_header:
            Decodes the base64-encoded token to retrieve user credentials.
        extract_user_credentials:
            Extracts user email and password from the decoded token.
        user_object_from_credentials:
            Retrieves a User object based on the provided credentials.
        current_user:
            Returns the authenticated User object for the current request.

    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts the base64-encoded authorization token from the header.

        Args:
            authorization_header (str): The authorization header string.

        Returns:
            str: The base64-encoded token extracted from the header.
                 Returns None if the header format is invalid.

        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        token = authorization_header.split(' ')[-1]
        return token

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes the base64-encoded token to retrieve user credentials.

        Args:
            base64_authorization_header (str): The base64-encoded token.

        Returns:
            str: The decoded token containing user credentials.
                 Returns None if decoding fails or input is invalid.

        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header.encode('utf-8')).decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts user email and password from the decoded token.

        Args:
            decoded_base64_authorization_header (str): The decoded token.

        Returns:
            Tuple[str, str]: A tuple containing user email and password.
                             Returns (None, None) if input is invalid.

        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Retrieves a User object based on the provided credentials.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The User object corresponding to the provided credentials.
                  Returns None if no user is found or credentials are invalid.

        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the authenticated User object for the current request.

        Args:
            request (Any): The HTTP request object containing authorization headers.

        Returns:
            User: The authenticated User object based on the authorization header.
                  Returns None if authentication fails or no valid user is found.

        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, password)

        return None