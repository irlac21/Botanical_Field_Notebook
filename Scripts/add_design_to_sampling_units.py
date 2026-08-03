import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute("""
ALTER TABLE sampling_units
ADD COLUMN designID INTEGER
""")


conn.commit()
conn.close()


print("Colonne designID ajoutée à sampling_units.")