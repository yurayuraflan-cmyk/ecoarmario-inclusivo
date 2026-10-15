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

# Barra lateral - Ajustes de Accesibilidad
st.sidebar.header("⚙️ Ajustes de Accesibilidad")
modo_lectura = st.sidebar.checkbox("👁️ Modo Alto Contraste / Lectura Fácil")
reducir_estimulos = st.sidebar.checkbox("🧠 Modo Sensorial Amigable (Bajo estímulo visual)")

if modo_lectura:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #000000 !important;
            color: #FFFF00 !important;
        }
        p, h1, h2, h3, label {
            color: #FFFF00 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Título Principal
st.title("🌱 EcoArmario Inclusivo")
st.caption("Armario cápsula inteligente, análisis visual y moda accesible para un consumo sostenible.")

st.write("---")

# Crear pestañas para organizar la app
tab1, tab2 = st.tabs(["👔 Armario Cápsula", "📸 Escáner IA, Colorimetría & Pinterest"])

with tab1:
    st.header("👔 Tu Armario Cápsula Sostenible")

    col1, col2, col3 = st.columns(3)

    with col1:
        prenda_superior = st.selectbox(
            "Prenda Superior (Parte de arriba):",
            ["Polera básica neutra", "Camisa de algodón orgánico", "Polo oversize pastel", "Chompa tejida reciclada"]
        )

    with col2:
        prenda_inferior = st.selectbox(
            "Prenda Inferior (Parte de abajo):",
            ["Pantalón denim reciclado", "Pantalón holgado beige", "Falda midi sostenible", "Pantalón deportivo neutro"]
        )

    with col3:
        calzado =Ese error (`ModuleNotFoundError`) en la línea 3 indica que Streamlit Cloud no encuentra instalado el paquete `google-generativeai`[cite: 7]. 

Tienes dos opciones rápidas para solucionarlo:

---

### Opción 1: Crear o editar el archivo `requirements.txt` (Solución rápida con IA)

Para que Streamlit Cloud sepa qué librerías descargar automáticamente:

1. Ve a la vista principal de tu repositorio en GitHub (`yurayuraflan-cmyk/ecoarmario-inclusivo`).
2. Verifica si tienes un archivo llamado `requirements.txt`:
   * **Si ya existe:** Haz clic sobre él, presiona el icono del lápiz (✏️) y añade las librerías.
   * **Si no existe:** Haz clic en **Add file** -> **Create new file**, y ponle de nombre exacto `requirements.txt`.
3. Pega este texto dentro del archivo:
   ```text
   streamlit
   google-generativeai
   Pillow
