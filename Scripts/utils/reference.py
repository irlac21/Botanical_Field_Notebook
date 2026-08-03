import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def load_table(table_name):

    conn = get_connection()

    df = pd.read_sql(
        f"SELECT * FROM {table_name} ORDER BY 2",
        conn
    )

    conn.close()

    return df


def get_choices(table_name, column_name):

    df = load_table(table_name)

    if column_name not in df.columns:
        return []

    return sorted(
        df[column_name]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


def add_record(table_name, data):

    conn = get_connection()

    cur = conn.cursor()

    columns = ",".join(data.keys())

    placeholders = ",".join(["?"] * len(data))

    sql = f"""
    INSERT INTO {table_name}
    ({columns})
    VALUES ({placeholders})
    """

    cur.execute(sql, tuple(data.values()))

    conn.commit()

    conn.close()