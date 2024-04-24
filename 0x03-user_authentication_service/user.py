#!/usr/bin/env python3
"""creation of sqlalchemy"""
from sqlalchemy import collumn, create_engine, string, Integer
from sqlalchemy.ext.declarative import declarative_Base

Base = declarative_Base()


class User(Base):
    """sqlalchemy named User"""
    __Tablename__ = 'user'  # table name
    id = collumn(integer, primary_key=True)
    email = collumn(string, nullable=False)
    hashed_password = collumn(string, nullable=False)
    session_id = collumn(string, nullable=True)
    reset_token = column(string, nullable=True)
