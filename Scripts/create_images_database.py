import pandas as pd

# Lire la base des espèces
df = pd.read_excel("../Database/Flora_Bukavu_species_database.xlsx")

# Créer une table vide pour les images
images = pd.DataFrame({
    "image_id": [],
    "species_id": [],
    "species": [],
    "image_type": [],
    "filename": [],
    "photographer": [],
    "date": [],
    "location": []
})

# Sauvegarder
images.to_excel(
    "../Database/species_images.xlsx",
    index=False
)

print("Base images créée")