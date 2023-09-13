#!/usr/bin/env python3
""" auth and password function
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """ Hash a password with bcrypt
    """
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())


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


    def valid_login(self, email: str, password: str):
        """ Checks th validity of provided email email and password in DB
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(password.encode(), user.hashed_password)
