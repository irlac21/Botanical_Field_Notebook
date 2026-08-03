import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(species)")

columns = cursor.fetchall()

print("Colonnes de species :")

for col in columns:
    print(col)

conn.close()