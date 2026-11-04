import streamlit as st
from PIL import Image
import requests
import io
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="EcoArmario", page_icon="👗", layout="wide")

# --- ESTILOS CSS (Colorido pero suave a la vista) ---
st.markdown("""
    <style>
    .stApp { background-color: #F9F7F3; } /* Fondo crema muy suave */
    h1, h2, h3 { color: #2C5F2D; } /* Verde naturaleza para títulos */
    .stButton>button {
        background-color: #97BC62; /* Verde pastel colorido */
        color: white;
        border-radius: 10px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #2C5F2D; }
    </style>
""", unsafe_allow_html=True)

# --- MEMORIA DE LA APLICACIÓN ---
# Aquí guardamos la ropa que el usuario va subiendo mientras usa la app
if 'mi_closet' not in st.session_state:
    st.session_state.mi_closet = {'Parte superior': [], 'Parte inferior': [], 'Calzado': []}

# --- FUNCIONES DE INTELIGENCIA ARTIFICIAL ---
def analizar_prenda_con_ia(imagen, api_key):
    """Usa la IA para mirar la foto y decirnos qué tipo de prenda es y su color."""
    try:
        genai.configure(api_key=api_key)
        modelo = genai.GenerativeModel('gemini-1.5-flash')
        respuesta = modelo.generate_content([
            "Eres un experto en moda. Analiza esta prenda. Responde SOLO con el tipo de prenda (Parte superior, Parte inferior o Calzado), seguido de un guión, y luego el color principal y textura. Ejemplo: 'Parte superior - Camisa azul de algodón'.", 
            imagen
        ])
        return respuesta.text.strip()
    except Exception as e:
        return "Error al analizar la prenda. Revisa tu clave de IA."

def generar_imagen_outfit(descripcion, api_token):
    """Usa una IA de imágenes para dibujar el outfit recomendado."""
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {api_token}"} if api_token else {}
    try:
        # Traducimos a inglés internamente porque las IAs de dibujo entienden mejor
        prompt = f"A beautiful aesthetic flat lay photograph of an outfit consisting of {descripcion}. Sustainable fashion, natural lighting, soft pastel background."
        respuesta = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        if respuesta.status_code == 200:
            return Image.open(io.BytesIO(respuesta.content))
        return None
    except:
        return None

# --- BARRA LATERAL: PERFIL DEL USUARIO ---
st.sidebar.title("🎨 Tu Perfil en EcoArmario")
tipo_cuerpo = st.sidebar.selectbox("Tu tipo de cuerpo:", ["Reloj de Arena", "Triángulo", "Triángulo Invertido", "Rectángulo", "Óvalo"])
daltonismo = st.sidebar.selectbox("¿Tienes algún tipo de daltonismo?", ["Ninguno", "Protanopía (Rojo-Verde)", "Deuteranopía (Verde-Rojo)", "Tritanopía (Azul-Amarillo)"])

st.sidebar.divider()
st.sidebar.caption("🔑 Claves para encender la Inteligencia Artificial")
gemini_key = st.sidebar.text_input("Clave de Google Gemini (Para leer fotos y dar consejos):", type="password")
hf_key = st.sidebar.text_input("Clave de Hugging Face (Para generar las imágenes):", type="password")

# --- TÍTULO PRINCIPAL ---
st.title("👗 EcoArmario")
st.write("Redescubre tu clóset, combina con confianza y viste de forma sostenible sin tener que comprar ropa nueva.")

# --- PESTAÑAS DE LA APLICACIÓN ---
tab1, tab2 = st.tabs(["📸 Agrega Ropa a tu Clóset", "✨ Crea tu Outfit Inclusivo"])

# PESTAÑA 1: SUBIR Y CATEGORIZAR ROPA
with tab1:
    st.header("1. Digitaliza tus prendas")
    st.write("Súbele fotos a la IA y ella las ordenará por ti mágicamente.")
    
    foto_subida = st.file_uploader("Sube una foto de tu prenda (Polo, pantalón, zapatos...)", type=["jpg", "png"])
    
    if foto_subida and gemini_key:
        imagen_prenda = Image.open(foto_subida)
        st.image(imagen_prenda, width=250)
        
        if st.button("Analizar y Guardar en mi Clóset"):
            with st.spinner("La IA está mirando tu prenda..."):
                resultado = analizar_prenda_con_ia(imagen_prenda, gemini_key)
                st.success(f"¡Prenda detectada! {resultado}")
                
                # Guardamos la prenda en la categoría correcta
                if "superior" in resultado.lower():
                    st.session_state.mi_closet['Parte superior'].append(resultado)
                elif "inferior" in resultado.lower():
                    st.session_state.mi_closet['Parte inferior'].append(resultado)
                elif "calzado" in resultado.lower() or "zapat" in resultado.lower():
                    st.session_state.mi_closet['Calzado'].append(resultado)
                else:
                    st.session_state.mi_closet['Parte superior'].append(resultado) # Por defecto
                    
    elif foto_subida and not gemini_key:
        st.warning("Pon tu clave de Gemini en el menú izquierdo para poder leer la foto.")

    st.divider()
    st.subheader("Tu Clóset Digital Actual:")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.write("**Partes Superiores**")
        for prenda in st.session_state.mi_closet['Parte superior']: st.write(f"👕 {prenda.split('-')[-1]}")
    with col_b:
        st.write("**Partes Inferiores**")
        for prenda in st.session_state.mi_closet['Parte inferior']: st.write(f"👖 {prenda.split('-')[-1]}")
    with col_c:
        st.write("**Calzado**")
        for prenda in st.session_state.mi_closet['Calzado']: st.write(f"👟 {prenda.split('-')[-1]}")

# PESTAÑA 2: ARMAR EL OUTFIT
with tab2:
    st.header("2. Deja que la IA arme tu estilo")
    st.write("Selecciona qué ropa de tu clóset quieres usar hoy, y la IA te dirá si combinan y cómo se ven.")
    
    # Solo mostramos opciones si hay ropa en el clóset
    if not st.session_state.mi_closet['Parte superior']:
        st.info("Primero sube algo de ropa en la pestaña anterior para poder armar un outfit.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            sup = st.selectbox("Elige parte superior", st.session_state.mi_closet['Parte superior'])
        with col2:
            inf = st.selectbox("Elige parte inferior", st.session_state.mi_closet['Parte inferior'] if st.session_state.mi_closet['Parte inferior'] else ["Pantalón básico"])
        with col3:
            calz = st.selectbox("Elige calzado", st.session_state.mi_closet['Calzado'] if st.session_state.mi_closet['Calzado'] else ["Zapatos cómodos"])

        if st.button("✨ Evaluar Outfit y Generar Imagen"):
            if not gemini_key:
                st.error("Necesitas tu clave de Google Gemini en la barra lateral para recibir consejos.")
            else:
                col_texto, col_imagen = st.columns([1, 1])
                
                with col_texto:
                    st.subheader("💡 Consejo de Estilo Inclusivo")
                    with st.spinner("Escribiendo consejos..."):
                        genai.configure(api_key=gemini_key)
                        modelo_texto = genai.GenerativeModel('gemini-1.5-flash')
                        
                        prompt_consejo = f"""
                        El usuario ha combinado: {sup}, {inf} y {calz}.
                        Su tipo de cuerpo es: {tipo_cuerpo}.
                        Su condición visual es: {daltonismo}.
                        Escribe un consejo corto, amable y motivador sobre cómo esta ropa favorece su cuerpo. 
                        Si tiene daltonismo, explícale de forma muy sencilla cómo contrastan o armonizan estos colores para que sienta seguridad al vestirse.
                        Termina con un consejo sobre cómo reutilizar estas prendas en lugar de comprar nuevas.
                        """
                        consejo = modelo_texto.generate_content(prompt_consejo)
                        st.write(consejo.text)
                
                with col_imagen:
                    st.subheader("🖼️ Así se vería tu combinación")
                    if hf_key:
                        with st.spinner("Dibujando el outfit..."):
                            outfit_desc = f"{sup}, {inf}, and {calz}"
                            img_outfit = generar_imagen_outfit(outfit_desc, hf_key)
                            if img_outfit:
                                st.image(img_outfit, use_container_width=True)
                            else:
                                st.error("No se pudo generar la imagen. Intenta de nuevo.")
                    else:
                        st.info("Coloca tu clave de Hugging Face en el menú para ver la imagen de tu outfit.")
