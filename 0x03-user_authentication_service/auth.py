#!/usr/bin/env python3
"""authentication
"""
import bcrypt


def _hash_password(Password: str, ) -> bytes:
    """ a function that takes in password, and salt and hash it
    args:
        password(str): password to be hashed

    Returns:
        bytes: hashed password
    """
    # password_in_byte = Password.encode('utf-8')
    # hashed_password = bcrypt.hashpw(password_in_byte, bcrypt.gensalt())
    # return hashed_password
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
