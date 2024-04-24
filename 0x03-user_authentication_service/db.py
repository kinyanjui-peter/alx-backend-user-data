#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResuiltFound

from user import Base


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

    def adduser(self, email: str, hashed_password: str) -> new_user:
        """add a new user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user
    
    def find_user_by(sellf, **kwargs):
        """find user"""
        try:
            user = self._session.query(user).filter_by(**kwargs).first()
            if not user:
                raise NoResuiltFound('NoResultFound')
            return user
        except InvalidRequestError as e:
            raise InvalidRequestError("InvalidRequestError") from e
        # for key, value in kwargs:
        #     find_user = {if }
