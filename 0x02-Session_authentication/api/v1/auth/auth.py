#!/usr/bin/env python3
""" Basic Auth class
"""
from os import getenv
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
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[-1] is not '/':
            path += '/'

        for paths in excluded_paths:
            if paths.endswith('*'):
                if path.startswith(paths[:-1]):
                    return False
            elif path == paths:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
            Looks at headers

            Args:
                request: Look for authorization

            Return:
                The authorization header or None
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Looks for current user

            Args:
                request: current request user

            Return:
                The user
        """
        return request

    def session_cookie(self, request=None):
        """
            return a cookie value from a request

            Args:
                request: current request containing cookie

            Return:
                cookie value
        """
        if request is None:
            return None
        _my_session_id = getenv("SESSION_NAME")
        cookie_value = request.cookies.get(_my_session_id)
        return cookie_value
