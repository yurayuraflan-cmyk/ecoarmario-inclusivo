import streamlit as st
from PIL import Image
import random
import time

# Configuración principal de la página
st.set_page_config(page_title="Eco Armario", page_icon="🌿", layout="wide")

# Inyección de CSS para colores llamativos, modernos y sin verse "muertos",
# garantizando un alto contraste para facilitar la lectura.
st.markdown("""
    <style>
    .stApp { 
        background-color: #F8FAFC; 
    }
    h1, h2, h3 { 
        color: #0F172A; 
        font-family: 'Arial', sans-serif; 
    }
    /* Botones vibrantes pero elegantes */
    .stButton>button { 
        background-color: #3B82F6; 
        color: white; 
        border-radius: 8px; 
        font-weight: bold; 
        border: none; 
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background-color: #2563EB; 
    }
    /* Etiquetas de accesibilidad visual */
    .accesibilidad-tag { 
        background-color: #FEF3C7; 
        color: #92400E; 
        padding: 8px 15px; 
        border-radius: 20px; 
        font-weight: bold; 
        font-size: 15px; 
        border: 2px solid #F59E0B; 
        display: inline-block;
        margin-top: 10px;
    }
    /* Burbujas de chat IA */
    .chat-user { 
        background-color: #DBEAFE; 
        padding: 15px; 
        border-radius: 10px 10px 0px 10px; 
        margin-bottom: 10px; 
        color: #1E3A8A; 
        text-align: right;
    }
    .chat-ai { 
        background-color: #E2E8F0; 
        padding: 15px; 
        border-radius: 10px 10px 10px 0px; 
        margin-bottom: 10px; 
        color: #334155; 
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 Eco Armario")
st.markdown("Tu asistente de estilo inteligente. Diseñado para que vestirse bien sea fácil, rápido y accesible para todos.")

# Creación de pestañas para dividir las funciones de la aplicación
tab_escaner, tab_ia, tab_armario = st.tabs(["📸 Escáner de Prendas", "🤖 Asistente de Estilo IA", "👕 Mi Armario"])

# --- PESTAÑA 1: ESCÁNER DE ROPA ---
with tab_escaner:
    st.header("Escáner Inteligente")
    st.write("Sube una foto de tu ropa. El sistema identificará qué es y te dirá el color exacto con recomendaciones claras.")
    
    archivo_subido = st.file_uploader("Sube una imagen de tu prenda (JPG, PNG)", type=["jpg", "png", "jpeg"])
    
    if archivo_subido is not None:
        imagen = Image.open(archivo_subido)
        st.image(imagen, caption="Prenda lista para analizar", use_container_width=True)
        
        if st.button("🔍 Analizar Prenda"):
            with st.spinner("Analizando texturas, forma y color..."):
                time.sleep(2) # Simula el tiempo que tarda la IA en procesar la imagen
                
                # Datos simulados que devolvería un modelo de visión real
                tipos = ["Camisa de botones", "Pantalón de vestir", "Chaqueta ligera", "Camiseta básica", "Suéter de lana"]
                colores_accesibles = [
                    "Azul marino (Tono oscuro, similar al cielo de noche)", 
                    "Rojo burdeos (Tono oscuro, similar al vino)", 
                    "Verde oliva (Tono medio, color tierra natural)",
                    "Beige (Tono claro, color arena)"
                ]
                
                tipo_prenda = random.choice(tipos)
                color_detectado = random.choice(colores_accesibles)
                
                st.success("¡Análisis completado con éxito!")
                st.subheader("Resultados de la clasificación:")
                st.write(f"**Tipo de prenda:** {tipo_prenda}")
                st.write(f"**Color exacto detectado:** {color_detectado}")
                
                # Etiqueta especial pensada para usuarios daltónicos
                st.markdown("💡 **Recomendación segura:**")
                st.markdown(f"<div class='accesibilidad-tag'>Esta prenda combina perfecto con colores neutros como Blanco, Gris claro o Negro.</div>", unsafe_allow_html=True)

# --- PESTAÑA 2: ASISTENTE IA ---
with tab_ia:
    st.header("Asistente de Inteligencia Artificial")
    st.write("Dime a dónde vas o qué clima hace, y te armaré el conjunto ideal con lo que tienes.")
    
    # Inicializar el historial de chat si no existe
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

    # Mostrar mensajes anteriores
    for mensaje in st.session_state.mensajes:
        if mensaje["rol"] == "usuario":
            st.markdown(f"<div class='chat-user'>👤 <b>Tú:</b> {mensaje['texto']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>🤖 <b>Eco Armario:</b> {mensaje['texto']}</div>", unsafe_allow_html=True)

    # Caja de texto para hablar con la IA
    entrada_usuario = st.text_input("Ejemplo: 'Tengo una entrevista de trabajo' o 'Hace calor y quiero ir cómodo'")
    
    if st.button("Preguntar a la IA"):
        if entrada_usuario:
            # Se guarda lo que el usuario escribió
            st.session_state.mensajes.append({"rol": "usuario", "texto": entrada_usuario})
            
            # Respuesta simulada de la IA (Aquí conectarías la API real en el futuro)
            respuesta_ia = f"Entendido. Para tu situación ('{entrada_usuario}'), te sugiero usar una base oscura en el pantalón y algo claro arriba para dar contraste. Es una combinación clásica, segura y que siempre se ve elegante. ¿Te gustaría que busque piezas específicas en tu armario?"
            st.session_state.mensajes.append({"rol": "ia", "texto": respuesta_ia})
            st.rerun()

# --- PESTAÑA 3: MI ARMARIO VIRTUAL ---
with tab_armario:
    st.header("Tu colección catalogada")
    st.write("Aquí guardamos todo lo que has escaneado. Los colores están descritos con texto para que nunca dudes al combinar.")
    
    # Mostramos prendas simuladas guardadas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("👖 **Pantalón Vaquero**\n\n*Color:* Azul claro (Celeste)\n\n*Ideal para:* Salidas informales.")
    with col2:
        st.success("👕 **Camisa Manga Corta**\n\n*Color:* Blanco puro\n\n*Ideal para:* Días soleados y calor.")
    with col3:
        st.warning("🧥 **Chaqueta de Invierno**\n\n*Color:* Mostaza (Amarillo oscuro cálido)\n\n*Ideal para:* Dar vida a ropa negra o gris.")
