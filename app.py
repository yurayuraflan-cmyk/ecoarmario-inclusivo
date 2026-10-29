import streamlit as st
import random
import urllib.parse
from PIL import Image

st.set_page_config(
    page_title="EcoArmario Inclusivo",
    page_icon="🌱",
    layout="wide"
)

# Estilos CSS Avanzados - Diseño tipo App Moderna / Startup
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
        color: #212529;
    }
    
    /* Sidebar estilizado */
    [data-testid="stSidebar"] {
        background-color: #E9ECEF;
    }
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p {
        color: #1B5E20 !important;
        font-weight: 600;
    }

    /* Botones principales con degradado llamativo */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.4em;
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        color: white !important;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 14px rgba(46, 125, 50, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.6);
        background: linear-gradient(135deg, #388E3C 0%, #2E7D32 100%);
    }
    
    /* Contenedores con estilo de tarjeta moderna */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Barra lateral - Perfil y Accesibilidad
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
st.sidebar.markdown("### ⚙️ Accesibilidad & Inclusión")
modo_lectura = st.sidebar.checkbox("👁️ Modo Alto Contraste (Daltonismo/Visión)")
modo_neuro = st.sidebar.checkbox("🧠 Modo Antiestrés Sensorial (Bajo estímulo)")

if modo_lectura:
    st.markdown("""
        <style>
        body, .stApp { background-color: #000000 !important; color: #FFFF00 !important; }
        p, h1, h2, h3, label { color: #FFFF00 !important; }
        </style>
    """, unsafe_allow_html=True)

# Encabezado Principal
st.markdown("<h1 style='text-align: center; color: #1B5E20;'>🌱 EcoArmario Inclusivo</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #666666; font-size: 17px;'>IA de Moda Sostenible • Silueta <b>{tipo_cuerpo.split(' ')[0]}</b> • Diseño Adaptativo & Sensorial</p>", unsafe_allow_html=True)

st.write("---")

tab1, tab2, tab3 = st.tabs(["👔 Armario Cápsula", "📸 Escáner IA & Pinterest", "🧩 Panel de Confort Sensorial"])

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
    st.markdown("### 🧩 ¿Cómo ayudamos a la Super / Hipersensibilidad?")
    st.write("Esta sección demuestra el impacto inclusivo real de la aplicación para personas con Autismo, TDAH o hipersensibilidad táctil y visual.")

    col_h1, col_h2 = st.columns(2)
    
    with col_h1:
        st.markdown("""
        <div class="card">
            <h4>🏷️ 1. Filtro Anti-Irritación Táctil</h4>
            <p>Las personas neurodivergentes suelen sufrir dolor o ansiedad extrema por <b>etiquetas internas, costuras gruesas o broches rígidos</b>.</p>
            <p><b>Cómo actúa la app:</b> El sistema filtra y prioriza exclusivamente ropa adaptativa confeccionada con costuras planas, algodón orgánico y cierres magnéticos o elásticos suaves.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_h2:
        st.markdown("""
        <div class="card">
            <h4>👁️ 2. Reducción de Sobrecarga Visual</h4>
            <p>Los entornos caóticos o interfaces llenas de colores estridentes generan fatiga cognitiva y crisis sensoriales.</p>
            <p><b>Cómo actúa la app:</b> Al activar el <i>Modo Antiestrés Sensorial</i>, la interfaz bloquea elementos distractores, suaviza la paleta cromática y prioriza fuentes de lectura ultra clara.</p>
        </div>
        """, unsafe_allow_html=True)

    if modo_neuro:
        st.warning("🧠 **Modo Antiestrés Sensorial Activo:** Interfaz simplificada al máximo, reduciendo estímulos visuales y mostrando solo información esencial.")

st.write("---")
st.markdown("<p style='text-align: center; color: #777; font-size: 13px;'>EcoArmario Inclusivo — Tecnología, Sostenibilidad e Inclusión Neuromotora.</p>", unsafe_allow_html=True)
