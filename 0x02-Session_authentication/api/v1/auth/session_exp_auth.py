#!/usr/bin/env python3

"""
Adds expiration date to session ID
"""
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Session expiration class
    """

    def __init__(self):
        """ Initialize class
        """
        try:
            session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0

        self.session_duration = session_duration

    def create_session(self, user_id: str = None) -> str:
        """ Creates a new session

            Args:
                user_id: ID of user
            Return:
                a session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {'user_id': user_id, 'created_at': datetime.now()}

        SessionAuth.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns user id for given session Id

            Args:
                session_id: the Session ID

            Return:
                the user ID of the given session_id
        """
        if session_id is None:
            return None
        if session_id not in SessionAuth.user_id_by_session_id.keys():
            return None
        session_dict = SessionAuth.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict["user_id"]

        if "created_at" not in session_dict.keys():
            return None

        creation_time = session_dict["created_at"]

        time_delta = timedelta(seconds=self.session_duration)
        if (creation_time + time_delta) < datetime.now():
            return None
        return session_dict["user_id"]
