import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute("""
ALTER TABLE field_notes
ADD COLUMN samplingUnitID INTEGER
""")


conn.commit()
conn.close()


print("Colonne samplingUnitID ajoutée à field_notes.")