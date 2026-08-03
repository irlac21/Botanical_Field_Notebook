import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


try:
    cursor.execute("""
    ALTER TABLE sampling_units
    ADD COLUMN altitude REAL
    """)

    print("Colonne altitude ajoutée à sampling_units.")

except sqlite3.OperationalError:
    print("La colonne altitude existe déjà.")


conn.commit()
conn.close()