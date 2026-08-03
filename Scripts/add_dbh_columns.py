import sqlite3
from pathlib import Path

# Localiser la base de données
PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Ajouter DBH
try:
    cur.execute("""
        ALTER TABLE field_notes
        ADD COLUMN dbh REAL
    """)
    print("✓ Colonne 'dbh' ajoutée.")
except sqlite3.OperationalError:
    print("La colonne 'dbh' existe déjà.")

# Ajouter Height
try:
    cur.execute("""
        ALTER TABLE field_notes
        ADD COLUMN height REAL
    """)
    print("✓ Colonne 'height' ajoutée.")
except sqlite3.OperationalError:
    print("La colonne 'height' existe déjà.")

conn.commit()
conn.close()

print("Terminé.")