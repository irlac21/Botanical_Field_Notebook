import sqlite3
from pathlib import Path


# =====================================================
# CHEMIN DATABASE
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


# =====================================================
# CONNEXION
# =====================================================

conn = sqlite3.connect(DB_FILE)

cur = conn.cursor()


# =====================================================
# CREATION TABLE FIELD NOTES
# =====================================================

cur.execute("""
CREATE TABLE IF NOT EXISTS field_notes (

noteID INTEGER PRIMARY KEY AUTOINCREMENT,

date TEXT,

time TEXT,

observer TEXT,

latitude REAL,

longitude REAL,

habitat TEXT,

photo TEXT,

taxonID TEXT,

species TEXT,

description TEXT,

remarks TEXT,

FOREIGN KEY (taxonID) REFERENCES species(taxonID)

)
""")


conn.commit()

conn.close()


print("✅ Table field_notes créée avec succès !")