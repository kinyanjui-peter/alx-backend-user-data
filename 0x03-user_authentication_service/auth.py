#!/usr/bin/env python3
"""authentication
"""
import bcrypt
from db import DB



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


class class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
        
    def register_user(self, email: str, required=True, password: str, required=True) -> User:
        """check user by email """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user is not None:
                raise ValueError(f'User {email} already exist')
            else:
                new_user = self._db.add_user(email=email, hashed_password=hashed_password)
                return new_user
        except Exception as e:
            # handle exception
            print(f'user cannot be registered')
            return None
            
                                              
        