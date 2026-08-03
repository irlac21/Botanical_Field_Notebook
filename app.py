import sys
from pathlib import Path
import streamlit as st

# ==========================================================
# CHEMINS DU PROJET
# ==========================================================

PROJECT_DIR = Path(__file__).resolve().parent

SCRIPTS_DIR = PROJECT_DIR / "Scripts"

PAGES_DIR = SCRIPTS_DIR / "pages"


# Ajouter Scripts aux imports Python
sys.path.insert(0, str(SCRIPTS_DIR))


# ==========================================================
# CONFIGURATION STREAMLIT
# ==========================================================

st.set_page_config(
    page_title="Botanical Field Notebook",
    layout="wide"
)


# ==========================================================
# CHARGEMENT APPLICATION PRINCIPALE
# ==========================================================

with open(SCRIPTS_DIR / "app.py", encoding="utf-8") as f:
    exec(f.read())