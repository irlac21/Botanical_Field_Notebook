import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
SELECT name FROM sqlite_master
WHERE type='table'
""")

print("Tables :")

for row in cursor.fetchall():
    print(row)

conn.close()