import pandas as pd

fichier = "Flora_Bukavu_species_database.xlsx"

df = pd.read_excel(fichier)

print("Nombre d'espèces :", len(df))

print("\nColonnes :")
print(df.columns.tolist())

print("\nPremières espèces :")
print(df.head())

print("\nValeurs manquantes :")
print(df.isna().sum())