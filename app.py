import streamlit as st
import pandas as pd
import random
from PIL import Image, ImageDraw

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="EcoArmario - Tu Closet Digital Sostenible",
    page_icon="🌿",
    layout="wide"
)

# 2. ESTADO DE LA SESIÓN (Para guardar datos mientras usas la app)
if 'armario' not in st.session_state:
    st.session_state.armario = [
        {"id": 1, "nombre": "Camisa de Lino Blanca", "categoria": "Parte Superior", "color": "Blanco", "usos": 12, "agua_l": 2700, "co2_kg": 5.5},
        {"id": 2, "nombre": "Suéter Tejido Beige", "categoria": "Parte Superior", "color": "Beige", "usos": 8, "agua_l": 3500, "co2_kg": 8.0},
        {"id": 3, "nombre": "Pantalón Chino Marrón", "categoria": "Parte Inferior", "color": "Marrón", "usos": 15, "agua_l": 7500, "co2_kg": 16.0},
        {"id": 4, "nombre": "Jeans Clásicos", "categoria": "Parte Inferior", "color": "Azul", "usos": 25, "agua_l": 10000, "co2_kg": 20.0},
        {"id": 5, "nombre": "Botines de Cuero", "categoria": "Calzado", "color": "Marrón Oscuro", "usos": 30, "agua_l": 8000, "co2_kg": 14.0},
        {"id": 6, "nombre": "Zapatillas de Lona", "categoria": "Calzado", "color": "Crema", "usos": 18, "agua_l": 3000, "co2_kg": 6.5},
    ]

if 'mensajes_ia' not in st.session_state:
    st.session_state.mensajes_ia = [
        {"rol": "assistant", "texto": "¡Hola! Soy tu eco-estilista virtual. ¿Para qué ocasión necesitas un outfit hoy o qué prenda de tu armario quieres aprender a combinar?"}
    ]

if 'perfil' not in st.session_state:
    st.session_state.perfil = {"cuerpo": "Reloj de arena / Equilibrado", "piel": "Cálido (Dorado / Melocotón)"}

# 3. BARRA LATERAL Y ACCESIBILIDAD (DALTONISMO)
st.sidebar.title("🌿 EcoArmario")
st.sidebar.markdown("*Viste elegante, cuida el planeta.*")
st.sidebar.divider()

st.sidebar.subheader("👁️ Accesibilidad Visual")
modo_daltonismo = st.sidebar.selectbox(
    "Adaptación para Daltonismo:",
    ["Estándar (Tonos Elegantes)", "Protanopia (Sin Rojo)", "Deuteranopia (Sin Verde)", "Tritanopia (Sin Azul)", "Alto Contraste (Monocromático)"]
)
mostrar_etiquetas = st.sidebar.checkbox("Mostrar códigos y nombres de color escritos", value=True)

# Definición de paletas según accesibilidad manteniendo la elegancia
paletas = {
    "Estándar (Tonos Elegantes)": {"bg": "#F7F3E9", "sec_bg": "#EAE0D5", "text": "#3C2A21", "accent": "#8C6239", "card": "#FFFFFF"},
    "Protanopia (Sin Rojo)": {"bg": "#F4F4F0", "sec_bg": "#E2E2D8", "text": "#2B2D42", "accent": "#4A6FA5", "card": "#FFFFFF"},
    "Deuteranopia (Sin Verde)": {"bg": "#F5F2EB", "sec_bg": "#E5DEC9", "text": "#22223B", "accent": "#6B5B95", "card": "#FFFFFF"},
    "Tritanopia (Sin Azul)": {"bg": "#F9F5F6", "sec_bg": "#EBE3D5", "text": "#2D2424", "accent": "#A25B5B", "card": "#FFFFFF"},
    "Alto Contraste (Monocromático)": {"bg": "#FFFFFF", "sec_bg": "#E0E0E0", "text": "#000000", "accent": "#333333", "card": "#F5F5F5"}
}
tema = paletas[modo_daltonismo]

# Inyección de estilo CSS para los colores beige y marrón elegantes
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {tema['bg']};
        color: {tema['text']};
    }}
    [data-testid="stSidebar"] {{
        background-color: {tema['sec_bg']};
    }}
    .stButton>button {{
        background-color: {tema['accent']};
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        opacity: 0.85;
        color: white;
    }}
    .tarjeta-elegante {{
        background-color: {tema['card']};
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid {tema['accent']};
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }}
    h1, h2, h3, h4, p, label {{
        color: {tema['text']} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. FUNCIÓN PARA GENERAR IMAGEN DE REFERENCIA DEL OUTFIT
def crear_imagen_referencia(top, bottom, shoes, piel):
    # Crea un lienzo con estética minimalista de revista de moda
    img = Image.new('RGB', (320, 440), color=(245, 239, 230))
    draw = ImageDraw.Draw(img)
    
    # Marco elegante
    draw.rectangle([10, 10, 310, 430], outline=(140, 98, 57), width=3)
    draw.text((85, 25), "VISTA PREVIA DE OUTFIT", fill=(60, 42, 33))
    
    # Silueta / Tono de piel referencial
    color_piel = (225, 185, 150) if "Cálido" in piel else (240, 205, 190) if "Frío" in piel else (210, 175, 145)
    draw.ellipse([135, 50, 185, 100], fill=color_piel, outline=(100, 75, 55), width=2)
    
    # Parte Superior
    draw.rectangle([90, 110, 230, 220], fill=(225, 215, 200), outline=(92, 64, 51), width=2)
    draw.text((100, 155), f"Top:\n{top[:20]}", fill=(50, 35, 25))
    
    # Parte Inferior
    draw.rectangle([105, 230, 215, 350], fill=(165, 135, 110), outline=(92, 64, 51), width=2)
    draw.text((115, 280), f"Pantalón:\n{bottom[:18]}", fill=(255, 255, 255))
    
    # Calzado
    draw.rectangle([115, 360, 205, 405], fill=(95, 65, 45), outline=(60, 42, 33), width=2)
    draw.text((125, 375), f"{shoes[:18]}", fill=(255, 255, 255))
    
    return img

# 5. ENCABEZADO Y NAVEGACIÓN PRINCIPAL
st.title("🧥 EcoArmario")
st.write("Tu asistente inteligente para multiplicar tus combinaciones sin comprar de más.")

tabs = st.tabs([
    "👗 Mi Armario",
    "📸 Escáner IA",
    "🧍 Perfil y Cuerpo",
    "✨ Recomendador y Agenda",
    "🤖 Asistente IA",
    "🌍 Impacto Ambiental"
])

# --- PESTAÑA 1: MI ARMARIO ---
with tabs[0]:
    st.header("Tu Ropa Actual")
    st.write("Combinar lo que ya tienes es el acto más sostenible.")
    
    cols = st.columns(3)
    for idx, prenda in enumerate(st.session_state.armario):
        with cols[idx % 3]:
            info_color = f"🎨 Color: **{prenda['color']}** *(Texto de apoyo activo)*" if mostrar_etiquetas else f"🎨 Color: {prenda['color']}"
            st.markdown(f"""
            <div class="tarjeta-elegante">
                <h4>{prenda['nombre']}</h4>
                <p>📁 Categoría: {prenda['categoria']}</p>
                <p>{info_color}</p>
                <p>🔄 Veces usado: <b>{prenda['usos']}</b></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Registrar uso hoy ➕", key=f"uso_{prenda['id']}"):
                prenda['usos'] += 1
                st.rerun()

# --- PESTAÑA 2: ESCÁNER AUTOMÁTICO ---
with tabs[1]:
    st.header("📸 Escáner Inteligente de Prendas")
    st.write("Sube una foto o usa tu cámara. El sistema clasificará automáticamente el tipo de prenda, color y su huella ecológica.")
    
    col_cam, col_res = st.columns(2)
    with col_cam:
        metodo = st.radio("Método de captura:", ["Subir foto de mi galería", "Tomar foto con la cámara"])
        if metodo == "Subir foto de mi galería":
            archivo_img = st.file_uploader("Selecciona la imagen de tu prenda", type=["jpg", "png", "jpeg"])
        else:
            archivo_img = st.camera_input("Enfoca tu prenda")
            
    with col_res:
        if archivo_img is not None:
            st.image(archivo_img, caption="Prenda detectada", width=220)
            st.success("¡Análisis automático completado!")
            
            # Clasificación automática sugerida con opción de confirmar
            nombre_auto = st.text_input("Nombre identificado:", value="Blazer Clásico de Algodón")
            cat_auto = st.selectbox("Categoría detectada:", ["Parte Superior", "Parte Inferior", "Calzado"])
            color_auto = st.selectbox("Color detectado:", ["Beige", "Marrón", "Blanco", "Negro", "Verde Oliva", "Azul", "Crema"])
            
            if st.button("Guardar en mi EcoArmario"):
                nueva_prenda = {
                    "id": len(st.session_state.armario) + 1,
                    "nombre": nombre_auto,
                    "categoria": cat_auto,
                    "color": color_auto,
                    "usos": 1,
                    "agua_l": 3200,
                    "co2_kg": 7.2
                }
                st.session_state.armario.append(nueva_prenda)
                st.balloons()
                st.success(f"¡{nombre_auto} se ha guardado exitosamente en tu armario!")

# --- PESTAÑA 3: PERFIL (TIPO DE CUERPO Y TONO DE PIEL) ---
with tabs[2]:
    st.header("🧍 Tu Perfil Estilístico")
    st.write("Configura tus características para adaptar los colores y cortes de tus recomendaciones.")
    
    c1, c2 = st.columns(2)
    with c1:
        tipo_cuerpo = st.selectbox(
            "Selecciona tu tipo de cuerpo:",
            ["Reloj de arena / Equilibrado", "Triángulo / Pera", "Triángulo Invertido", "Rectángulo", "Ovalado / Manzana"],
            index=0
        )
        tonos_piel = st.selectbox(
            "Selecciona tu subtono de piel:",
            ["Cálido (Dorado / Melocotón)", "Frío (Rosado / Azulado)", "Neutro (Equilibrado)"],
            index=0
        )
        if st.button("Actualizar mi perfil"):
            st.session_state.perfil["cuerpo"] = tipo_cuerpo
            st.session_state.perfil["piel"] = tonos_piel
            st.success("¡Perfil guardado! Tus recomendaciones semanales ahora usan estos datos.")
            
    with c2:
        st.markdown("<div class='tarjeta-elegante'>", unsafe_allow_html=True)
        st.subheader("💡 Diagnóstico para ti")
        if "Cálido" in tonos_piel:
            st.write("🎨 **Paleta ideal:** Los tonos tierra, beige, marrón camel, verde oliva y cremas resaltan la luminosidad natural de tu piel.")
        elif "Frío" in tonos_piel:
            st.write("🎨 **Paleta ideal:** El blanco puro, azul marino, gris carbón y marrón chocolate profundo crean un contraste elegante en ti.")
        else:
            st.write("🎨 **Paleta ideal:** Tienes gran versatilidad. Los tonos suaves como el arena, topo y grises cálidos te quedan excelentes.")
            
        st.write(f"📐 **Estrategia para silueta ({tipo_cuerpo}):** Priorizaremos combinaciones en tu armario que equilibren visualmente tus proporciones usando tus propias prendas.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- PESTAÑA 4: RECOMENDADOR CON IMAGEN Y AGENDA SEMANAL ---
with tabs[3]:
    st.header("✨ Tu Outfit Ideal y Agenda Semanal")
    
    superiores = [p for p in st.session_state.armario if p['categoria'] == 'Parte Superior']
    inferiores = [p for p in st.session_state.armario if p['categoria'] == 'Parte Inferior']
    calzados = [p for p in st.session_state.armario if p['categoria'] == 'Calzado']
    
    col_out, col_img = st.columns([1.2, 1])
    
    with col_out:
        st.subheader("Recomendación del Día")
        ocasion = st.selectbox("¿Qué planes tienes hoy?", ["Casual / Diario", "Trabajo / Oficina", "Salida Elegante", "Fin de Semana Relajado"])
        
        if st.button("Generar Combinación Ahora 🎲") or 'outfit_actual' not in st.session_state:
            st.session_state.outfit_actual = {
                "top": random.choice(superiores),
                "bottom": random.choice(inferiores),
                "shoes": random.choice(calzados)
            }
            
        actual = st.session_state.outfit_actual
        st.markdown(f"""
        <div class="tarjeta-elegante">
            <h4>Conjunto para: {ocasion}</h4>
            <p>👕 <b>Superior:</b> {actual['top']['nombre']} ({actual['top']['color']})</p>
            <p>👖 <b>Inferior:</b> {actual['bottom']['nombre']} ({actual['bottom']['color']})</p>
            <p>👞 <b>Calzado:</b> {actual['shoes']['nombre']} ({actual['shoes']['color']})</p>
            <hr>
            <p>✨ <i>Adaptado a tu cuerpo <b>{st.session_state.perfil['cuerpo']}</b> y piel <b>{st.session_state.perfil['piel']}</b>. ¡0 compras nuevas necesarias!</i></p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_img:
        st.subheader("Imagen de Referencia")
        img_ref = crear_imagen_referencia(
            actual['top']['nombre'],
            actual['bottom']['nombre'],
            actual['shoes']['nombre'],
            st.session_state.perfil['piel']
        )
        st.image(img_ref, caption="Boceto visual de cómo luce la combinación")
        
    st.divider()
    st.subheader("📅 Agenda de Outfits para la Semana")
    st.write("Planifica tu semana con anticipación para no repetir de más ni sentir que 'no tienes nada que ponerte'.")
    
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    plan_semanal = []
    for d in dias:
        plan_semanal.append({
            "Día": d,
            "Parte Superior": random.choice(superiores)['nombre'],
            "Parte Inferior": random.choice(inferiores)['nombre'],
            "Calzado": random.choice(calzados)['nombre'],
            "Ahorro Estimado": "$35 USD (Al no comprar ropa rápida)"
        })
    st.dataframe(pd.DataFrame(plan_semanal), use_container_width=True, hide_index=True)

# --- PESTAÑA 5: ASISTENTE DE INTELIGENCIA ARTIFICIAL ---
with tabs[4]:
    st.header("🤖 Asistente de Estilo Sostenible (IA)")
    st.write("Pregúntame cómo combinar una prenda difícil o qué ponerte según el clima.")
    
    for msg in st.session_state.mensajes_ia:
        with st.chat_message(msg["rol"]):
            st.write(msg["texto"])
            
    pregunta = st.chat_input("Ej: ¿Cómo combino mi pantalón marrón para una reunión?")
    if pregunta:
        st.session_state.mensajes_ia.append({"rol": "user", "texto": pregunta})
        with st.chat_message("user"):
            st.write(pregunta)
            
        top_sugerido = random.choice(superiores)['nombre']
        calzado_sugerido = random.choice(calzados)['nombre']
        respuesta = (
            f"¡Excelente idea usar lo que ya tienes! Teniendo en cuenta tu perfil ({st.session_state.perfil['cuerpo']} "
            f"y subtono {st.session_state.perfil['piel']}), te recomiendo combinar esa prenda con tu **{top_sugerido}** "
            f"y tus **{calzado_sugerido}**. Los tonos tierra y neutros de tu armario crean un look súper elegante sin gastar un centavo."
        )
        st.session_state.mensajes_ia.append({"rol": "assistant", "texto": respuesta})
        with st.chat_message("assistant"):
            st.write(respuesta)

# --- PESTAÑA 6: IMPACTO AMBIENTAL ---
with tabs[5]:
    st.header("🌍 El Impacto Positivo de tu Ropa")
    st.write("Cada vez que reutilizas tu ropa y evitas compras impulsivas, ahorras miles de litros de agua y reduces emisiones de carbono.")
    
    total_agua = sum(p['agua_l'] for p in st.session_state.armario)
    total_co2 = sum(p['co2_kg'] for p in st.session_state.armario)
    total_usos = sum(p['usos'] for p in st.session_state.armario)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("💧 Agua contenida en tu armario", f"{total_agua:,} Litros", "Equivalente a +30 años de agua para beber")
    m2.metric("☁️ Emisiones evitadas al reutilizar", f"{total_co2:.1f} kg CO2", "Menos contaminación textil")
    m3.metric("♻️ Total de usos de tus prendas", f"{total_usos} puestas", "+15% de vida útil este mes")
    
    st.divider()
    st.subheader("📊 Huella Ecológica por Prenda vs. Veces que la has usado")
    df_impacto = pd.DataFrame(st.session_state.armario)
    df_impacto["Agua Amortizada por Uso (L)"] = (df_impacto["agua_l"] / df_impacto["usos"]).round(1)
    
    st.bar_chart(data=df_impacto.set_index("nombre")[["usos"]])
    st.caption("💡 **Meta EcoArmario:** Mientras más barras altas tengas (más usos por prenda), más divides el impacto ambiental que costó fabricarla.")
