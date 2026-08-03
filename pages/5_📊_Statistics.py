import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt


# =====================================================
# DATABASE
# =====================================================

# Racine du projet Botanical_Field_Notebook
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Chemin vers la base SQLite
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"

# Vérification existence base
if not DB_FILE.exists():
    st.error(f"Database not found: {DB_FILE}")
    st.stop()

# Connexion SQLite
conn = sqlite3.connect(str(DB_FILE))


# =====================================================
# LOAD DATA
# =====================================================

species = pd.read_sql(
    "SELECT * FROM species",
    conn
)

field_notes = pd.read_sql(
    "SELECT * FROM field_notes",
    conn
)

collectors = pd.read_sql(
    "SELECT * FROM collectors",
    conn
)

projects = pd.read_sql(
    "SELECT * FROM projects",
    conn
)

locations = pd.read_sql(
    "SELECT * FROM locations",
    conn
)

sampling_units = pd.read_sql(
    "SELECT * FROM sampling_units",
    conn
)

occurrences = pd.read_sql(
    "SELECT * FROM occurrences",
    conn
)

conn.close()


# =====================================================
# PAGE TITLE
# =====================================================

st.title("📊 Botanical Statistics")

st.markdown(
"""
Explore biodiversity patterns from the botanical database.
"""
)


# =====================================================
# GENERAL INDICATORS
# =====================================================

st.subheader("Overview")

# Première ligne
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🌿 Species",
    species["species"].nunique()
)

col2.metric(
    "🌳 Genera",
    species["genus"].nunique()
)

col3.metric(
    "🌼 Families",
    species["family"].nunique()
)

col4.metric(
    "📑 Observations",
    len(field_notes)
)

# Deuxième ligne
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👤 Collectors",
    len(collectors)
)

col2.metric(
    "📁 Projects",
    len(projects)
)

col3.metric(
    "📍 Localities",
    len(locations)
)

col4.metric(
    "📦 Sampling Units",
    len(sampling_units)
)

st.divider()

# =====================================================
# OBSERVATION TYPES
# =====================================================

st.subheader("Observation Types")

# Séparation des observations
opportunistic = field_notes[
    field_notes["samplingUnitID"].isna() &
    field_notes["transectID"].isna()
]

plot = field_notes[
    field_notes["samplingUnitID"].notna()
]

transect = field_notes[
    field_notes["transectID"].notna()
]

col1, col2, col3 = st.columns(3)

# =====================================================
# OPPORTUNISTIC
# =====================================================

with col1:

    st.markdown("### 🟢 Opportunistic")

    st.metric(
        "Observations",
        len(opportunistic)
    )

    st.metric(
        "Species",
        opportunistic["taxonID"].nunique()
    )

    st.metric(
        "Individuals",
        opportunistic["individualCount"].fillna(0).sum()
    )

# =====================================================
# PLOTS
# =====================================================

with col2:

    st.markdown("### 🔵 Plot")

    st.metric(
        "Observations",
        len(plot)
    )

    st.metric(
        "Species",
        plot["taxonID"].nunique()
    )

    st.metric(
        "Individuals",
        plot["individualCount"].fillna(0).sum()
    )

    st.metric(
        "Mean DBH",
        round(plot["dbh"].mean(), 2)
        if plot["dbh"].notna().any()
        else 0
    )

# =====================================================
# TRANSECTS
# =====================================================

with col3:

    st.markdown("### 🟠 Transect")

    st.metric(
        "Observations",
        len(transect)
    )

    st.metric(
        "Species",
        transect["taxonID"].nunique()
    )

    st.metric(
        "Individuals",
        transect["individualCount"].fillna(0).sum()
    )

    st.metric(
        "Mean DBH",
        round(transect["dbh"].mean(), 2)
        if transect["dbh"].notna().any()
        else 0
    )

st.divider()

# =====================================================
# OBSERVATIONS BY TYPE
# =====================================================

st.subheader("Observations by Type")

obs_type = pd.DataFrame({
    "Type": ["Opportunistic", "Plot", "Transect"],
    "Observations": [
        len(opportunistic),
        len(plot),
        len(transect)
    ]
})

fig, ax = plt.subplots(figsize=(6,4))

ax.bar(
    obs_type["Type"],
    obs_type["Observations"]
)

ax.set_xlabel("")
ax.set_ylabel("Number of observations")
ax.set_title("Observation types")

for i, v in enumerate(obs_type["Observations"]):
    ax.text(
        i,
        v,
        str(v),
        ha="center",
        va="bottom"
    )

st.pyplot(fig)

st.divider()

# =====================================================
# ORIGIN / ESTABLISHMENT STATUS
# =====================================================

st.subheader("Species establishment status")

status_count = (
    species["establishmentMeans"]
    .fillna("Unknown")
    .value_counts()
)


fig, ax = plt.subplots()

status_count.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("")
ax.set_ylabel("Number of species")

st.pyplot(fig)


# =====================================================
# FAMILY RICHNESS
# =====================================================

st.subheader("Species richness by family")

family_count = (
    species.groupby("family")["species"]
    .nunique()
    .sort_values(ascending=False)
    .head(15)
)


fig, ax = plt.subplots()

family_count.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("")
ax.set_ylabel("Species")

st.pyplot(fig)


# =====================================================
# MOST REPRESENTED GENERA
# =====================================================

st.subheader("Most represented genera")

genus_count = (
    species.groupby("genus")["species"]
    .nunique()
    .sort_values(ascending=False)
    .head(15)
)


st.dataframe(
    genus_count.reset_index(
        name="Species"
    ),
    hide_index=True
)