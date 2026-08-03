import pandas as pd
import sqlite3
from pathlib import Path


# =====================================================
# CHEMINS
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

EXCEL_FILE = PROJECT_DIR / "Bukavu checklist_irlac21_20260715.xlsx"

DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


# =====================================================
# LECTURE DES DONNEES
# =====================================================

df = pd.read_excel(EXCEL_FILE)

print("Nombre total d'observations :", len(df))


# =====================================================
# CONNEXION BASE
# =====================================================

conn = sqlite3.connect(DB_FILE)

cur = conn.cursor()


# =====================================================
# CREATION TABLE OCCURRENCES
# =====================================================

cur.execute("""
CREATE TABLE IF NOT EXISTS occurrences (

occurrenceID TEXT PRIMARY KEY,

taxonID TEXT,

eventDate TEXT,

basisOfRecord TEXT,

scientificName TEXT,

family TEXT,

genus TEXT,

species TEXT,

establishmentMeans TEXT,

organismRemarks TEXT,

nativeRange TEXT,

iucnRedListCategory TEXT,

vernacularName TEXT,

observationStatus TEXT,

primaryUse TEXT,

country TEXT,

stateProvince TEXT,

locality TEXT,

institutionCode TEXT,

ownerInstitutionCode TEXT

)
""")


# =====================================================
# RECUPERATION DES TAXON ID
# =====================================================

taxon_map = pd.read_sql(
    "SELECT taxonID, species FROM species",
    conn
)


df = df.merge(
    taxon_map,
    on="species",
    how="left"
)


# =====================================================
# IMPORT DES OBSERVATIONS
# =====================================================

for _, row in df.iterrows():

    cur.execute("""
    INSERT OR REPLACE INTO occurrences
    (
    occurrenceID,
    taxonID,
    eventDate,
    basisOfRecord,
    scientificName,
    family,
    genus,
    species,
    establishmentMeans,
    organismRemarks,
    nativeRange,
    iucnRedListCategory,
    vernacularName,
    observationStatus,
    primaryUse,
    country,
    stateProvince,
    locality,
    institutionCode,
    ownerInstitutionCode
    )

    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,

    (

    row["occurrenceID"],
    row["taxonID"],
    row["eventDate"],
    row["basisOfRecord"],
    row["scientificName"],
    row["family"],
    row["genus"],
    row["species"],
    row["establishmentMeans"],
    row["organismRemarks"],
    row["nativeRange"],
    row["iucnRedListCategory"],
    row["vernacularName"],
    row["observationStatus"],
    row["primaryUse"],
    row["country"],
    row["stateProvince"],
    row["locality"],
    row["institutionCode"],
    row["ownerInstitutionCode"]

    ))


conn.commit()

conn.close()


print("✅ Import des occurrences terminé !")