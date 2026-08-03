import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(field_notes)")

print("Colonnes de field_notes :")

for col in cursor.fetchall():
    print(col)

conn.close()