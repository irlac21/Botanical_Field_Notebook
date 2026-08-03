import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


designs = [

    (
        1,
        "opportunistic",
        "Opportunistic observations",
        "Observation libre sans unité d'échantillonnage"
    ),

    (
        3,
        "plot",
        "Plot inventory",
        "Inventaire avec plots, subplots et quadrats"
    ),

    (
        4,
        "transect",
        "Transect inventory",
        "Inventaire le long d'un transect avec points"
    )

]


for project_id, design_type, name, description in designs:

    cursor.execute("""
    INSERT INTO sampling_designs
    (
        projectID,
        designType,
        name,
        description
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        project_id,
        design_type,
        name,
        description
    ))


conn.commit()


cursor.execute("""
SELECT * FROM sampling_designs
""")


print("Designs créés :")

for row in cursor.fetchall():
    print(row)


conn.close()