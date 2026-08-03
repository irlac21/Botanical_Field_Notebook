import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS sampling_units (

    unitID INTEGER PRIMARY KEY AUTOINCREMENT,

    projectID INTEGER,

    unitType TEXT NOT NULL,
    unitName TEXT NOT NULL,

    parentUnitID INTEGER,

    latitude REAL,
    longitude REAL,

    area REAL,

    length REAL,
    width REAL,

    description TEXT,

    FOREIGN KEY(projectID)
    REFERENCES projects(projectID),

    FOREIGN KEY(parentUnitID)
    REFERENCES sampling_units(unitID)

)
""")


conn.commit()
conn.close()


print("Table sampling_units créée avec succès.")