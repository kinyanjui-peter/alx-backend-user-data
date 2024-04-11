#!/usr/bin/env python3
"""
Script for managing Sensitive Information
"""
from typing import List
import re
import logging
from os import environ
import mysql.connector

# Sensitive fields to be sanitized
SENSITIVE_FIELDS = ("name", "email", "phone", "ssn", "password")

def sanitize_data(fields: List[str], sanitization: str,
                  message: str, separator: str) -> str:
    """
    Replaces sensitive data in a message with sanitized values
    based on the list of fields to sanitize

    Args:
        fields: list of fields to sanitize
        sanitization: the value to use for sanitization
        message: the string message to filter
        separator: the separator to use between fields

    Returns:
        The filtered string message with sanitized values
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={sanitization}{separator}', message)
    return message

def get_logger() -> logging.Logger:
    """
    Returns a Logger object for managing Sensitive Information

    Returns:
        A Logger object with INFO log level and SanitizingFormatter
        formatter for sanitizing sensitive fields
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(SanitizingFormatter(list(SENSITIVE_FIELDS)))
    logger.addHandler(stream_handler)

    return logger

def get_database_connection() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a MySQLConnection object for accessing Sensitive Information database

    Returns:
        A MySQLConnection object using connection details from
        environment variables
    """
    username = environ.get("SENSITIVE_DATA_DB_USERNAME", "root")
    password = environ.get("SENSITIVE_DATA_DB_PASSWORD", "")
    host = environ.get("SENSITIVE_DATA_DB_HOST", "localhost")
    database_name = environ.get("SENSITIVE_DATA_DB_NAME")

    connection = mysql.connector.connection.MySQLConnection(user=username,
                                                     password=password,
                                                     host=host,
                                                     database=database_name)
    return connection

def main():
    """
    Main function to retrieve user data from database and log to console
    """
    db_connection = get_database_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [column[0] for column in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{field}={str(value)}; ' for value, field in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db_connection.close()

class SanitizingFormatter(logging.Formatter):
    """
    Sanitizing Formatter class for filtering sensitive fields
    """

    SANITIZATION = "***"
    FORMAT = "[SENSITIVE_DATA] %(name)s %(levelname)s %(asctime)-15s:%(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor method for SanitizingFormatter class

        Args:
            fields: list of fields to sanitize in log messages
        """
        super(SanitizingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the specified log record as text.
        Sanitizes values in incoming log records using sanitize_data.
        """
        record.msg = sanitize_data(self.fields, self.SANITIZATION,
                    record.getMessage(), self.SEPARATOR)
        return super(SanitizingFormatter, self).format(record)


if __name__ == '__main__':
    main()
