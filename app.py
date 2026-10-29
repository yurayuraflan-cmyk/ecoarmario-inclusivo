import streamlit as st
import random
import urllib.parse
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="EcoArmario Inclusivo",
    page_icon="🌱",
    layout="wide"
)

# Estilos CSS Avanzados con corrección absoluta de visibilidad de texto
st.markdown("""
    <style>
    /* Estilos generales */
    .stApp {
        background-color: #FAFAFA;
        color: #222222;
    }
    
    /* Forzar color y visibilidad clara en la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #F1F8F5;
    }
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #1B5E20 !important;
        font-weight: 600;
    }
    
    /* Botones principales modernos con degradado */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.2em;
