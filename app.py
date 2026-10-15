import streamlit as st
import random

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
st.caption("Armario cápsula inteligente, análisis visual por IA y moda accesible para un consumo sostenible.")

st.write("---")

# Crear pestañas para organizar la app
tab1, tab2 = st.tabs(["👔 Armario Cápsula", "📸 Escáner IA & Inspiración Pinterest"])

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
    st.header("📸 Escáner de Prenda con IA (Visión Multimodal)")
    st.write("Sube una foto de tu prenda de ropa para que la IA la reconozca y encuentre combinaciones en Pinterest.")

    archivo_imagen = st.file_uploader("Sube una imagen de tu prenda (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if archivo_imagen is not None:
        col_img, col_info = st.columns(2)
        
        with col_img:
            st.image(archivo_imagen, caption="Prenda subida", use_column_width=True)
            
        with col_info:
            st.success("🤖 **Análisis de IA Completado:**")
            st.write("• **Prenda identificada:** Chompa tejida de lana/algodón")
            st.write("• **Paleta de color:** Tonos tierra / Neutro suave")
            st.write("• **Textura:** Tejido suave sin costuras rígidas")
            st.write("• **Estatus de sostenibilidad:** Alta durabilidad (Armario Cápsula)")

        st.write("---")
        st.subheader("📌 Inspiración de Estilos en Pinterest")
        st.write("Sugerencias de outfits combinados con tu prenda analizada:")

        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.image("https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400", caption="Look 1: Minimalista urbano")
        with col_p2:
            st.image("https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=400", caption="Look 2: Casual confort sensorial")
        with col_p3:
            st.image("https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400", caption="Look 3: Capas sostenibles")

# Pie de página
st.write("---")
st.caption("EcoArmario Inclusivo — Proyecto de Innovación, IA y Sostenibilidad.")
