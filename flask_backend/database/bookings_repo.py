from datetime import datetime
import sqlite3
import logging
import os


def connect() -> sqlite3.Connection:
    return sqlite3.connect("db/bookings_database.db")


def init() -> None:
    if not os.path.exists("db"):
        os.makedirs("db")

    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Bookings
        (
            USERNAME            text,
            RACK_ID        text,
            CONFIRMED           bool,
            BOOKING_TIME_UNIX   integer
        )
    """
    )
    con.commit()
    logger = logging.getLogger(__name__)
    logger.info("Databased Initialized")


def clear_booking(username: str, rack_id: str):
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        DELETE FROM Bookings
        WHERE username = ?
        AND rack_id = ?
        """,
        (username, rack_id)
    )
    con.commit()


def add_booking(username: str, rack_id: str, booking_time: datetime):
    unix_time = int(booking_time.timestamp())
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        SELECT COUNT(*) FROM Bookings
        WHERE rack_id = ?
        AND username = ?
        """,
        (rack_id, username)
    )
    con.commit()
    if cur.fetchone()[0] > 0:
        # Shows booking already exists so return False
        return False
    cur.execute(
        """
        INSERT INTO Bookings (username, rack_id, confirmed, booking_time_unix)
        VALUES (?, ?, ?, ?)
        """,
        (username, rack_id, False, unix_time)
    )
    con.commit()
    return True


def get_rack_booking_count(rack_id: str):
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        SELECT COUNT(*) FROM Bookings
        WHERE rack_id = ?
        """,
        (rack_id,)
    )
    return cur.fetchone()[0]


def confirm_booking(username: str, rack_id: str):
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        UPDATE Bookings
        SET confirmed = 1
        WHERE username = ?
        AND rack_id = ?
        """,
        (username, rack_id)
    )
    con.commit()


def get_bookings(username: str):
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
            SELECT * FROM Bookings
            WHERE username = ?
            """,
        (username,)
    )
    con.commit()
    data = []
    for row in cur.fetchall():
        date = datetime.fromtimestamp(row[3])
        booking = {
            "Description": row[1],
            "DateTime": str(date),
            "Confirmed": row[2]
        }
        data.append(booking)
    return data


def prune_bookings():
    time_now = int(datetime.now().timestamp())
    cutoff_time = time_now - (30*60)
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        DELETE FROM Bookings
        WHERE booking_time_unix < ?
        AND confirmed = 0
        """,
        (cutoff_time,)
    )
    con.commit()
