#!/usr/bin/env python3
""" Session Auth class inherits from Auth class
    and authenticates with sessions.
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session Auth class
    """
    def __init__(self):
        """ Constructor"""
