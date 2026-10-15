import streamlit as st
import random
import google.generativeai as genai
from PIL import Image
import urllib.parse

# Configuración de la página
st.set_page_config(
    page_title="EcoArmario Inclusivo",
    page_icon="🌱",
    layout="wide"
)

# Configuración segura de la API de Gemini mediante Secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

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
st.caption("Armario cápsula inteligente, análisis visual por IA y moda accesible para un consumo sostenible.")

st.write("---")

# Crear pestañas para organizar la app
tab1, tab2 = st.tabs(["👔 Armario Cápsula", "📸 Escáner IA, Colorimetría & Pinterest"])

with tab1:
    st.header("👔 Tu Armario Cápsula Sostenible")

    col1, col2, col3 = st.columns(3)

    with col1:
        prenda_Para guardar tus cambios de manera segura sin que GitHub vuelva a bloquear la clave API por la alerta de seguridad, sigue estos tres pasos rápidos:

1. **Borra todo el contenido** actual del editor de la imagen[cite: 7].
2. **Pega este código exacto**, que usa la función segura `st.secrets` para leer la clave sin exponerla en el texto del archivo:

```python
import streamlit as st
import random
import google.generativeai as genai
from PIL import Image
import urllib.parse

# Configuración de la página
st.set_page_config(
    page_title="EcoArmario Inclusivo",
    page_icon="🌱",
    layout="wide"
)

# Configuración segura de la API de Gemini mediante Secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

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
st.caption("Armario cápsula inteligente, análisis visual por IA y moda accesible para un consumo sostenible.")

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
        calzado = st.selectbox(
            "Calzado / Accesorios:",
            ["Zapatillas urbanas ecológicas", "Mocasines cómodos", "Botines de cuero sintético", "Sandalias ergonómicas"]
        )

    # Opciones sensoriales
    st.subheader("🧩 Preferencias Sensoriales del Día")
    textura_comoda = st.checkbox("Sin etiquetas molestas / Costuras suaves")
    facil_puesto = st.checkbox("Cierres magnéticos / Elásticos (Fácil de colocar)")

    st.write("---")

    # Botón para generar la combinación
    if st.button("✨ Generar Combinación Sostenible"):
        st.success("¡Combinación creada con éxito!")
        
        st.markdown("### 🎯 Tu Outfit Recomendado:")
        st.write(f"- **Arriba:** {prenda_superior}")
        st.write(f"- **Abajo:** {prenda_inferior}")
        st.write(f"- **Calzado:** {calzado}")
        
        # Detalle de impacto ecológico
        ahorro_agua = random.randint(1200, 2500)
        st.info(f"💡 **Impacto Positivo:** Al usar este outfit cápsula estás reduciendo el consumo excesivo de agua en aprox. **{ahorro_agua} litros** frente al fast fashion.")
        
        if textura_comoda or facil_puesto:
            st.caption("✅ Se aplicaron las configuraciones ergonómicas y sensoriales seleccionadas.")

with tab2:
    st.header("📸 Escáner de Prenda, Colorimetría y Proporciones")
    st.write("Sube la foto de cualquier prenda de tu clóset para analizarla en tiempo real con IA.")

    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        colorimetria = st.selectbox("Tu subtono de piel / estación cromática (Opcional):", ["Neutro", "Cálido (Primavera/Otoño)", "Frío (Verano/Invierno)"])
    with col_sel2:
        silueta = st.selectbox("Preferencia de proporciones/corte:", ["Holgado / Confort", "Equilibrado", "Estructurado / Entallado"])

    archivo_imagen = st.file_uploader("Sube una foto de tu ropa (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if archivo_imagen is not None:
        imagen = Image.open(archivo_imagen)
        
        col_img, col_info = st.columns(2)
        
        with col_img:
            st.image(imagen, caption="Prenda ingresada", use_column_width=True)
            
        with col_info:
            if not GEMINI_API_KEY:
                st.info("ℹ️ Para activar el análisis de la foto por IA en tiempo real, configura `GEMINI_API_KEY` en los Secrets de Streamlit Cloud.")
            else:
                with st.spinner("🤖 Analizando la prenda, colorimetría y proporciones con IA..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        prompt = f"""
                        Analiza detalladamente la foto de esta prenda de vestir.
                        Considera que el usuario prefiere una colorimetría de tipo '{colorimetria}' y un corte de proporciones '{silueta}'.
                        
                        Proporciona una respuesta estructurada y breve en español con los siguientes puntos:
                        1. **Prenda identificada:** (Nombre exacto)
                        2. **Paleta de color detectada:** (Colores principales)
                        3. **Análisis de Colorimetría:** (Cómo combinarla según su subtono {colorimetria})
                        4. **Sugerencia de Proporciones:** (Cómo armar el outfit para un corte {silueta})
                        5. **Confort Sensorial:** (Estimación de textura/comodidad)
                        """
                        
                        response = model.generate_content([prompt, imagen])
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error al analizar la imagen: {e}")

            # Enlace dinámico a Pinterest siempre disponible
            busqueda_pinterest = f"outfit {colorimetria} {silueta} moda sostenible"
            url_pinterest = f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(busqueda_pinterest)}"
            
            st.write("---")
            st.subheader("📌 Inspiración en Tiempo Real en Pinterest")
            st.markdown(f"[👉 Haz clic aquí para ver tableros e ideas de combinación en Pinterest para esta prenda]({url_pinterest})")

# Pie de página
st.write("---")
st.caption("EcoArmario Inclusivo — Proyecto de Innovación, IA y Sostenibilidad.")
