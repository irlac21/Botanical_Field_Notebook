import pandas as pd

# Charger les données
fichier = "Bukavu checklist_irlac21_20260715.xlsx"
df = pd.read_excel(fichier)

# Nombre d'espèces
nb_especes = df["species"].nunique()

# Nombre de familles
nb_familles = df["family"].nunique()

# Nombre d'observations
nb_observations = len(df)

print("Nombre d'observations :", nb_observations)
print("Nombre d'espèces :", nb_especes)
print("Nombre de familles :", nb_familles)

print("\nEspèces par famille (10 premières) :")
print(df.groupby("family")["species"].nunique().sort_values(ascending=False).head(10))