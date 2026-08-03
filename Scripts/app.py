import streamlit as st
from app_utils import load_css, set_background


# ==========================================================
# CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Botanical Field Notebook",
    layout="wide"
)


# ==========================================================
# STYLE
# ==========================================================

load_css()
set_background()


st.markdown(
"""
<style>

.block-container {

    padding-top: 33vh;
    padding-bottom: 0.5rem;

}


/* Grand titre */

.home-title {

    color: white;

    font-size: 36px;

    font-weight: 700;

    margin: 0 0 20px 0;

    padding: 0;

}



/* Sous-titre */

.home-subtitle {

    color: white;

    font-size: 21px;

    font-weight: 600;

    margin: 0;

    padding: 0;

}



/* Texte */

.home-text {

    color: white;

    font-size: 16px;

    line-height: 1.25;

    margin: 0;

    padding: 0;

}


</style>
""",
unsafe_allow_html=True
)



# ==========================================================
# ACCUEIL
# ==========================================================

st.markdown(
"""
<div class="home-title">

Botanical Field Notebook

</div>


<div class="home-text">


<div class="home-subtitle">

Digital Botanical Platform

</div>


Welcome to <b>Botanical Field Notebook</b>.<br>
This platform is designed for botanical documentation,
field observations, species identification, and biodiversity
data management.<br>
It supports botanical research, education, and conservation
through the collection, organization, and visualization of
plant diversity data.<br>
Developed to support botanical exploration and biodiversity
documentation.


</div>
""",
unsafe_allow_html=True
)