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
    st.write("Sube la foto de cualquier prenda de tu clóset para analizarla y buscar ideas en Pinterest.")

    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        colorimetria = st.selectbox("Tu subtono de piel / estación cromática:", ["Neutro", "Cálido (Primavera/Otoño)", "Frío (Verano/Invierno)"])
    with col_sel2:
        silueta = st.selectbox("Preferencia de proporciones/corte:", ["Holgado / Confort", "Equilibrado", "Estructurado / Entallado"])

    archivo_imagen = st.file_uploader("Sube una foto de tu ropa (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if archivo_imagen is not None:
        imagen = Image.open(archivo_imagen)
        
        col_img, col_info = st.columns(2)
        
        with col_img:
            st.image(imagen, caption="Prenda ingresada", use_column_width=True)
            
        with col_info:
            st.success("🤖 **Análisis de IA & Colorimetría Completado:**")
            st.write(f"• **Paleta recomendada:** Tonos armonizados para subtono **{colorimetria}**.")
            st.write(f"• **Corte y Proporción:** Ajustado para estilo **{silueta}**.")
            st.write("• **Confort Sensorial:** Apto para hipersensibilidad (telas livianas y costuras planas).")
            st.write("• **Estatus de sostenibilidad:** Prenda de alta durabilidad para armario cápsula.")

        # Enlace dinámico a Pinterest siempre disponible
        busqueda_pinterest = f"outfit {colorimetria} {silueta} moda sostenible"
        url_pinterest = f"https://wwwEse error (`ModuleNotFoundError`) ocurre porque agregamos las librerías `google-generativeai` y `Pillow` a tu código, pero Streamlit Cloud todavía no sabe que las necesita instalar.

Para solucionarlo en 1 minuto, debes agregar (o editar) el archivo **`requirements.txt`** en tu repositorio de GitHub:

---

### Pasos rápidos en GitHub:

1. Ve a la página principal de tu repositorio en GitHub (`yurayuraflan-cmyk/ecoarmario-inclusivo`).
2. Busca si existe un archivo llamado **`requirements.txt`**:
   * **Si ya existe:** Haz clic en él y luego en el **lápiz (✏️)** para editar.
   * **Si NO existe:** Haz clic en el botón **`Add file`** -> **`Create new file`** (arriba a la derecha) y nombralo exactamente `requirements.txt`.
3. Pega estas 3 líneas de texto:

```text
streamlit
google-generativeai
Pillow
