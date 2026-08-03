import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app_utils import load_database

st.set_page_config(
    page_title="Search Species",
    page_icon="🔎",
    layout="wide"
)

df = load_database()

st.title("🔎 Search Species")

st.write(
    "Search and filter plant species from the botanical database."
)

# -------------------------
# SEARCH
# -------------------------

search = st.selectbox(
    "Scientific name",
    [""] + sorted(df["species"].dropna().unique()),
    index=0
)

# -------------------------
# FILTERS
# -------------------------

col1, col2 = st.columns(2)

with col1:

    family = st.selectbox(
        "Family",
        ["All"] + sorted(
            df["family"]
            .dropna()
            .unique()
        )
    )


with col2:

    status = st.selectbox(
        "Establishment status",
        ["All"] + sorted(
            df["establishmentMeans"]
            .dropna()
            .unique()
        )
    )


# -------------------------
# FILTER DATABASE
# -------------------------

result = df.copy()


if search:

    result = result[
        result["species"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]


if family != "All":

    result = result[
        result["family"] == family
    ]


if status != "All":

    result = result[
        result["establishmentMeans"] == status
    ]


st.divider()

if search or family != "All" or status != "All":

    st.write(f"**{len(result)} species found**")

    for _, row in result.head(20).iterrows():

        with st.container(border=True):

            st.subheader(row["species"])

            st.write("**Family:**", row["family"])
            st.write("**Genus:**", row["genus"])
            st.write("**Native range:**", row["nativeRange"])
            st.write("**Establishment status:**", row["establishmentMeans"])
            st.write("**IUCN:**", row["iucnRedListCategory"])
            st.write("**Primary use:**", row["primaryUse"])