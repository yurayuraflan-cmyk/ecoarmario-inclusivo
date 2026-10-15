import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="🌱 EcoArmario Inclusivo",
    page_icon="👕",
    layout="wide"
)

# Estilos CSS personalizados para modos de accesibilidad
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F1F8E9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Barra lateral: Opciones de Accesibilidad Sensorial
st.sidebar.header("⚙️ Ajustes de Accesibilidad")
modo_alto_contraste = st.sidebar.checkbox("👁️ Modo Alto Contraste")
modo_sensorial = st.sidebar.checkbox("🧠 Modo Sensorial Reducido (Sin animaciones/colores intensos)")
fuente_grande = st.sidebar.checkbox("🔍 Texto Grande")

if modo_alto_contraste:
    st.markdown("""
        <style>
        .stApp { background-color: #000000; color: #FFFFFF; }
        .card { background-color: #1A1A1A; border-left: 5px solidAquí tienes el código completo y listo para tu archivo `app.py`. 

Solo entra a GitHub, pégalo en el cuadro grande y dale al botón verde **"Commit changes"**:

```python
import streamlit as st
import random

# Configuración de la página
st.set_page_config(
    page_title="EcoArmario Inclusivo",
    page_icon="🌱",
    layout="wide"
)

# Estilos CSS para Accesibilidad Sensorial y Modo Alto Contraste
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
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

# Barra lateral - Ajustes de Accesibilidad
st.sidebar.header("⚙️ Ajustes de Accesibilidad")
modo_lectura = st.sidebar.checkbox("👁️ Modo Alto Contraste / Lectura
