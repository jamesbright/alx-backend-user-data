#!/usr/bin/env python3
"""Basic Auth class inherits from Auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth class """
    def __init__(self):
        """Constructor"""
