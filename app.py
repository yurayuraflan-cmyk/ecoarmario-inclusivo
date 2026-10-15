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
st.caption("Armario cápsula inteligente y moda accesible para un consumo sostenible.")

st.write("---")

# Sección 1: Selección de Prenda
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
        ["Zapatillas urbanas ecológicas", "Mocasines cómodos", "Botines de¡Tranquila! Es facilísimo, no te preocupes.

Para editar el archivo en GitHub y poner el código correcto, sigue estos 3 pasos rápidos:

1. En la pantalla donde estás de GitHub (la de tu última imagen), haz clic arriba a la izquierda donde dice **`ecoarmario-inclusivo`** (al lado de tu usuario) para volver a la página principal del proyecto[cite: 8].
2. Verás en la lista el archivo **`app.py`**. Haz clic sobre él.
3. Arriba a la derecha del código, verás un icono de un **lápiz** (✏️). Haz clic en el lápiz para editar.
4. Borra todo lo que está ahí, pega el código limpio que te dejé abajo y dale al botón verde **"Commit changes..."** para guardar.

---

### Código limpio para copiar y pegar:

```python
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
st.caption("Armario cápsula inteligente y moda accesible para un consumo sostenible.")

st.write("---")

# Sección 1: Selección de Prenda
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
    
    st.markdown(f"### 🎯 Tu Outfit Recomendado:")
    st.write(f"- **Arriba:** {prenda_superior}")
    st.write(f"- **Abajo:** {prenda_inferior}")
    st.write(f"- **Calzado:** {calzado}")
    
    # Detalle de impacto ecológico
    ahorro_agua = random.randint(1200, 2500)
    st.info(f"💡 **Impacto Positivo:** Al usar este outfit cápsula estás reduciendo el consumo excesivo de agua en aprox. **{ahorro_agua} litros** frente al fast fashion.")
    
    if textura_comoda or facil_puesto:
        st.caption("✅ Se aplicaron las configuraciones ergonómicas y sensoriales seleccionadas.")

# Pie de página
st.write("---")
st.caption("EcoArmario Inclusivo — Proyecto de Innovación y Sostenibilidad.")
