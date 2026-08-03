import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute("""
SELECT
    su.unitName,
    su.unitType,
    sup.pointType,
    sup.latitude,
    sup.longitude,
    sup.altitude

FROM sampling_units su

JOIN sampling_unit_points sup
ON su.unitID = sup.unitID

ORDER BY su.unitID, sup.pointID
""")


print("Géométrie des unités :\n")


for row in cursor.fetchall():
    print(row)


conn.close()