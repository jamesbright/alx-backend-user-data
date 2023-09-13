#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Saves user to DB and returns the object

            Args:
                email: user email
                hashed_password: user password hash

            Return:
                Saved user object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Finds a user using supplied arguments
            Args:
                **kwargs: search terms
            Return:
                User if found or raise exception
        """
        if kwargs is None:
            raise InvalidRequestError
        
        for i in kwargs.keys():
            if i not in User.__table__.columns.keys():
                raise InvalidRequestError
            
        user_data = self._session.query(User).filter_by(**kwargs).first()

        if user_data is None:
            raise NoResultFound
        
        return user_data


