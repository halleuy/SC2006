import sqlite3
import logging
import os
import bcrypt


def connect() -> sqlite3.Connection:
    return sqlite3.connect("db/users_database.db")


def init() -> None:
    if not os.path.exists("db"):
        os.makedirs("db")
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Users
        (
            USERNAME        text,
            PASSWORD        text
        )
    """
    )
    con.commit()
    logger = logging.getLogger(__name__)
    logger.info("Databased Initialized")


def user_exists(username):
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        SELECT * FROM Users
        WHERE username = ?
        """,
        (username,)
    )
    con.commit()
    if cur.fetchone() is None:
        return False
    return True


def register(username: str, password: bytes):
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO Users (username, password)
        VALUES (?, ?)
        """,
        (username, password)
    )
    con.commit()


def login(username: str, password: str):
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        SELECT * FROM Users
        WHERE username = ?
        """,
        (username,)
    )
    con.commit()
    user_details = cur.fetchone()
    if user_details is None:
        return False
    hashed_password = user_details[1]
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
