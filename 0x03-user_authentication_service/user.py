#!/usr/bin/env python3
"""creation of sqlalchemy"""
from sqlalchemy import Column, create_engine, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """sqlalchemy named User"""
    __tablename__ = 'user'  # table name

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
