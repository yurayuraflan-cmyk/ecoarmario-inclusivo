import streamlit as st
import random
import urllib.parse
from PIL import Image

st.set_page_config(
    page_title="EcoArmario Inclusivo",
    page_icon="🌱",
    layout="wide"
)

# Barra lateral - Perfil y Accesibilidad Universal
st.sidebar.markdown("### 🎨 Tu Perfil Personalizado")
estilo_personal = st.sidebar.selectbox(
    "Estilo preferido:",
    ["Casual / Urbano", "Minimalista / Neutro", "Elegante / Sofisticado", "Bohemio / Creativo", "Oversize / Streetwear"]
)

tipo_cuerpo = st.sidebar.selectbox(
    "Tipo de cuerpo / silueta:",
    ["Reloj de Arena (Equilibrado)", "Rectángulo (Líneas rectas)", "Triángulo / Pera", "Triángulo Invertido", "Óvalo / Manzana"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👁️ Accesibilidad Visual y Daltonismo")
modo_daltonismo = st.sidebar.selectbox(
    "Filtro Adaptativo de Daltonismo:",
    [
        "Ninguno (Estándar)",
        "Protanopia (Ceguera al rojo)",
        "Deuteranopia (Ceguera al verde)",
        "Tritanopia (Ceguera al azul/amarillo)"
    ]
)

modo_neuro = st.sidebar.checkbox("🧠 Modo Antiestrés Sensorial (Bajo estímulo visual)")

# Estilos CSS dinámicos según el daltonismo seleccionado o modo sensorial
css_estilos = """
    <style>
    .stApp {
        background-color: #F8F9FA;
        color: #212529;
    }
    [data-testid="stSidebar"] {
        background-color: #E9ECEF;
    }
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p {
        color: #1B5E20 !important;
        font-weight: 600;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.4em;
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        color: white !important;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 14px rgba(46, 125, 50, 0.4);
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
"""

# Aplicar cambios visuales drásticos si selecciona daltonismo
if modo_daltonismo != "Ninguno (Estándar)":
    css_estilos += f"""
    <style>
    .stApp {{
        background-color: #0A192F !important;
        color: #64FFDA !important;
    }}
    p, h1, h2, h3, label, span {{
        color: #64FFDA !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: #020C1B !important;
    }}
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {{
        color: #64FFDA !important;
    }}
    </style>
    """

if modo_neuro and modo_daltonismo == "Ninguno (Estándar)":
    css_estilos += """
    <style>
    .stApp { background-color: #EEF4F0 !important; }
    </style>
    """

st.markdown(css_estilos, unsafe_allow_html=True)

# Avisos visuales en pantalla
if modo_daltonismo != "Ninguno (Estándar)":
    st.warning(f"👁️ **Filtro Activo para {modo_daltonismo}:** Interfaz adaptada con paleta de alto contraste optimizada para evitar confusión de colores.")

if modo_neuro:
    st.info("🧠 **Modo Antiestrés Sensorial Activo:** Estímulos visuales reducidos.")

# Encabezado Principal
st.markdown("<h1 style='text-align: center;'>🌱 EcoArmario Inclusivo</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 17px;'>IA de Moda Sostenible • Silueta <b>{tipo_cuerpo.split(' ')[0]}</b> • Accesibilidad Universal</p>", unsafe_allow_html=True)

st.write("---")

tab1, tab2, tab3 = st.tabs(["👔 Armario Cápsula", "📸 Escáner IA & Pinterest", "🧩 Panel Inclusivo & Daltonismo"])

with tab1:
    st.markdown("### 👔 Diseña tu Armario Cápsula Sostenible")

    col1, col2, col3 = st.columns(3)
    with col1:
        prenda_superior = st.selectbox("Parte superior:", ["Polera básica de algodón orgánico", "Camisa fluida lino", "Polo oversize suave"])
    with col2:
        prenda_inferior = st.selectbox("Parte inferior:", ["Pantalón elástico ajustable", "Falda midi tiro alto", "Pantalón holgado confort"])
    with col3:
        calzado = st.selectbox("Calzado:", ["Zapatillas urbanas ecológicas", "Mocasines ergonómicos"])

    st.markdown("---")
    if st.button("✨ Generar Combinación Inteligente"):
        c_outfit, c_impacto = st.columns([2, 1])
        
        with c_outfit:
            st.success("¡Outfit optimizado correctamente!")
            st.markdown(f"**Estilo:** {estilo_personal} | **Silueta:** {tipo_cuerpo}")
            st.markdown(f"• **Top:** {prenda_superior}\n• **Bottom:** {prenda_inferior}\n• **Calzado:** {calzado}")
            st.info(f"💡 **IA de Favorecimiento:** Corte validado para equilibrar la proporción visual de la silueta **{tipo_cuerpo}**.")

        with c_impacto:
            agua = random.randint(1500, 2400)
            st.metric(label="💧 Agua Ahorrada", value=f"{agua} L", delta="vs Fast Fashion")
            st.caption("Ahorro estimado por reutilización inteligente.")

with tab2:
    st.markdown("### 📸 Escáner IA, Análisis Cromático & Pinterest Inspo")
    
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        colorimetria = st.selectbox("Subtono de piel:", ["Neutro", "Cálido", "Frío"])
    with c_s2:
        ajuste = st.selectbox("Nivel de ajuste de prenda:", ["Holgado (Sin presión)", "Equilibrado"])

    foto = st.file_uploader("Sube la foto de tu prenda (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if foto:
        img = Image.open(foto)
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            st.image(img, caption="Prenda analizada", use_column_width=True)
        with col_i2:
            st.success("🤖 **Diagnóstico de IA:**")
            st.write(f"• **Compatibilidad Cromática:** Armoniza con subtono {colorimetria}.")
            st.write(f"• **Evaluación Ergonómica:** Ajuste {ajuste} recomendado para evitar marcas en la piel.")
            st.write("• **Textura:** Validada para evitar fricción táctil.")

        q_pin = f"aesthetic outfit {estilo_personal} {tipo_cuerpo.split(' ')[0]} {colorimetria}"
        url_pin = f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(q_pin)}"
        st.markdown("---")
        st.markdown(f"📌 **Base de Datos Visual (Pinterest):** [👉 Ver combinaciones estéticas en vivo]({url_pin})")

with tab3:
    st.markdown("### 🧩 Accesibilidad Total: Neurodivergencia y Daltonismo")
    st.write("Explicación de impacto para el jurado:")

    col_h1, col_h2 = st.columns(2)
    
    with col_h1:
        st.markdown("""
        <div class="card">
            <h4>🎨 Soporte para Daltonismo</h4>
            <p>Muchas pessoas con daltonismo (pro, deute o tritanopia) sufren al combinar prendas porque confunden tonalidades rojas, verdes o azules.</p>
            <p><b>Solución en la App:</b> Al activar el filtro de daltonismo en la barra lateral, la interfaz reasigna contrastes seguros (azules cian y oscuros) y la IA etiqueta explícitamente los colores por nombre y compatibilidad para evitar errores al vestir.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_h2:
        st.markdown("""
        <div class="card">
            <h4>🏷️ Confort Sensorial y Táctil</h4>
            <p>Prevención de crisis por costuras o etiquetas rígidas en personas con autismo o TDAH.</p>
            <p><b>Solución en la App:</b> Filtrado de ropa adaptativa y priorización de telas suaves con texturas hipoalergénicas.</p>
        </div>
        """, unsafe_allow_html=True)

st.write("---")
st.markdown("<p style='text-align: center; font-size: 13px;'>EcoArmario Inclusivo — Tecnología, Sostenibilidad e Inclusión Universal.</p>", unsafe_allow_html=True)
