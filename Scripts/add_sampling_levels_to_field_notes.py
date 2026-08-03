import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


columns = [
    "plotID INTEGER",
    "subplotID INTEGER",
    "quadratID INTEGER",
    "transectID INTEGER"
]


for column in columns:
    try:
        cursor.execute(
            f"ALTER TABLE field_notes ADD COLUMN {column}"
        )
        print(f"Ajouté : {column}")

    except sqlite3.OperationalError:
        print(f"Existe déjà : {column}")


conn.commit()
conn.close()


print("Structure field_notes mise à jour.")