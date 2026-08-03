import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime


# =====================================================
# DATABASE
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)

cur = conn.cursor()


# =====================================================
# PAGE
# =====================================================

st.title("📓 Daily Botanical Notebook")

st.write(
    """
    Record a botanical observation during field work.
    """
)


# =====================================================
# AUTOMATIC DATE AND TIME
# =====================================================

now = datetime.now()

date = now.strftime("%Y-%m-%d")

time = now.strftime("%H:%M:%S")


st.info(
    f"Date: {date} | Time: {time}"
)


# =====================================================
# FORM
# =====================================================

observer = st.text_input(
    "Observer / Collector"
)


habitat = st.text_input(
    "Habitat"
)


latitude = st.number_input(
    "Latitude",
    format="%.6f"
)


longitude = st.number_input(
    "Longitude",
    format="%.6f"
)


# =====================================================
# SPECIES SEARCH
# =====================================================

species = pd.read_sql(
    """
    SELECT *
    FROM species
    ORDER BY species
    """,
    conn
)


search = st.text_input(
    "🔎 Search species"
)


filtered_species = species[
    species["species"]
    .str.contains(
        search,
        case=False,
        na=False
    )
]


selected_species = st.selectbox(
    "Select species",
    filtered_species["species"].tolist()
)


# =====================================================
# AUTOMATIC TAXON INFORMATION
# =====================================================

if selected_species:

    taxon = filtered_species[
        filtered_species["species"] == selected_species
    ].iloc[0]


    st.subheader("🌿 Taxonomic information")


    col1, col2 = st.columns(2)


    with col1:

        st.text_input(
            "Kingdom",
            taxon["kingdom"],
            disabled=True
        )

        st.text_input(
            "Phylum",
            taxon["phylum"],
            disabled=True
        )

        st.text_input(
            "Class",
            taxon["class"],
            disabled=True
        )

        st.text_input(
    "Order",
    taxon["order_name"],
    disabled=True
)


    with col2:

        st.text_input(
            "Family",
            taxon["family"],
            disabled=True
        )

        st.text_input(
            "Genus",
            taxon["genus"],
            disabled=True
        )

        st.text_input(
            "Taxon ID",
            taxon["taxonID"],
            disabled=True
        )

description = st.text_area(
    "Plant description"
)


remarks = st.text_area(
    "Remarks"
)


# =====================================================
# SAVE
# =====================================================

if st.button("💾 Save observation"):

    taxonID = species[
        species["species"] == selected_species
    ]["taxonID"].iloc[0]


    cur.execute(
        """
        INSERT INTO field_notes
        (
        date,
        time,
        observer,
        latitude,
        longitude,
        habitat,
        taxonID,
        species,
        description,
        remarks
        )

        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,

        (
        date,
        time,
        observer,
        latitude,
        longitude,
        habitat,
        taxonID,
        selected_species,
        description,
        remarks
        )
    )


    conn.commit()


    st.success(
        "✅ Observation saved successfully!"
    )


conn.close()