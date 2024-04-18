#!/usr/bin/env python3
"""

"""
from flask import request
from typing import List, TypeVar


class Auth():
    def __init__(self):
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns False - path and excluded_paths
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        auth header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None
