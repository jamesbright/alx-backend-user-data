#!/usr/bin/env python3
""" Session Auth class inherits from Auth class
    and authenticates with sessions.
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session Auth class
    """
    def __init__(self):
        """ Constructor"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates session for a user

            Args:
                user_id: ID of the user

            return:
                 the Session ID
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a user ID based on a Session ID

            Args:
                session_id: the session ID
            Return:
                user ID that has session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
