import pandas as pd

from utils.database import get_connection


def load_collectors():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM collectors
        ORDER BY fullName
        """,
        conn
    )

    conn.close()

    return df


def get_collector_names():

    df = load_collectors()

    return df["fullName"].tolist()


def add_collector(fullName, institution="", email=""):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO collectors
        (fullName, institution, email)
        VALUES (?,?,?)
        """,
        (
            fullName,
            institution,
            email
        )
    )

    conn.commit()

    conn.close()