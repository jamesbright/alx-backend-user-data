#!/usr/bin/env python3
"""
Implement a hash_password and verify_password function. hash_password expects one string argument
name password and returns a salted, hashed password, which is a byte string.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns salted, hashed password which is a byte string
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
