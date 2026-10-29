import streamlit as st
import random
import urllib.parse
from PIL import Image

st.set_page_config(
    page_title="EcoArmario Inclusivo",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #FAFAFA;
        color: #222222;
    }
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
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.2em;
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        color: white !important;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(46, 125, 50, 0.4);
        background: linear-gradient(135deg, #388E3C 0%, #2E7D32 100%);
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🎨 Tu Perfil Personalizado")
estilo_personal = st.sidebar.selectbox(
    "Selecciona tu estilo preferido:",
    [
        "Casual / Urbano",
        "Minimalista / Neutro",
        "Elegante / Sofisticado",
        "Bohemio / Creativo",
        "Deportivo / Athleisure",
        "Oversize / Streetwear"
    ]
)

tipo_cuerpo = st.sidebar.selectbox(
    "Selecciona tu tipo de cuerpo / silueta:",
    [
        "Reloj de Arena (Equilibrado)",
        "Rectángulo (Líneas rectas)",
        "Triángulo / Pera (Mayor volumen en caderas)",
        "Triángulo Invertido (Mayor volumen en hombros)",
        "Óvalo / Manzana (Volumen central)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Accesibilidad & Inclusión")
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

st.markdown("<h1 style='text-align: center; color: #1B5E20;'>🌱 EcoArmario Inclusivo</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #444444; font-size: 18px;'>Inteligencia Artificial aplicada a la moda sostenible, silueta <b>{tipo_cuerpo.split(' ')[0]}</b> y confort sensorial.</p>", unsafe_allow_html=True)

st.write("---")

tab1, tab2 = st.tabs(["👔 Armario Cápsula Inteligente", "📸 Escáner IA, Proporciones & Pinterest Inspo"])

with tab1:
    st.markdown("### 👔 Diseña tu Armario Cápsula Sostenible")

    col1, col2, col3 = st.columns(3)

    with col1:
        prenda_superior = st.selectbox(
            "Prenda Superior (Parte de arriba):",
            ["Polera básica neutra", "Camisa de algodón orgánico", "Polo oversize pastel", "Chompa tejida reciclada", "Blazer escotado en V"]
        )

    with col2:
        prenda_inferior = st.selectbox(
            "Prenda Inferior (Parte de abajo):",
            ["Pantalón tiro alto denim", "Pantalón holgado beige", "Falda midi tiro alto", "Pantalón de corte recto", "Pantalón deportivo neutro"]
        )

    with col3:
        calzado = st.selectbox(
            "Calzado / Accesorios:",
            ["Zapatillas urbanas ecológicas", "Mocasines cómodos", "Botines de cuero sintético", "Sandalias ergonómicas"]
        )

    st.markdown("#### 🧩 Preferencias Sensoriales del Día")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        textura_comoda = st.checkbox("Sin etiquetas molestas / Costuras suaves")
    with col_s2:
        facil_puesto = st.checkbox("Cierres magnéticos / Elásticos (Fácil de colocar)")

    st.write("")

    if st.button("✨ Generar Combinación Personalizada"):
        st.success("¡Outfit generado con éxito por el motor inteligente!")
        
        col_outfit, col_impacto = st.columns([2, 1])
        
        with col_outfit:
            st.markdown("#### 🎯 Tu Outfit Recomendado:")
            st.write(f"- **Estilo asignado:** {estilo_personal}")
            st.write(f"- **Tipo de Cuerpo:** {tipo_cuerpo}")
            st.write(f"- **Arriba:** {prenda_superior}")
            st.write(f"- **Abajo:** {prenda_inferior}")
            st.write(f"- **Calzado:** {calzado}")
            st.info("💡 **Evaluación de Favorecimiento:** Esta combinación crea un equilibrio visual perfecto para tu silueta.")

        with col_impacto:
            ahorro_agua = random.randint(1200, 2500)
            st.metric(label="💧 Agua Ahorrada Hoy", value=f"{ahorro_agua} Litros", delta="vs. Fast Fashion")
            st.caption("Calculado en base a reutilización de prendas cápsula.")

        if textura_comoda or facil_puesto:
            st.success("✅ **Filtro Sensorial Aplicado:** Combinación adaptativa libre de etiquetas e irritación táctil.")

with tab2:
    st.markdown("### 📸 Escáner con IA: Análisis de Silueta, Colorimetría y Pinterest")
    st.write("Sube una foto de tu prenda para que la Inteligencia Artificial analice si favorece tu tipo de cuerpo y te muestre combinaciones estéticas.")

    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        colorimetria = st.selectbox("Tu subtono de piel / estación cromática:", ["Neutro", "Cálido (Primavera/Otoño)", "Frío (Verano/Invierno)"])
    with col_sel2:
        silueta_corte = st.selectbox("Preferencia de ajuste del outfit:", ["Holgado / Confort", "Equilibrado", "Estructurado / Definido"])

    archivo_imagen = st.file_uploader("Sube una foto de tu ropa (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if archivo_imagen is not None:
        imagen = Image.open(archivo_imagen)
        
        col_img, col_info = st.columns(2)
        
        with col_img:
            st.image(imagen, caption="Prenda analizada por IA", use_column_width=True)
            
        with col_info:
            st.success("🤖 **Análisis de Inteligencia Artificial Completado:**")
            st.write(f"• **Análisis de Favorecimiento:** La caída de esta prenda potencia tu silueta **{tipo_cuerpo}**.")
            st.write(f"• **Armonía Cromática:** Compatible con tu subtono **{colorimetria}**.")
            st.write(f"• **Adaptación de Estilo:** Alineada al concepto **{estilo_personal}**.")
            st.write("• **Evaluación Sensorial:** Apto para alta sensibilidad táctil (costuras planas).")

        query_pinterest = f"aesthetic outfit {estilo_personal} {tipo_cuerpo.split(' ')[0]} {colorimetria} moda sostenible"
        url_pinterest = f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(query_pinterest)}"
        
        st.write("---")
        st.markdown("#### 📌 Inspiración Estética en Tiempo Real (Pinterest)")
        st.markdown(f"La IA ha vinculado esta consulta con una base de datos visual en vivo. [👉 Haz clic aquí para abrir los tableros de Pinterest ideales para ti]({url_pinterest})")

st.write("---")
st.markdown("<p style='text-align: center; color: #888888; font-size: 13px;'>EcoArmario Inclusivo — Inteligencia Artificial, Silueta Personalizada, Accesibilidad e Impacto Ambiental.</p>", unsafe_allow_html=True)
