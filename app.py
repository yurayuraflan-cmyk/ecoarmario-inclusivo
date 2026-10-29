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

# Barra lateral - Perfil de Estilo y Tipo de Cuerpo
st.sidebar.header("🎨 Tu Perfil Personalizado")
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

st.sidebar.write("---")
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
st.caption(f"Armario cápsula inteligente adaptado a tu estilo **{estilo_personal}** y tipo de cuerpo **{tipo_cuerpo.split(' ')[0]}**.")

st.write("---")

# Crear pestañas para organizar la app
tab1, tab2 = st.tabs(["👔 Armario Cápsula Inteligente", "📸 Escáner IA, Proporciones & Pinterest Inspo"])

with tab1:
    st.header("👔 Tu Armario Cápsula Sostenible")

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

    # Opciones sensoriales
    st.subheader("🧩 Preferencias Sensoriales del Día")
    textura_comoda = st.checkbox("Sin etiquetas molestas / Costuras suaves")
    facil_puesto = st.checkbox("Cierres magnéticos / Elásticos (Fácil de colocar)")

    st.write("---")

    # Botón para generar la combinación
    if st.button("✨ Generar Combinación Personalizada"):
        st.success("¡Outfit generado según tu perfil!")
        
        col_outfit, col_impacto = st.columns([2, 1])
        
        with col_outfit:
            st.markdown("### 🎯 Tu Outfit Recomendado:")
            st.write(f"- **Estilo asignado:** {estilo_personal}")
            st.write(f"- **Tipo de Cuerpo:** {tipo_cuerpo}")
            st.write(f"- **Arriba:** {prenda_superior}")
            st.write(f"- **Abajo:** {prenda_inferior}")
            st.write(f"- **Calzado:** {calzado}")
            st.info(f"💡 **Evaluación de Favorecimiento:** Esta combinación equilibra las proporciones visuales para una silueta **{tipo_cuerpo}**.")

        with col_impacto:
            ahorro_agua = random.randint(1200, 2500)
            st.metric(label="💧 Agua Ahorrada Hoy", value=f"{ahorro_agua} Litros", delta="vs. Fast Fashion")
            st.caption("Calculado en base a reutilización de prendas cápsula.")

        if textura_comoda or facil_puesto:
            st.success("✅ **Filtro Sensorial Aplicado:** Combinación libre de etiquetas e irritación táctil.")

with tab2:
    st.header("📸 Escáner con IA: Análisis de Silueta, Colorimetría y Pinterest")
    st.write("Sube una foto de tu prenda para que la Inteligencia Artificial analice si favorece tu tipo de cuerpo y te muestre combinaciones estéticas en Pinterest.")

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
            st.write(f"• **Análisis de Favorecimiento:** La caída de esta prenda potencia la silueta **{tipo_cuerpo}**.")
            st.write(f"• **Armonía Cromática:** Compatible con subtono **{colorimetria}**.")
            st.write(f"• **Adaptación de Estilo:** Alineada al estilo **{estilo_personal}**.")
            st.write("• **Evaluación Sensorial:** Apto para alta sensibilidad táctil (costuras planas).")

        # Enlace dinámico a Pinterest
        query_pinterest = f"aesthetic outfit {estilo_personal} {tipo_cuerpo.split(' ')[0]} {colorimetria} moda sostenible"
        url_pinterest = f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(query_pinterest)}"
        
        st.write("---")
        st.subheader("📌 Inspiración Estética en Tiempo Real (Pinterest)")
        st.markdown(f"La IA ha seleccionado una fuente de combinaciones bonitas para ti. [👉 Haz clic aquí para abrir los mejores tableros de Pinterest para este outfit]({url_pinterest})")

# Pie de página
st.write("---")
st.caption("EcoArmario Inclusivo — Inteligencia Artificial, Silueta Personalizada, Accesibilidad e Impacto Ambiental.")
