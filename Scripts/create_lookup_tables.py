import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# ============================
# Collectors
# ============================

cur.execute("""
CREATE TABLE IF NOT EXISTS collectors(

collectorID INTEGER PRIMARY KEY AUTOINCREMENT,

fullName TEXT UNIQUE,

institution TEXT,

email TEXT

)
""")

# ============================
# Projects
# ============================

cur.execute("""
CREATE TABLE IF NOT EXISTS projects(

projectID INTEGER PRIMARY KEY AUTOINCREMENT,

projectName TEXT UNIQUE,

description TEXT

)
""")

# ============================
# Locations
# ============================

cur.execute("""
CREATE TABLE IF NOT EXISTS locations(

locationID INTEGER PRIMARY KEY AUTOINCREMENT,

country TEXT,

province TEXT,

territory TEXT,

locality TEXT,

latitude REAL,

longitude REAL,

altitude REAL

)
""")

# ============================
# Vernacular names
# ============================

cur.execute("""
CREATE TABLE IF NOT EXISTS vernacular_names(

vernacularID INTEGER PRIMARY KEY AUTOINCREMENT,

taxonID TEXT,

language TEXT,

region TEXT,

vernacularName TEXT,

source TEXT,

FOREIGN KEY(taxonID)
REFERENCES species(taxonID)

)
""")

# ============================
# Species uses
# ============================

cur.execute("""
CREATE TABLE IF NOT EXISTS species_uses(

useID INTEGER PRIMARY KEY AUTOINCREMENT,

taxonID TEXT,

useType TEXT,

source TEXT,

FOREIGN KEY(taxonID)
REFERENCES species(taxonID)

)
""")

conn.commit()
conn.close()

print("✅ Lookup tables created successfully!")