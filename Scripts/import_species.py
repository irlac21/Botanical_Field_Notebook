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
# LECTURE EXCEL
# =====================================================

df = pd.read_excel(EXCEL_FILE)


print("Nombre total d'observations :", len(df))


# =====================================================
# EXTRACTION DES ESPECES UNIQUES
# =====================================================

species_df = (
    df[
        df["species"].notna()
    ]
    .drop_duplicates(subset=["species"])
    .copy()
)
print("Nombre d'espèces uniques :", len(species_df))


# =====================================================
# CREATION TAXON ID
# =====================================================

species_df["taxonID"] = [
    f"TAX{i:06d}"
    for i in range(1, len(species_df)+1)
]


# =====================================================
# CONNEXION SQLITE
# =====================================================

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()


# =====================================================
# CREATION TABLE SPECIES
# =====================================================

cursor.execute("""
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


# =====================================================
# IMPORT DES DONNEES
# =====================================================

for _, row in species_df.iterrows():

    cursor.execute("""
    INSERT OR REPLACE INTO species
    (
    taxonID,
    scientificName,
    kingdom,
    phylum,
    class,
    order_name,
    family,
    genus,
    species,
    taxonomicStatus,
    establishmentMeans,
    organismRemarks,
    nativeRange,
    iucnRedListCategory,
    vernacularName,
    observationStatus,
    primaryUse
    )
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,

    (
    row["taxonID"],
    row["scientificName"],
    row["kingdom"],
    row["phylum"],
    row["class"],
    row["order"],
    row["family"],
    row["genus"],
    row["species"],
    row["taxonomicStatus"],
    row["establishmentMeans"],
    row["organismRemarks"],
    row["nativeRange"],
    row["iucnRedListCategory"],
    row["vernacularName"],
    row["observationStatus"],
    row["primaryUse"]
    ))

conn.commit()

conn.close()


print("✅ Import des espèces terminé !")