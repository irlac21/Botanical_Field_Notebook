import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# ==========================
# Habitats
# ==========================

cur.execute("""
CREATE TABLE IF NOT EXISTS habitats(

habitatID INTEGER PRIMARY KEY AUTOINCREMENT,

habitatName TEXT UNIQUE,

description TEXT

)
""")

# ==========================
# Phenology
# ==========================

cur.execute("""
CREATE TABLE IF NOT EXISTS phenology_types(

phenologyID INTEGER PRIMARY KEY AUTOINCREMENT,

phenologyName TEXT UNIQUE

)
""")

# ==========================
# Observation Status
# ==========================

cur.execute("""
CREATE TABLE IF NOT EXISTS observation_status(

statusID INTEGER PRIMARY KEY AUTOINCREMENT,

statusName TEXT UNIQUE

)
""")

# ==========================
# Establishment Means
# ==========================

cur.execute("""
CREATE TABLE IF NOT EXISTS establishment_means(

establishmentID INTEGER PRIMARY KEY AUTOINCREMENT,

establishmentName TEXT UNIQUE

)
""")

# ==========================
# Native Range
# ==========================

cur.execute("""
CREATE TABLE IF NOT EXISTS native_ranges(

rangeID INTEGER PRIMARY KEY AUTOINCREMENT,

rangeName TEXT UNIQUE

)
""")

conn.commit()
conn.close()

print("✅ Reference tables created successfully!")