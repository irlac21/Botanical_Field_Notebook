import pandas as pd

df = pd.read_excel("../Database/Flora_Bukavu_species_database.xlsx")


print("\n=== establishmentMeans ===")
print(df["establishmentMeans"].value_counts(dropna=False))


print("\n=== observationStatus ===")
print(df["observationStatus"].value_counts(dropna=False))


print("\n=== nativeRange (20 premières valeurs) ===")
print(df["nativeRange"].value_counts(dropna=False).head(20))