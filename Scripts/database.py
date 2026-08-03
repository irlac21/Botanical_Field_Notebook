import sqlite3
from pathlib import Path

# Dossier principal du projet
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Chemin vers la base SQLite
DB_PATH = PROJECT_DIR / "Database" / "botanical.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_database():
    conn = get_connection()
    cur = conn.cursor()

    # ===========================
    # TABLE DES ESPÈCES
    # ===========================
    cur.execute("""
CREATE TABLE IF NOT EXISTS species (

taxonID TEXT PRIMARY KEY,

scientificName TEXT,

kingdom TEXT,
phylum TEXT,
class TEXT,
order_name TEXT,

family TEXT,
genus TEXT,
species TEXT,

taxonomicStatus TEXT,

establishmentMeans TEXT,

organismRemarks TEXT,

nativeRange TEXT,

iucnRedListCategory TEXT,

vernacularName TEXT,

observationStatus TEXT,

primaryUse TEXT

)
""")

    # ===========================
    # TABLE DES PROJETS
    # ===========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        description TEXT,
        locality TEXT
    )
    """)

    # ===========================
    # TABLE DES OBSERVATIONS
    # ===========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS observations (
        observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        species_id TEXT,
        observer TEXT,
        collector TEXT,
        collection_number TEXT,
        observation_date TEXT,
        observation_time TEXT,
        latitude REAL,
        longitude REAL,
        altitude REAL,
        gps_accuracy REAL,
        locality TEXT,
        habitat TEXT,
        microhabitat TEXT,
        substrate TEXT,
        abundance TEXT,
        phenology TEXT,
        description TEXT,
        remarks TEXT,
        FOREIGN KEY(species_id) REFERENCES species(species_id)
    )
    """)

    # ===========================
    # TABLE DES PHOTOS
    # ===========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS photos (
        photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        observation_id INTEGER,
        filename TEXT,
        photo_type TEXT,
        FOREIGN KEY(observation_id) REFERENCES observations(observation_id)
    )
    """)

    conn.commit()
    conn.close()

    print("✅ botanical.db created successfully!")


if __name__ == "__main__":
    create_database()