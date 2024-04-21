#!/usr/bin/env python3
"""
this is the vasic app for the API
"""
from flask import request
from typing import List, TypeVar


class Auth():
    # def __init__(self):
    #     pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns False - path and excluded_paths
        """
        if path is None:
            return True
        if not excluded_paths or excluded_paths is None:
            return True

        if path.endswith('/'):
            path = path[:-1]

        for excluded_paths in excluded_paths:
            if excluded_paths.endswith('/'):
                excluded_paths = excluded_paths[:-1]
            if path == excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        auth header
        """
        if request is None:
            return None

        authorization_header = request.header.get('authorization')
        if authorization_header is None:
            return None
        return authorization_header
            
            
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None
