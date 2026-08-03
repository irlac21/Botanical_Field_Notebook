import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS sampling_unit_points (

    pointID INTEGER PRIMARY KEY AUTOINCREMENT,

    unitID INTEGER NOT NULL,

    pointType TEXT NOT NULL,

    latitude REAL,

    longitude REAL,

    altitude REAL,

    description TEXT

)
""")


conn.commit()

conn.close()


print("Table sampling_unit_points créée.")