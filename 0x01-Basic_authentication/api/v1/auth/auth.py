#!/usr/bin/env python3
""" Basic Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth Class """

    def __init__(self):
        """
            Constructor

            Args:
                path: path to authenticate
                excluded_paths: list of excluded path to authenticate
        """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Requires auth

            Args:
                path: path to authenticate
                excluded_paths: list of excluded path to authenticate

            Return:
                True if is authenticated otherwise False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
            Looks at headers

            Args:
                request: Look for authorization

            Return:
                The authorization header or None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Looks for current user

            Args:
                request: current request user

            Return:
                The user
        """
        return request
