import pandas as pd

fichier = "Bukavu checklist_irlac21_20260715.xlsx"

df = pd.read_excel(fichier)

ligne = df[df["species"].isna()]

print(ligne.T)