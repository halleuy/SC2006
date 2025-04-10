import sqlite3
import logging
import os


def connect() -> sqlite3.Connection:
    return sqlite3.connect("db/racks_database.db")


def init() -> None:
    if not os.path.exists("db"):
        os.makedirs("db")
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Racks
        (
            DESCRIPTION         text,
            LATITUDE            float,
            LONGITUDE           float,
            RACK_TYPE           text,
            RACK_COUNT          int,
            SHELTER_INDICATOR   text
        )
    """
    )
    con.commit()
    logger = logging.getLogger(__name__)
    logger.info("Databased Initialized")


def add_rack(
        description: str,
        latitude: float,
        longitude: float,
        rack_type: str,
        rack_count: int,
        shelter_indicator: str
):
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO Racks (
            description,
            latitude,
            longitude,
            rack_type,
            rack_count,
            shelter_indicator
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            description,
            latitude,
            longitude,
            rack_type,
            rack_count,
            shelter_indicator
        )
    )
    con.commit()


def rack_exists(rack_id: str):
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        SELECT * FROM Racks
        WHERE description = ?
        """,
        (rack_id,)
    )
    rack = cur.fetchone()
    if rack is None:
        return False
    return True


def get_rack_limit(rack_id: str):
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        SELECT * FROM Racks
        WHERE description = ?
        """,
        (rack_id,)
    )
    rack = cur.fetchone()
    if rack is None:
        return -1
    return rack[4]


def get_all_racks():
    con = connect()
    cur = con.cursor()
    cur.execute(
        """
        SELECT * FROM Racks
        """,
    )
    racks = []
    for rack in cur.fetchall():
        racks.append(
            {
                "Description": rack[0],
                "Latitude": rack[1],
                "Longitude": rack[2],
                "RackType": rack[3],
                "RackCount": rack[4],
                "ShelterIndicator": rack[5]
            }
        )
    return racks
