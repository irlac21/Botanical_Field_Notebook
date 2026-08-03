from pathlib import Path
import pandas as pd
import base64
import streamlit as st


# ==========================================================
# CHEMINS DU PROJET
# ==========================================================

PROJECT_DIR = Path(__file__).resolve().parent

DATABASE_DIR = PROJECT_DIR / "Database"

IMAGE_DIR = DATABASE_DIR / "Images"

PHOTO_DIR = PROJECT_DIR / "Photos"

DATABASE_FILE = DATABASE_DIR / "Flora_Bukavu_species_database.xlsx"

SPECIES_IMAGES = DATABASE_DIR / "species_images.xlsx"

BACKGROUND_IMAGE = IMAGE_DIR / "bk.jpg"


# ==========================================================
# CHARGEMENT DE LA BASE
# ==========================================================

@st.cache_data
def load_database():

    if not DATABASE_FILE.exists():
        st.error(f"Database file not found: {DATABASE_FILE}")
        st.stop()

    return pd.read_excel(DATABASE_FILE)


# ==========================================================
# CHARGEMENT BASE IMAGES
# ==========================================================

@st.cache_data
def load_species_images():

    if SPECIES_IMAGES.exists():

        return pd.read_excel(SPECIES_IMAGES)

    return pd.DataFrame()


# ==========================================================
# BACKGROUND HEADER DARK
# ==========================================================

def set_background():

    if not BACKGROUND_IMAGE.exists():

        return


    with open(BACKGROUND_IMAGE, "rb") as file:

        encoded = base64.b64encode(file.read()).decode()


    st.markdown(
        f"""
        <style>

        /* Fond général noir */

        .stApp {{

            background-color: #0b0b0b;

        }}



        /* Image en haut */

        .stApp::before {{

            content: "";

            position: fixed;

            top: 0;

            left: 0;

            width: 100%;

            height: 40vh;


            background-image:

            linear-gradient(
                rgba(0,0,0,0.35),
                rgba(0,0,0,0.35)
            ),

            url("data:image/jpeg;base64,{encoded}");


            background-size: cover;

            background-position: center 65%;

            background-repeat: no-repeat;


            z-index: 0;

        }}



        /* Contenu au-dessus de l'image */

        .block-container {{

            position: relative;

            z-index: 1;

            padding-top: 42vh;

        }}



        </style>
        """,

        unsafe_allow_html=True
    )

# ==========================================================
# STYLE CSS
# ==========================================================

STYLE_FILE = Path(__file__).resolve().parent / "style.css"


def load_css():

    if STYLE_FILE.exists():

        with open(STYLE_FILE) as f:

            st.markdown(

                f"<style>{f.read()}</style>",

                unsafe_allow_html=True

            )