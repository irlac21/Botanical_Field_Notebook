import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS sampling_designs (

    designID INTEGER PRIMARY KEY AUTOINCREMENT,

    projectID INTEGER,

    designType TEXT NOT NULL,

    name TEXT,

    description TEXT,

    FOREIGN KEY(projectID)
    REFERENCES projects(projectID)

)
""")


conn.commit()
conn.close()


print("Table sampling_designs créée.")