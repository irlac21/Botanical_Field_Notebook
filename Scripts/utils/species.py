import pandas as pd

from utils.database import get_connection



def load_species():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM species
        ORDER BY species
        """,
        conn
    )

    conn.close()

    return df



def search_species(text):

    df = load_species()

    if not isinstance(text, str) or text == "":
        return df

    return df[
        df["species"].str.contains(
            text,
            case=False,
            na=False
        )
    ]



def get_species(species_name):

    df = load_species()

    result = df[
        df["species"] == species_name
    ]

    if result.empty:

        return None

    return result.iloc[0]



def create_species(data):

    """
    Create a new species if it does not exist.
    """

    conn = get_connection()

    cur = conn.cursor()


    # Vérifier existence

    cur.execute(
        """
        SELECT taxonID
        FROM species
        WHERE species=?
        """,
        (
        data["species"],
        )
    )


    existing = cur.fetchone()


    if existing:

        conn.close()

        return existing["taxonID"]



    columns = ",".join(data.keys())

    placeholders = ",".join(
        ["?"] * len(data)
    )


    sql = f"""
    INSERT INTO species
    ({columns})
    VALUES ({placeholders})
    """


    cur.execute(
        sql,
        tuple(data.values())
    )


    conn.commit()


    taxonID = cur.lastrowid


    conn.close()


    return taxonID