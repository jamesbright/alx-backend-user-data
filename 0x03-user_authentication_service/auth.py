#!/usr/bin/env python3
""" auth and password function
"""
import bcrypt


def _hash_password(password: str) -> str:
    """ Hash a password with bcrypt
    """
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
