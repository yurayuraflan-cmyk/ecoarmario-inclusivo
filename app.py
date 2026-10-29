import streamlit as st
import random
import urllib.parse
from PIL import Image
import requests
import io

# Configuración de la página
st.set_page_config(
    page_title="EcoArmario Inclusivo",
    page_icon="🌱",
    layout="wide"
)

# Estilos CSS para Accesibilidad Sensorial
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Función para generar imágenes con IA (usando Hugging Face gratis)
def generar_imagen_outfit(prompt, api_token=None):
    # Usamos el modelo estable y gratuito SDXL de Hugging Face
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
    # Si el usuario no tiene token, podemos usar un fallback o avisarle, 
    # pero int
api-inference.huggingface.co
