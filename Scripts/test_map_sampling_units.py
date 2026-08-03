import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

import folium
from streamlit_folium import st_folium
from folium import Polygon, Marker


# ==========================
# DATABASE
# ==========================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

conn = sqlite3.connect(DB_FILE)


query_units = """
SELECT
    unitID,
    unitType,
    unitName
FROM sampling_units
WHERE unitType IN ('Plot', 'Subplot', 'Quadrat')
"""

units = pd.read_sql(query_units, conn)


query_points = """
SELECT
    unitID,
    pointType,
    latitude,
    longitude,
    altitude
FROM sampling_unit_points
"""

points = pd.read_sql(query_points, conn)


conn.close()


# ==========================
# PAGE
# ==========================

st.title("🌳 Sampling Units Map")


if units.empty:
    st.warning("No sampling units found.")
    st.stop()


# ==========================
# MAP
# ==========================

center_lat = points.latitude.mean()
center_lon = points.longitude.mean()


m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=16
)


# couleurs selon type

colors = {
    "Plot": "green",
    "Subplot": "blue",
    "Quadrat": "orange"
}


# ==========================
# DRAW POLYGONS
# ==========================

for _, unit in units.iterrows():

    unit_points = points[
        points["unitID"] == unit["unitID"]
    ]

    corners = unit_points[
        unit_points["pointType"].isin(
            ["NW", "NE", "SE", "SW"]
        )
    ]


    if len(corners) == 4:

        # ordre du polygone
        order = ["NW", "NE", "SE", "SW"]

        polygon_points = []

        for p in order:

            row = corners[
                corners["pointType"] == p
            ]

            polygon_points.append(
                [
                    row.latitude.values[0],
                    row.longitude.values[0]
                ]
            )


        Polygon(
            locations=polygon_points,
            color=colors.get(
                unit["unitType"],
                "gray"
            ),
            fill=True,
            fill_opacity=0.3,
            popup=f"""
            <b>{unit['unitType']}</b><br>
            {unit['unitName']}
            """
        ).add_to(m)


    # centre

    center = unit_points[
        unit_points["pointType"] == "center"
    ]


    if len(center) > 0:

        Marker(
            [
                center.latitude.values[0],
                center.longitude.values[0]
            ],
            popup=f"""
            {unit['unitType']} :
            {unit['unitName']}
            """
        ).add_to(m)



st_folium(
    m,
    width=1200,
    height=700
)