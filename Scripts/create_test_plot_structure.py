import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


# Plot P01 existe déjà avec unitID = 1


# Subplot S01
cursor.execute("""
INSERT INTO sampling_units
(projectID, unitType, unitName, parentUnitID, designID)
VALUES (?, ?, ?, ?, ?)
""",
(3, "Subplot", "S01", 1, 2))


subplot1 = cursor.lastrowid


# Quadrat Q01
cursor.execute("""
INSERT INTO sampling_units
(projectID, unitType, unitName, parentUnitID, designID)
VALUES (?, ?, ?, ?, ?)
""",
(3, "Quadrat", "Q01", subplot1, 2))


# Quadrat Q02
cursor.execute("""
INSERT INTO sampling_units
(projectID, unitType, unitName, parentUnitID, designID)
VALUES (?, ?, ?, ?, ?)
""",
(3, "Quadrat", "Q02", subplot1, 2))


# Subplot S02
cursor.execute("""
INSERT INTO sampling_units
(projectID, unitType, unitName, parentUnitID, designID)
VALUES (?, ?, ?, ?, ?)
""",
(3, "Subplot", "S02", 1, 2))


conn.commit()


cursor.execute("""
SELECT unitID, unitType, unitName, parentUnitID
FROM sampling_units
WHERE designID = 2
""")


print("Structure Plot :")

for row in cursor.fetchall():
    print(row)


conn.close()