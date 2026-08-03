import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Information",
    page_icon="ℹ️",
    layout="wide"
)

# =====================================================
# IMAGE
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
photo = PROJECT_DIR / "assets" / "land.png"

# =====================================================
# TITLE
# =====================================================

st.title("Botanical Field Notebook")

st.write("")
st.write("")

# =====================================================
# DEVELOPED BY
# =====================================================

left, right = st.columns([3.5, 1.5], vertical_alignment="center")

with left:

    st.markdown("""
## Developed by

### IRAGI CIGANGU Landry

**Botanist**

📧 **iragi.cigangu_21@uob.ac.cd**

📍 **Bukavu, DR Congo**

**Université Officielle de Bukavu (UOB)**

**Centre de Recherche en Ecologie et Gestion des Ecosystèmes Terrestres (CREGET)**

**Centre d'Expertise en Botanique Congolaise (CEBOC)**
""")

with right:

    if photo.exists():
        st.image(photo, width=220)

st.divider()

# =====================================================
# ABOUT
# =====================================================

st.header("About the Platform")

st.write("""
Botanical Field Notebook is a digital platform designed for botanical
documentation, plant diversity surveys, field observations and biodiversity
data management.

The application provides an efficient workflow for recording, organizing,
editing and visualizing botanical observations collected during fieldwork,
supporting botanical research, education and biodiversity documentation.
""")

# =====================================================
# FEATURES
# =====================================================

st.header("Main Features")

st.markdown("""
- Botanical species database

- Search species

- Digital botanical field notebook

- Field records management

- Observation map

- Biodiversity statistics
""")

# =====================================================
# TECHNOLOGY
# =====================================================

st.header("Technology Stack")

st.markdown("""
- Python

- Streamlit

- SQLite

- Pandas

- Matplotlib
""")

# =====================================================
# GEOSPATIAL
# =====================================================

st.header("Geospatial Resources")

st.write("""
Mapping and geolocation features are supported by **OpenStreetMap**, while
**Google Maps Street View** may be used to assist in the visual verification
of observation localities and surrounding environments when imagery is
available.
""")

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption("""
Botanical Field Notebook • Version 1.0.0

© 2026 IRAGI CIGANGU Landry
""")