import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

from streamlit_searchbox import st_searchbox

# ==========================
# DATABASE
# ==========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


if not DB_FILE.exists():

    st.error(
        f"Database not found: {DB_FILE}"
    )

    st.stop()



conn = sqlite3.connect(
    str(DB_FILE)
)



# ==========================
# LOAD PROJECTS
# ==========================

projects = pd.read_sql(
    """
    SELECT *
    FROM projects
    WHERE deleted = 0
    """,
    conn
)



# ==========================
# PROJECT SELECTION
# ==========================

active_projects = projects[
    projects["deleted"] == 0
]


if active_projects.empty:

    st.warning(
        "No active projects available."
    )

    st.stop()



project_list = (
    active_projects["project_name"]
    .sort_values()
    .tolist()
)



selected_project = st.sidebar.selectbox(
    "📁 Project",
    project_list
)



selected_project_id = active_projects[
    active_projects["project_name"] == selected_project
]["project_id"].iloc[0]



# ==========================
# LOAD PROJECT OBSERVATIONS
# ==========================

# Toutes les observations du projet
project_query = """

SELECT

    f.species,
    f.observer,
    f.date,
    f.latitude,
    f.longitude,
    f.projectID,
    s.establishmentMeans

FROM field_notes f

LEFT JOIN species s

ON f.taxonID = s.taxonID

WHERE f.projectID = ?

AND f.deleted = 0

"""


project_df = pd.read_sql(
    project_query,
    conn,
    params=(
        int(selected_project_id),
    )
)



# Données utilisées uniquement pour la carte
df = project_df.dropna(
    subset=["latitude", "longitude"]
).copy()


df = df[
    (df["latitude"] != 0)
    &
    (df["longitude"] != 0)
]



conn.close()
# ==========================
# PAGE
# ==========================

st.title("🗺️ Observation Map")

if project_df.empty:

    st.warning(
        "No observations found for this project."
    )

    st.stop()


if df.empty:

    st.warning(
        "No observations with GPS coordinates."
    )

    st.stop()

# ==========================
# FILTERS
# ==========================

st.sidebar.header("🔎 Filter")


# Choix du type de filtre
filter_type = st.sidebar.selectbox(
    "Filter by:",
    [
        "Species",
        "Establishment means",
        "Observer"
    ]
)



# ==========================
# SPECIES FILTER
# ==========================

if filter_type == "Species":

    species_list = sorted(
        project_df["species"]
        .dropna()
        .unique()
        .tolist()
    )


    selected_species = st.sidebar.selectbox(
        "Select species",
        species_list
    )


    df = df[
        df["species"] == selected_species
    ]



# ==========================
# ESTABLISHMENT MEANS FILTER
# ==========================

elif filter_type == "Establishment means":

    establishment_list = sorted(
        project_df["establishmentMeans"]
        .dropna()
        .unique()
        .tolist()
    )


    selected_establishment = st.sidebar.selectbox(
        "Select establishment means",
        establishment_list
    )


    df = df[
        df["establishmentMeans"] == selected_establishment
    ]



# ==========================
# OBSERVER FILTER
# ==========================

elif filter_type == "Observer":

    observers = sorted(
        project_df["observer"]
        .dropna()
        .unique()
        .tolist()
    )


    selected_observer = st.sidebar.selectbox(
        "Select observer",
        observers
    )


    df = df[
        df["observer"] == selected_observer
    ]

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