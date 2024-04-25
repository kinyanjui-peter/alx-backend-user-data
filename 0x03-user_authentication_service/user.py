#!/usr/bin/env python3
"""creation of sqlalchemy"""
from sqlalchemy import Column, create_engine, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """sqlalchemy named User"""
    __tablename__ = 'users'  # table name

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
