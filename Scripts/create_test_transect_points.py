import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


# Transect T01 = unitID 2

points = [

    (
        2,
        "T01-000",
        0,
        -2.300000,
        28.800000,
        2000,
        "Départ du transect"
    ),

    (
        2,
        "T01-100",
        100,
        -2.301000,
        28.801000,
        2050,
        "Point 100 m"
    ),

    (
        2,
        "T01-200",
        200,
        -2.302000,
        28.802000,
        2100,
        "Point 200 m"
    )

]


for point in points:

    cursor.execute("""
    INSERT INTO transect_points
    (
        transectID,
        pointName,
        distance_m,
        latitude,
        longitude,
        altitude,
        description
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, point)


conn.commit()


cursor.execute("""
SELECT
pointID,
transectID,
pointName,
distance_m,
latitude,
longitude
FROM transect_points
""")


print("Points du transect :")

for row in cursor.fetchall():
    print(row)


conn.close()