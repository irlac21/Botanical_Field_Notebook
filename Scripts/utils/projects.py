import pandas as pd

from utils.database import get_connection


def load_projects():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM projects
        ORDER BY project_name
        """,
        conn
    )

    conn.close()

    return df


def get_project_names():

    df = load_projects()

    return df["project_name"].tolist()


def save_project(project_name, description="", locality=""):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT project_id
        FROM projects
        WHERE project_name=?
        """,
        (project_name,)
    )

    row = cur.fetchone()

    if row:

        conn.close()

        return row["project_id"]

    cur.execute(
        """
        INSERT INTO projects
        (project_name, description, locality)
        VALUES (?,?,?)
        """,
        (
            project_name,
            description,
            locality
        )
    )

    project_id = cur.lastrowid

    conn.commit()

    conn.close()

    return project_id