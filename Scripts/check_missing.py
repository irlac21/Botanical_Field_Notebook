import pandas as pd

df = pd.read_excel("Flora_Bukavu_species_database.xlsx")

missing = df[df["species"].isna()]

print(missing)