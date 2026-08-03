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

    st.error(
        f"Database not found: {DB_FILE}"
    )

    st.stop()


# Connexion SQLite
conn = sqlite3.connect(
    str(DB_FILE)
)


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
Explore biodiversity patterns by project.
"""
)



# =====================================================
# PROJECT SELECTION
# =====================================================

st.subheader("📁 Select project")


active_projects = projects[
    projects["deleted"] == 0
]



if len(active_projects) == 0:

    st.warning(
        "No active projects available."
    )

    st.stop()



project_options = (
    active_projects["project_name"]
    .sort_values()
    .tolist()
)



selected_project = st.selectbox(
    "Choose a project",
    project_options
)



selected_project_id = active_projects[
    active_projects["project_name"] == selected_project
]["project_id"].iloc[0]



# =====================================================
# LOAD SELECTED PROJECT RECORDS
# =====================================================


conn = sqlite3.connect(
    str(DB_FILE)
)


project_records = pd.read_sql(
    """

    SELECT *

    FROM field_notes

    WHERE projectID = ?

    AND deleted = 0

    """,

    conn,

    params=(
        int(selected_project_id),
    )
)


conn.close()
# =====================================================
# PROJECT SPECIES
# =====================================================

project_taxa = project_records[
    project_records["taxonID"].notna()
]["taxonID"].unique()



project_species = species[
    species["taxonID"].isin(project_taxa)
]



# =====================================================
# PROJECT OVERVIEW
# =====================================================

st.divider()


st.subheader(
    f"📁 {selected_project} overview"
)



col1, col2, col3, col4 = st.columns(4)



col1.metric(
    "📑 Records",
    len(project_records)
)



col2.metric(
    "Species",
    project_species["species"].nunique()
)



col3.metric(
    "Families",
    project_species["family"].nunique()
)



col4.metric(
    "Collectors",
    project_records["observer"].nunique()
)



col1, col2, col3, col4 = st.columns(4)



col1.metric(
    "📍 Localities",
    project_records["locationID"].nunique()
)



col2.metric(
    "Sampling units",
    project_records["samplingUnitID"].nunique()
)



col3.metric(
    "First observation",
    project_records["date"].min()
    if len(project_records) > 0
    else "-"
)



col4.metric(
    "Last observation",
    project_records["date"].max()
    if len(project_records) > 0
    else "-"
)



st.divider()

# =====================================================
# OBSERVATION TYPES
# =====================================================

st.subheader("Observation Types in selected project")


# Utiliser uniquement les observations du projet choisi

if len(project_records) > 0:


    opportunistic = project_records[
        project_records["samplingUnitID"].isna()
        &
        project_records["transectID"].isna()
    ]


    plot = project_records[
        project_records["samplingUnitID"].notna()
    ]


    transect = project_records[
        project_records["transectID"].notna()
    ]



    col1, col2, col3 = st.columns(3)



    # =====================================================
    # OPPORTUNISTIC
    # =====================================================

    with col1:

        st.markdown(
            "### Opportunistic"
        )


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
            opportunistic["individualCount"]
            .fillna(0)
            .sum()
        )



    # =====================================================
    # PLOTS
    # =====================================================

    with col2:

        st.markdown(
            "### Plot"
        )


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
            plot["individualCount"]
            .fillna(0)
            .sum()
        )


        st.metric(
            "Mean DBH",
            round(
                plot["dbh"].mean(),
                2
            )
            if plot["dbh"].notna().any()
            else 0
        )



    # =====================================================
    # TRANSECTS
    # =====================================================

    with col3:

        st.markdown(
            "### Transect"
        )


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
            transect["individualCount"]
            .fillna(0)
            .sum()
        )


        st.metric(
            "Mean DBH",
            round(
                transect["dbh"].mean(),
                2
            )
            if transect["dbh"].notna().any()
            else 0
        )


else:

    st.info(
        "No observations available for this project."
    )


st.divider()

# =====================================================
# OBSERVATIONS BY TYPE
# =====================================================

st.subheader(
    "Observations by Type in selected project"
)



if len(project_records) > 0:


    obs_type = pd.DataFrame(
        {
            "Type": [
                "Opportunistic",
                "Plot",
                "Transect"
            ],

            "Observations": [

                len(
                    project_records[
                        project_records["samplingUnitID"].isna()
                        &
                        project_records["transectID"].isna()
                    ]
                ),


                len(
                    project_records[
                        project_records["samplingUnitID"].notna()
                    ]
                ),


                len(
                    project_records[
                        project_records["transectID"].notna()
                    ]
                )
            ]
        }
    )



    fig, ax = plt.subplots(
        figsize=(6,4)
    )


    ax.bar(
        obs_type["Type"],
        obs_type["Observations"]
    )


    ax.set_xlabel(
        ""
    )


    ax.set_ylabel(
        "Number of observations"
    )


    ax.set_title(
        f"Observation types - {selected_project}"
    )



    for i, v in enumerate(
        obs_type["Observations"]
    ):

        ax.text(
            i,
            v,
            str(v),
            ha="center",
            va="bottom"
        )



    st.pyplot(fig)



else:


    st.info(
        "No observations available for this project."
    )


st.divider()

# =====================================================
# ORIGIN / ESTABLISHMENT STATUS
# =====================================================

st.subheader(
    "Species establishment status in selected project"
)



if len(project_species) > 0:


    status_count = (
        project_species["establishmentMeans"]
        .fillna("Unknown")
        .value_counts()
    )



    fig, ax = plt.subplots(
        figsize=(6,4)
    )


    status_count.plot(
        kind="bar",
        ax=ax
    )


    ax.set_xlabel(
        ""
    )


    ax.set_ylabel(
        "Number of species"
    )


    ax.set_title(
        f"Establishment status - {selected_project}"
    )


    plt.xticks(
        rotation=45,
        ha="right"
    )


    st.pyplot(fig)



else:


    st.info(
        "No identified species available for this project."
    )


st.divider()


# =====================================================
# FAMILY RICHNESS
# =====================================================

st.subheader(
    "Species richness by family in selected project"
)



if len(project_species) > 0:


    family_count = (
        project_species
        .groupby("family")["species"]
        .nunique()
        .sort_values(
            ascending=False
        )
        .head(15)
    )



    fig, ax = plt.subplots(
        figsize=(8,5)
    )


    family_count.plot(
        kind="bar",
        ax=ax
    )


    ax.set_xlabel(
        ""
    )


    ax.set_ylabel(
        "Number of species"
    )


    ax.set_title(
        f"Top families - {selected_project}"
    )


    plt.xticks(
        rotation=45,
        ha="right"
    )


    st.pyplot(fig)



else:


    st.info(
        "No identified species available for this project."
    )


st.divider()


# =====================================================
# MOST REPRESENTED GENERA
# =====================================================

st.subheader(
    "Most represented genera in selected project"
)



if len(project_species) > 0:


    genus_count = (
        project_species
        .groupby("genus")["species"]
        .nunique()
        .sort_values(
            ascending=False
        )
        .head(15)
    )



    # -------------------------------
    # GRAPH
    # -------------------------------

    fig, ax = plt.subplots(
        figsize=(8,5)
    )


    genus_count.plot(
        kind="bar",
        ax=ax
    )


    ax.set_xlabel(
        ""
    )


    ax.set_ylabel(
        "Number of species"
    )


    ax.set_title(
        f"Top genera - {selected_project}"
    )


    plt.xticks(
        rotation=45,
        ha="right"
    )


    st.pyplot(fig)



    # -------------------------------
    # TABLE
    # -------------------------------

    st.markdown(
        "### Genus summary"
    )


    st.dataframe(
        genus_count
        .reset_index(
            name="Species"
        ),
        hide_index=True,
        use_container_width=True
    )



else:


    st.info(
        "No identified species available for this project."
    )