import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()


# ==========================================================
# Fonction qui ajoute une colonne uniquement si elle n'existe pas
# ==========================================================

def add_column(table, column, definition):

    cols = [c[1] for c in cur.execute(f"PRAGMA table_info({table})")]

    if column not in cols:

        cur.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
        )

        print(f"✅ {column} ajouté")

    else:

        print(f"✔ {column} existe déjà")


# ==========================================================
# Champs de gestion
# ==========================================================

add_column("field_notes", "collectorID", "INTEGER")
add_column("field_notes", "projectID", "INTEGER")
add_column("field_notes", "locationID", "INTEGER")


# ==========================================================
# Informations de collecte botanique
# ==========================================================

add_column("field_notes", "collectorNumber", "TEXT")
add_column("field_notes", "specimenCount", "INTEGER")
add_column("field_notes", "individualCount", "INTEGER")
add_column("field_notes", "phenology", "TEXT")


# ==========================================================
# Localité
# ==========================================================

add_column("field_notes", "altitude", "REAL")
add_column("field_notes", "localityDescription", "TEXT")


# ==========================================================
# Métadonnées
# ==========================================================

add_column("field_notes", "createdAt", "TEXT")
add_column("field_notes", "updatedAt", "TEXT")


conn.commit()
conn.close()

print("\n✅ field_notes updated successfully!")