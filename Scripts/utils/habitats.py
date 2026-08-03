import pandas as pd

from utils.database import get_connection


def load_habitats():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM habitats
        ORDER BY habitatName
        """,
        conn
    )

    conn.close()

    return df



def get_habitat_names():

    df = load_habitats()

    return (
        df["habitatName"]
        .dropna()
        .tolist()
    )



def save_habitat(
    habitatName,
    description=""
):

    conn = get_connection()

    cur = conn.cursor()


    # Vérifier si l'habitat existe déjà

    cur.execute(
        """
        SELECT habitatID
        FROM habitats
        WHERE habitatName=?
        """,
        (habitatName,)
    )


    row = cur.fetchone()


    if row:

        conn.close()

        return row["habitatID"]



    # Créer un nouvel habitat

    cur.execute(
        """
        INSERT INTO habitats
        (
        habitatName,
        description
        )

        VALUES (?,?)
        """,

        (
        habitatName,
        description
        )
    )


    habitatID = cur.lastrowid


    conn.commit()

    conn.close()


    return habitatID