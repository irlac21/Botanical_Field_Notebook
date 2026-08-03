import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


points = [

    # =====================
    # Plot P01 (unitID = 1)
    # =====================

    (1, "center", -2.300000, 28.800000, 2150, "Centre du Plot P01"),
    (1, "NW",     -2.299500, 28.799500, 2148, "Nord-Ouest Plot P01"),
    (1, "NE",     -2.299500, 28.800500, 2152, "Nord-Est Plot P01"),
    (1, "SW",     -2.300500, 28.799500, 2149, "Sud-Ouest Plot P01"),
    (1, "SE",     -2.300500, 28.800500, 2151, "Sud-Est Plot P01"),


    # =====================
    # Subplot S01 (unitID = 3)
    # =====================

    (3, "center", -2.300000, 28.800000, 2150, "Centre Subplot S01"),
    (3, "NW",     -2.299800, 28.799800, 2149, "Nord-Ouest Subplot S01"),
    (3, "NE",     -2.299800, 28.800200, 2151, "Nord-Est Subplot S01"),
    (3, "SW",     -2.300200, 28.799800, 2149, "Sud-Ouest Subplot S01"),
    (3, "SE",     -2.300200, 28.800200, 2151, "Sud-Est Subplot S01"),


    # =====================
    # Quadrat Q01 (unitID = 4)
    # =====================

    (4, "center", -2.300000, 28.800000, 2150, "Centre Quadrat Q01"),
    (4, "NW",     -2.299900, 28.799900, 2149, "Nord-Ouest Quadrat Q01"),
    (4, "NE",     -2.299900, 28.800100, 2151, "Nord-Est Quadrat Q01"),
    (4, "SW",     -2.300100, 28.799900, 2149, "Sud-Ouest Quadrat Q01"),
    (4, "SE",     -2.300100, 28.800100, 2151, "Sud-Est Quadrat Q01")

]


for p in points:

    cursor.execute("""
    INSERT INTO sampling_unit_points
    (
        unitID,
        pointType,
        latitude,
        longitude,
        altitude,
        description
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, p)


conn.commit()


cursor.execute("""
SELECT
pointID,
unitID,
pointType,
latitude,
longitude,
altitude
FROM sampling_unit_points
""")


print("Points créés :")

for row in cursor.fetchall():
    print(row)


conn.close()