import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


# ==========================
# Plot P01
# ==========================

cursor.execute("""
INSERT INTO sampling_units
(
    projectID,
    unitType,
    unitName,
    description,
    designID
)
VALUES (?, ?, ?, ?, ?)
""",
(
    3,
    "Plot",
    "P01",
    "Premier plot d'inventaire forestier",
    2
))


# ==========================
# Transect T01
# ==========================

cursor.execute("""
INSERT INTO sampling_units
(
    projectID,
    unitType,
    unitName,
    description,
    designID
)
VALUES (?, ?, ?, ?, ?)
""",
(
    4,
    "Transect",
    "T01",
    "Premier transect du gradient altitudinal",
    3
))


conn.commit()


cursor.execute("""
SELECT
unitID,
projectID,
unitType,
unitName,
designID
FROM sampling_units
""")


print("Unités créées :")

for row in cursor.fetchall():
    print(row)


conn.close()