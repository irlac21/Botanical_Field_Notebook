import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path


# =====================================================
# DATABASE
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)


query = """

SELECT

field_notes.*,

species.scientificName,
species.family,
species.genus,

locations.country,
locations.province,
locations.territory,
locations.locality,


sampling_units.unitName AS samplingUnitName


FROM field_notes


LEFT JOIN species
ON field_notes.taxonID = species.taxonID


LEFT JOIN locations
ON field_notes.locationID = locations.locationID


LEFT JOIN sampling_units
ON field_notes.samplingUnitID = sampling_units.unitID


ORDER BY field_notes.date DESC

"""


df = pd.read_sql(
    query,
    conn
)


conn.close()



# =====================================================
# PAGE
# =====================================================

st.title("📑 Field Records")


st.markdown(
"""
Browse, review and manage botanical field observations.
"""
)

# =====================================================
# EDIT FORM
# =====================================================

def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0


def safe_int(value):
    try:
        return int(value)
    except:
        return 0



if "edit_noteID" in st.session_state:


    noteID = st.session_state["edit_noteID"]


    conn = sqlite3.connect(DB_FILE)


    record = pd.read_sql(
        """
        SELECT *
        FROM field_notes
        WHERE noteID=?
        """,
        conn,
        params=(noteID,)
    )


    conn.close()



    if len(record) > 0:


        row = record.iloc[0]


        st.subheader("✏️ Edit botanical observation")



        # ==============================
        # TAXONOMY
        # ==============================

        st.markdown("## 🌿 Taxonomy")


        conn = sqlite3.connect(DB_FILE)


        species_df = pd.read_sql(
            """
            SELECT taxonID, scientificName
            FROM species
            ORDER BY scientificName
            """,
            conn
        )


        conn.close()



        current_species = ""

        if pd.notna(row["taxonID"]):

            current = species_df[
                species_df["taxonID"] == row["taxonID"]
            ]

            if len(current)>0:

                current_species = current.iloc[0]["scientificName"]



        species_list = species_df["scientificName"].tolist()



        if current_species in species_list:

            index_species = species_list.index(current_species)

        else:

            index_species = 0



        selected_species = st.selectbox(
            "Scientific name",
            species_list,
            index=index_species
        )



        new_taxonID = species_df[
            species_df["scientificName"] == selected_species
        ]["taxonID"].iloc[0]




        # ==============================
        # GENERAL INFORMATION
        # ==============================


        st.markdown("## 👤 Collector")


        new_observer = st.text_input(
            "Observer",
            value=str(row["observer"])
            if pd.notna(row["observer"])
            else ""
        )


        new_collectorNumber = st.text_input(
            "Collector number",
            value=str(row["collectorNumber"])
            if pd.notna(row["collectorNumber"])
            else ""
        )


        new_date = st.text_input(
            "Collection date",
            value=str(row["date"])
            if pd.notna(row["date"])
            else ""
        )



        # ==============================
        # LOCATION
        # ==============================


        st.markdown("## 📍 Coordinates")


        new_latitude = st.number_input(
            "Latitude",
            value=safe_float(row["latitude"])
        )


        new_longitude = st.number_input(
            "Longitude",
            value=safe_float(row["longitude"])
        )


        new_altitude = st.number_input(
            "Altitude (m)",
            value=safe_float(row["altitude"])
        )




        # ==============================
        # SAMPLING
        # ==============================


        st.markdown("## 🧭 Sampling")


        conn = sqlite3.connect(DB_FILE)


        plots = pd.read_sql(
            """
            SELECT unitID, unitName
            FROM sampling_units
            ORDER BY unitName
            """,
            conn
        )


        conn.close()



        plot_options = ["None"] + plots["unitName"].tolist()


        selected_plot = st.selectbox(
            "Plot",
            plot_options
        )



        if selected_plot != "None":

            new_samplingUnitID = plots[
                plots["unitName"] == selected_plot
            ]["unitID"].iloc[0]

        else:

            new_samplingUnitID = None




        # ==============================
        # ECOLOGY
        # ==============================


        st.markdown("## 🌱 Ecology")


        new_habitat = st.text_input(
            "Habitat",
            value=str(row["habitat"])
            if pd.notna(row["habitat"])
            else ""
        )


        new_phenology = st.text_input(
            "Phenology",
            value=str(row["phenology"])
            if pd.notna(row["phenology"])
            else ""
        )



        # ==============================
        # MEASUREMENTS
        # ==============================


        st.markdown("## 📏 Measurements")


        new_individualCount = st.number_input(
            "Individuals",
            value=safe_int(row["individualCount"])
        )


        new_height = st.number_input(
            "Height (m)",
            value=safe_float(row["height"])
        )


        new_dbh = st.number_input(
            "DBH (cm)",
            value=safe_float(row["dbh"])
        )



        # ==============================
        # NOTES
        # ==============================


        st.markdown("## 📝 Notes")


        new_description = st.text_area(
            "Description",
            value=str(row["description"])
            if pd.notna(row["description"])
            else ""
        )


        new_remarks = st.text_area(
            "Remarks",
            value=str(row["remarks"])
            if pd.notna(row["remarks"])
            else ""
        )



        st.divider()



        col1, col2 = st.columns(2)



        with col1:


            if st.button("💾 Save modifications"):


                conn = sqlite3.connect(DB_FILE)

                cur = conn.cursor()


                cur.execute(
                    """
                    UPDATE field_notes

                    SET

                    taxonID=?,
                    observer=?,
                    collectorNumber=?,
                    date=?,

                    latitude=?,
                    longitude=?,
                    altitude=?,

                    samplingUnitID=?,

                    habitat=?,
                    phenology=?,

                    individualCount=?,
                    height=?,
                    dbh=?,

                    description=?,
                    remarks=?,

                    updatedAt=datetime('now')

                    WHERE noteID=?

                    """,

                    (
                        new_taxonID,

                        new_observer,
                        new_collectorNumber,
                        new_date,

                        new_latitude,
                        new_longitude,
                        new_altitude,

                        new_samplingUnitID,

                        new_habitat,
                        new_phenology,

                        new_individualCount,
                        new_height,
                        new_dbh,

                        new_description,
                        new_remarks,

                        noteID
                    )
                )


                conn.commit()

                conn.close()


                del st.session_state["edit_noteID"]


                st.success(
                    "Observation updated successfully."
                )


                st.rerun()



        with col2:


            if st.button("❌ Cancel"):


                del st.session_state["edit_noteID"]


                st.rerun()

# =====================================================
# OBSERVATION TYPE FILTER
# =====================================================


def get_observation_type(row):

    if pd.notna(row["transectID"]):
        return "Transect"

    elif pd.notna(row["samplingUnitID"]):
        return "Plot"

    else:
        return "Opportunistic"



df["observationType"] = df.apply(
    get_observation_type,
    axis=1
)



obs_filter = st.selectbox(
    "Observation type",
    [
        "All",
        "Opportunistic",
        "Plot",
        "Transect"
    ]
)



if obs_filter != "All":

    df = df[
        df["observationType"] == obs_filter
    ]



# =====================================================
# SEARCH
# =====================================================


search = st.text_input(
    "🔎 Search species, observer or locality"
)


if search:

    df = df[
        df.astype(str)
        .apply(
            lambda row:
            row.str.contains(
                search,
                case=False,
                na=False
            ).any(),
            axis=1
        )
    ]



st.write(
    f"**{len(df)} field records**"
)
# =====================================================
# FIELD NOTE DISPLAY
# =====================================================


for index, row in df.iterrows():

    with st.expander(
        f"📓 {row['scientificName'] if pd.notna(row['scientificName']) else 'Unknown species'} | {row['date']} | {row['observationType']}"
    ):


        st.markdown("## 🌿 Taxon")


        st.write(
            f"**Species:** {row['scientificName'] if pd.notna(row['scientificName']) else 'Not identified'}"
        )


        st.write(
            f"**Family:** {row['family'] if pd.notna(row['family']) else '-'}"
        )


        st.write(
            f"**Genus:** {row['genus'] if pd.notna(row['genus']) else '-'}"
        )



        st.markdown("## 👤 Collector")


        st.write(
            f"**Observer:** {row['observer']}"
        )


        st.write(
            f"**Collection number:** {row['collectorNumber']}"
        )



        st.markdown("## 📍 Locality")
        st.write(
            f"""
            Latitude: {row['latitude']}  
            Longitude: {row['longitude']}  
            Altitude: {row['altitude']} m
            """
        )


        st.write(
            f"""
            Country: {row['country']}  
            Province: {row['province']}  
            Territory: {row['territory']}  
            Locality: {row['locality']}
            """
        )



        st.markdown("## 🌱 Ecology")


        st.write(
            f"**Habitat:** {row['habitat']}"
        )


        st.write(
            f"**Phenology:** {row['phenology']}"
        )



        st.markdown("## 📏 Measurements")


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Individuals",
                int(row["individualCount"])
                if pd.notna(row["individualCount"])
                else 0
            )


        with col2:

            st.metric(
                "Height (m)",
                row["height"]
                if pd.notna(row["height"])
                else 0
            )


        with col3:

            st.metric(
                "DBH (cm)",
                row["dbh"]
                if pd.notna(row["dbh"])
                else 0
            )



        st.markdown("## 📝 Notes")


        if "updatedAt" in row and pd.notna(row["updatedAt"]):

            st.caption(
                f"Last update: {row['updatedAt']}"
            )


        st.write(
            "**Description:**"
        )


        st.write(
            row["description"]
            if pd.notna(row["description"])
            else "-"
        )


        st.write(
            "**Remarks:**"
        )


        st.write(
            row["remarks"]
            if pd.notna(row["remarks"])
            else "-"
        )



        st.markdown("## 🧭 Sampling")


        st.write(
            f"**Type:** {row['observationType']}"
        )


        if row["observationType"] == "Plot":

            st.write(
                f"Sampling unit: {row['samplingUnitName'] if pd.notna(row['samplingUnitName']) else '-'}"
            )


        if row["observationType"] == "Transect":

            st.write(
                f"Transect ID: {row['transectID']}"
            )


        st.markdown("---")


        # =====================================================
        # EDIT RECORD
        # =====================================================

        if st.button(
            "✏️ Edit this record",
            key=f"edit_{row['noteID']}"
        ):

            st.session_state["edit_noteID"] = int(row["noteID"])
            st.rerun()

# =====================================================
# DOWNLOAD CSV
# =====================================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download CSV",
    csv,
    file_name="botanical_field_records.csv",
    mime="text/csv"
)