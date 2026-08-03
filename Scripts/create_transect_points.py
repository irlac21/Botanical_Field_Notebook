import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS transect_points (

    pointID INTEGER PRIMARY KEY AUTOINCREMENT,

    transectID INTEGER NOT NULL,

    pointName TEXT,

    distance_m REAL,

    latitude REAL,
    longitude REAL,

    altitude REAL,

    description TEXT,

    FOREIGN KEY(transectID)
    REFERENCES sampling_units(unitID)

)
""")


conn.commit()
conn.close()


print("Table transect_points créée.")