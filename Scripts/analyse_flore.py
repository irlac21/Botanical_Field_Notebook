import pandas as pd

# Nom du fichier Excel
fichier = "Bukavu checklist_irlac21_20260715.xlsx"

# Lecture du fichier
df = pd.read_excel(fichier)

# Afficher les informations générales
print("Nombre de lignes :", len(df))
print("Nombre de colonnes :", len(df))

print("\nColonnes disponibles :")
print(df.columns.tolist())

print("\nPremières lignes :")
print(df.head())
