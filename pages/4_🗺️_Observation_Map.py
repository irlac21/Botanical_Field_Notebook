import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# ==========================
# DATABASE
# ==========================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

conn = sqlite3.connect(DB_FILE)

query = """
SELECT
    f.species,
    f.observer,
    f.date,
    f.latitude,
    f.longitude,
    s.establishmentMeans
FROM field_notes f
LEFT JOIN species s
ON f.species = s.species
WHERE f.latitude IS NOT NULL
AND f.longitude IS NOT NULL
"""

df = pd.read_sql(query, conn)

conn.close()
# ==========================
# PAGE
# ==========================

st.title("🗺️ Observation Map")

if df.empty:
    st.warning("No observations found.")
    st.stop()

# supprimer les coordonnées nulles
df = df.dropna(subset=["latitude", "longitude"])

df = df[
    (df.latitude != 0) &
    (df.longitude != 0)
]

if df.empty:
    st.warning("No observations with GPS coordinates.")
    st.stop()

# ==========================
# FILTERS
# ==========================

st.sidebar.header("Filters")

species_list = ["All"] + sorted(df["species"].dropna().unique().tolist())

selected_species = st.sidebar.selectbox(
    "Species",
    species_list
)

if selected_species != "All":
    df = df[df["species"] == selected_species]
if df.empty:
    st.warning("No observations match the selected filter.")
    st.stop()

# ==========================
# MAP
# ==========================

# Centre de la carte
center_lat = df.latitude.mean()
center_lon = df.longitude.mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    tiles=None
)

# Zoom automatique
if len(df) == 1:
    # Une seule observation
    m.location = [df.iloc[0]["latitude"], df.iloc[0]["longitude"]]
    m.zoom_start = 18
else:
    # Plusieurs observations
    bounds = [
        [df.latitude.min(), df.longitude.min()],
        [df.latitude.max(), df.longitude.max()]
    ]
    m.fit_bounds(bounds)

folium.TileLayer(
    "OpenStreetMap",
    name="OpenStreetMap"
).add_to(m)

folium.TileLayer(
    tiles="Esri.WorldImagery",
    attr="Esri",
    name="Satellite"
).add_to(m)

marker_cluster = MarkerCluster().add_to(m)


# ==========================
# COULEUR DES MARQUEURS
# ==========================

def marker_color(status):

    if status == "native":
        return "green"

    elif status == "exotic":
        return "red"

    else:
        return "gray"


# Ajouter les observations
for _, row in df.iterrows():

    popup = folium.Popup(
        f"""
        <b>🌿 Species:</b> {row['species']}<br>
        <b>🌍 Origin:</b> {row['establishmentMeans']}<br>
        <b>👤 Observer:</b> {row['observer']}<br>
        <b>📅 Date:</b> {row['date']}
        """,
        max_width=300
    )

    folium.Marker(
    [row["latitude"], row["longitude"]],
    popup=popup,
    tooltip=row["species"],
    icon=folium.Icon(
        color=marker_color(row["establishmentMeans"]),
        icon="leaf",
        prefix="fa"
    )
).add_to(marker_cluster)

# ← AJOUTER ICI
folium.LayerControl().add_to(m)

st_folium(
    m,
    width=1200,
    height=700
)