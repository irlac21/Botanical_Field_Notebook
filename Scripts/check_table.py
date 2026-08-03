import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
SELECT name 
FROM sqlite_master 
WHERE type='table'
""")

tables = cursor.fetchall()

print("Tables disponibles :")

for table in tables:
    print(table[0])

conn.close()