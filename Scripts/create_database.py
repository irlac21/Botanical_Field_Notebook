import pandas as pd

# Charger les données originales
fichier = "Bukavu checklist_irlac21_20260715.xlsx"

df = pd.read_excel(fichier)

# Garder uniquement les observations identifiées au niveau espèce
df = df.dropna(subset=["species"])

# Garder une ligne par espèce
species = df.drop_duplicates(subset=["species"]).copy()

# Sélectionner les informations utiles
species_database = species[
    [
        "species",
        "family",
        "genus",
        "taxonomicStatus",
        "establishmentMeans",
        "nativeRange",
        "iucnRedListCategory",
        "vernacularName",
        "primaryUse"
    ]
]

# Ajouter un identifiant unique
species_database.insert(
    0,
    "species_id",
    ["BK{:04d}".format(i+1) for i in range(len(species_database))]
)

# Sauvegarder
species_database.to_excel(
    "Flora_Bukavu_species_database.xlsx",
    index=False
)

print("Base créée avec", len(species_database), "espèces")