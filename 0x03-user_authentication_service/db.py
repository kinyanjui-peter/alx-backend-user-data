#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """add a new user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """Find user by keyword arguments"""
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound('NoResultFound')
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """Method to update users"""
        try:
            # Find user using find_user_by method
            user_to_update = self.find_user_by(id=user_id)

            # Check if user_id is valid
            if user_id is None or not isinstance(user_id, int):
                raise ValueError("user_id must be an integer")

            # Check if every key in kwargs is valid
            for key in kwargs:
                if not hasattr(User, key):
                    raise ValueError(f"Invalid attribute: {key}")

            # Update user attributes
            for attr, value in kwargs.items():
                setattr(user_to_update, attr, value)

            # Update the database
            self._session.commit()

        except NoResultFound:
            raise ValueError(f"No user found with id: {user_id}") from None   
         