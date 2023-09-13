#!/usr/bin/env python3
""" auth and password function
"""
import bcrypt
from uuid import uuid4
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """ Hash a password with bcrypt
    """
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generates and returns a string representation of a uuid
    """
    return str(uuid4())


class Auth:
    """ Class interacts with the authentication DB
    """

    def __init__(self) -> None:
        """ Initialize Auth class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Verifies data and registers a new user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            pwd_encrypt = _hash_password(password=password)
            return self._db.add_user(email=email, hashed_password=pwd_encrypt)
        else:
            raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks th validity of provided email email and password in DB
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(bytes(password, "ascii"),
                                  user.hashed_password)

    def create_session(self, email: str) -> str:
        """ Takes an email str argument to find a user, then
        generate a session_id
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ takes a session_id string and returns the corresponding user
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: str) -> None:
        """ Destroys a user session with user ID
        """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            return self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ generates and returns password reset token for
            A valid user
        """
        if email is None:
            return None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the user password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            user.hashed_password = _hash_password(password=password)
            user.reset_token = None
