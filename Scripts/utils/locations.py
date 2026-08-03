import sqlite3
import pandas as pd

from utils.database import get_connection

def load_locations():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM locations
        ORDER BY locality
        """,
        conn
    )

    conn.close()

    return df



def get_locality_names():

    df = load_locations()

    return (
        df["locality"]
        .dropna()
        .unique()
        .tolist()
    )


def save_location(
    country,
    province,
    territory,
    locality,
    latitude=None,
    longitude=None,
    altitude=None
):

    if latitude is None or longitude is None:
        raise ValueError(
            "Latitude and longitude are required to save a location."
        )

    if not locality:
        raise ValueError(
            "Locality name is required."
        )

    conn = get_connection()

    # Pour que fetchone() renvoie un dictionnaire
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()


    # Vérifier si la localité existe déjà

    cur.execute(
    """
    SELECT locationID
    FROM locations
    WHERE locality=?
    AND ROUND(latitude,5)=ROUND(?,5)
    AND ROUND(longitude,5)=ROUND(?,5)
    AND (
        altitude IS NULL
        OR ? IS NULL
        OR ABS(altitude - ?) <= 10
    )
    """,
    (
        locality,
        latitude,
        longitude,
        altitude,
        altitude
    )
)

    row = cur.fetchone()


    if row:

        conn.close()

        return row["locationID"]



    # Sinon créer

    cur.execute(
        """
        INSERT INTO locations
        (
        country,
        province,
        territory,
        locality,
        latitude,
        longitude,
        altitude
        )

        VALUES (?,?,?,?,?,?,?)
        """,

        (
        country,
        province,
        territory,
        locality,
        latitude,
        longitude,
        altitude
        )
    )


    locationID = cur.lastrowid


    conn.commit()

    conn.close()


    return locationID