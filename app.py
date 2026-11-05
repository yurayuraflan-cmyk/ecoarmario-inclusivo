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

# 2. MAPA DE COLORES PARA DIBUJAR LAS PRENDAS EN EL AVATAR
PALETA_COLORES = {
    "blanco": (248, 248, 248),
    "beige": (225, 212, 188),
    "crema": (245, 238, 220),
    "marrón": (115, 75, 48),
    "marron": (115, 75, 48),
    "marrón oscuro": (75, 48, 32),
    "marron oscuro": (75, 48, 32),
    "negro": (40, 40, 40),
    "azul": (60, 95, 145),
    "azul marino": (35, 50, 85),
    "verde oliva": (105, 115, 75),
    "verde": (80, 115, 80),
    "gris": (155, 155, 155),
    "terracota": (180, 85, 60),
    "mostaza": (210, 155, 50)
}

def obtener_rgb(nombre_color, por_defecto=(140, 110, 90)):
    nombre_limpio = str(nombre_color).strip().lower()
    for clave, rgb in PALETA_COLORES.items():
        if clave in nombre_limpio:
            return rgb
    return por_defecto

# 3. ESTADO DE LA SESIÓN
if 'armario' not in st.session_state:
    st.session_state.armario = [
        {"id": 1, "nombre": "Camisa de Lino Blanca", "categoria": "Parte Superior", "color": "Blanco", "material": "Lino", "usos": 12, "agua_l": 2500, "co2_kg": 5.0},
        {"id": 2, "nombre": "Suéter Tejido Beige", "categoria": "Parte Superior", "color": "Beige", "material": "Lana/Algodón", "usos": 8, "agua_l": 3200, "co2_kg": 7.5},
        {"id": 3, "nombre": "Pantalón Chino Marrón", "categoria": "Parte Inferior", "color": "Marrón", "material": "Algodón", "usos": 15, "agua_l": 6000, "co2_kg": 12.0},
        {"id": 4, "nombre": "Jeans Clásicos Azules", "categoria": "Parte Inferior", "color": "Azul", "material": "Denim", "usos": 25, "agua_l": 8500, "co2_kg": 18.0},
        {"id": 5, "nombre": "Mocasines de Cuero", "categoria": "Calzado", "color": "Marrón Oscuro", "material": "Cuero", "usos": 30, "agua_l": 7000, "co2_kg": 14.0},
        {"id": 6, "nombre": "Zapatillas de Lona", "categoria": "Calzado", "color": "Crema", "material": "Lona", "usos": 18, "agua_l": 2800, "co2_kg": 6.0},
    ]

if 'mensajes_ia' not in st.session_state:
    st.session_state.mensajes_ia = [
        {"rol": "assistant", "texto": "¡Hola! Soy tu eco-estilista personal. ¿Qué prenda de tu armario quieres aprender a combinar hoy para no tener que comprar ropa nueva?"}
    ]

if 'perfil' not in st.session_state:
    st.session_state.perfil = {
        "cuerpo": "Reloj de arena / Equilibrado",
        "piel": "Cálido (Dorado / Melocotón)"
    }

# 4. BARRA LATERAL Y ACCESIBILIDAD PARA DALTONISMO
st.sidebar.title("🌿 EcoArmario")
st.sidebar.markdown("*Viste con estilo sin comprar de más.*")
st.sidebar.divider()

st.sidebar.subheader("👁️ Accesibilidad Visual")
modo_daltonismo = st.sidebar.selectbox(
    "Filtro para Daltonismo:",
    ["Estándar (Tonos Tierra)", "Protanopia (Sin Rojo)", "Deuteranopia (Sin Verde)", "Tritanopia (Sin Azul)", "Alto Contraste"]
)
mostrar_etiquetas = st.sidebar.checkbox("Mostrar etiquetas escritas de color", value=True)

paletas = {
    "Estándar (Tonos Tierra)": {"bg": "#F8F5EE", "sec_bg": "#EFE6D8", "text": "#3D2B1F", "accent": "#8A5A36", "card": "#FFFFFF"},
    "Protanopia (Sin Rojo)": {"bg": "#F4F4F1", "sec_bg": "#E1E4D7", "text": "#222C3C", "accent": "#416788", "card": "#FFFFFF"},
    "Deuteranopia (Sin Verde)": {"bg": "#F5F3EC", "sec_bg": "#E6DEC6", "text": "#242038", "accent": "#6C5B7B", "card": "#FFFFFF"},
    "Tritanopia (Sin Azul)": {"bg": "#FAF5F5", "sec_bg": "#EBDCDD", "text": "#322222", "accent": "#9E4747", "card": "#FFFFFF"},
    "Alto Contraste": {"bg": "#FFFFFF", "sec_bg": "#EDEDED", "text": "#000000", "accent": "#2B2B2B", "card": "#F7F7F7"}
}
tema = paletas[modo_daltonismo]

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
        padding: 8px 18px;
        font-weight: 600;
    }}
    .stButton>button:hover {{
        opacity: 0.9;
        color: white;
    }}
    .tarjeta-ropa {{
        background-color: {tema['card']};
        padding: 16px;
        border-radius: 12px;
        border-left: 5px solid {tema['accent']};
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }}
    h1, h2, h3, h4, p, label {{
        color: {tema['text']} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. DIBUJADO DE LA PERSONA ANIMADA (AVATAR DE MODA)
def crear_avatar_animado(prenda_top, prenda_bottom, prenda_shoes, tipo_piel, tipo_cuerpo):
    # Lienzo con fondo beige editorial
    ancho, alto = 380, 520
    img = Image.new('RGB', (ancho, alto), color=(248, 244, 237))
    draw = ImageDraw.Draw(img)
    linea = (55, 40, 30)

    # Marco exterior minimalista
    draw.rectangle([12, 12, ancho - 12, alto - 12], outline=linea, width=2)
    draw.text((115, 25), "TU OUTFIT ILUSTRADO", fill=linea)

    # Selector de tono de piel del avatar
    if "Cálido" in tipo_piel:
        color_piel = (238, 198, 160)
        sombra_piel = (215, 175, 138)
    elif "Frío" in tipo_piel:
        color_piel = (245, 212, 198)
        sombra_piel = (225, 188, 175)
    else:
        color_piel = (226, 190, 158)
        sombra_piel = (205, 168, 138)

    # Colores obtenidos de las prendas seleccionadas
    color_top = obtener_rgb(prenda_top['color'], (225, 212, 188))
    color_bottom = obtener_rgb(prenda_bottom['color'], (115, 75, 48))
    color_shoes = obtener_rgb(prenda_shoes['color'], (75, 48, 32))

    # Ajuste según silueta corporal
    ancho_hombro = 44 if "Invertido" in tipo_cuerpo else 36 if "Pera" in tipo_cuerpo else 40
    ancho_cadera = 46 if "Pera" in tipo_cuerpo else 36 if "Invertido" in tipo_cuerpo else 40

    # 1. Cabello (Parte posterior)
    draw.ellipse([140, 48, 240, 145], fill=(70, 45, 30))

    # 2. Cabeza, cuello y rostro animado
    draw.rectangle([182, 125, 198, 155], fill=sombra_piel)
    draw.ellipse([150, 55, 230, 135], fill=color_piel, outline=linea, width=2)
    
    # Cabello frontal con estilo
    draw.chord([148, 52, 232, 115], start=180, end=360, fill=(75, 48, 32))
    draw.polygon([(148, 85), (170, 100), (190, 80), (210, 100), (232, 85), (220, 55), (160, 55)], fill=(75, 48, 32))

    # Ojos y sonrisa amigable (estilo caricatura)
    draw.arc([168, 88, 180, 98], start=190, end=350, fill=linea, width=2)
    draw.arc([200, 88, 212, 98], start=190, end=350, fill=linea, width=2)
    draw.arc([182, 105, 198, 118], start=20, end=160, fill=linea, width=2)
    # Mejillas
    draw.ellipse([162, 98, 172, 106], fill=(235, 160, 150))
    draw.ellipse([208, 98, 218, 106], fill=(235, 160, 150))

    # 3. Brazos (debajo de la ropa)
    draw.line([(190 - ancho_hombro, 160), (125, 260)], fill=color_piel, width=12)
    draw.line([(190 + ancho_hombro, 160), (255, 260)], fill=color_piel, width=12)
    draw.ellipse([118, 255, 132, 269], fill=color_piel)  # Mano izq
    draw.ellipse([248, 255, 262, 269], fill=color_piel)  # Mano der

    # 4. Prenda Superior (Blusa, Suéter o Camisa animada)
    cuerpo_coords = [
        (190 - ancho_hombro, 155),
        (190 + ancho_hombro, 155),
        (190 + ancho_cadera - 4, 265),
        (190 - ancho_cadera + 4, 265)
    ]
    draw.polygon(cuerpo_coords, fill=color_top, outline=linea)
    # Mangas
    draw.polygon([(190 - ancho_hombro, 155), (128, 215), (142, 222), (180, 185)], fill=color_top, outline=linea)
    draw.polygon([(190 + ancho_hombro, 155), (252, 215), (238, 222), (200, 185)], fill=color_top, outline=linea)
    # Cuello de la prenda
    draw.arc([175, 150, 205, 172], start=0, end=180, fill=linea, width=2)

    # 5. Prenda Inferior (Pantalón estilizado)
    pantalon_izq = [
        (190 - ancho_cadera + 4, 265),
        (190, 265),
        (192, 320),
        (182, 435),
        (150, 435),
        (156, 310)
    ]
    pantalon_der = [
        (190, 265),
        (190 + ancho_cadera - 4, 265),
        (224, 310),
        (230, 435),
        (198, 435),
        (188, 320)
    ]
    draw.polygon(pantalon_izq, fill=color_bottom, outline=linea)
    draw.polygon(pantalon_der, fill=color_bottom, outline=linea)
    draw.line([(190, 265), (190, 320)], fill=linea, width=2)

    # 6. Calzado animado
    draw.ellipse([142, 430, 184, 455], fill=color_shoes, outline=linea, width=2)
    draw.ellipse([196, 430, 238, 455], fill=color_shoes, outline=linea, width=2)

    # Tarjeta de resumen al pie de la imagen
    draw.rectangle([25, 465, ancho - 25, 505], fill=(255, 255, 255), outline=linea, width=1)
    etiqueta = f"Top: {prenda_top['color']} | Pant: {prenda_bottom['color']}"
    draw.text((38, 478), etiqueta[:42], fill=linea)

    return img

# 6. ENCABEZADO Y TABS DE LA APLICACIÓN
st.title("🧥 EcoArmario")
st.write("Aprende a combinar lo que ya tienes, reduce compras innecesarias y viste de forma consciente.")

tabs = st.tabs([
    "👗 Mi Armario",
    "➕ Agregar Prenda",
    "📸 Escáner IA",
    "🧍 Mi Perfil y Silueta",
    "✨ Recomendador y Agenda",
    "🤖 Asistente IA",
    "🌍 Impacto Ambiental"
])

# --- TAB 1: MI ARMARIO ---
with tabs[0]:
    st.header("Tus Prendas Registradas")
    st.write("Tu mejor guardarropa es el que ya tienes.")
    
    filtro_cat = st.radio("Filtrar por categoría:", ["Todas", "Parte Superior", "Parte Inferior", "Calzado"], horizontal=True)
    prendas_mostradas = st.session_state.armario if filtro_cat == "Todas" else [p for p in st.session_state.armario if p['categoria'] == filtro_cat]
    
    cols = st.columns(3)
    for idx, prenda in enumerate(prendas_mostradas):
        with cols[idx % 3]:
            etiqueta_color = f"🎨 Color: **{prenda['color']}**" if mostrar_etiquetas else f"🎨 {prenda['color']}"
            st.markdown(f"""
            <div class="tarjeta-ropa">
                <h4>{prenda['nombre']}</h4>
                <p>📁 <b>Tipo:</b> {prenda['categoria']}</p>
                <p>{etiqueta_color}</p>
                <p>🧵 <b>Material:</b> {prenda.get('material', 'Textil mixto')}</p>
                <p>🔄 <b>Puestas:</b> {prenda['usos']} veces</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Me la puse hoy ➕", key=f"btn_uso_{prenda['id']}"):
                prenda['usos'] += 1
                st.rerun()

# --- TAB 2: AGREGAR PRENDA MANUALMENTE ---
with tabs[1]:
    st.header("➕ Añadir Nueva Prenda a tu Armario")
    st.write("Registra la ropa que tienes en tu clóset para que el recomendador pueda armar combinaciones automáticas.")

    with st.form("formulario_agregar_prenda", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            nuevo_nombre = st.text_input("Nombre de la prenda:", placeholder="Ej: Chompa de lana cuello alto")
            nueva_cat = st.selectbox("Categoría:", ["Parte Superior", "Parte Inferior", "Calzado"])
            nuevo_color = st.selectbox(
                "Color principal:",
                ["Beige", "Marrón", "Marrón Oscuro", "Blanco", "Negro", "Azul", "Azul Marino", "Crema", "Verde Oliva", "Gris", "Terracota", "Mostaza"]
            )
            
        with col_f2:
            nuevo_material = st.selectbox(
                "Tipo de material o tela:",
                ["Algodón", "Lino", "Lana", "Denim / Mezclilla", "Poliéster / Sintético", "Cuero / Semicuero", "Lona"]
            )
            usos_previos = st.number_input("¿Cuántas veces aproximadamente la has usado ya?", min_value=1, value=5, step=1)
            notas = st.text_input("Detalles o estilo:", placeholder="Ej: Corte recto, para días fríos")

        btn_guardar = st.form_submit_button("Guardar Prenda en EcoArmario 🌿")

        if btn_guardar:
            if nuevo_nombre.strip() == "":
                st.error("Por favor, escribe un nombre para tu prenda.")
            else:
                # Estimación de huella ecológica según tipo de prenda y material
                huellas = {
                    "Parte Superior": {"agua": 2700, "co2": 5.5},
                    "Parte Inferior": {"agua": 7500, "co2": 15.0},
                    "Calzado": {"agua": 6000, "co2": 12.0}
                }
                datos_eco = huellas.get(nueva_cat, {"agua": 3500, "co2": 8.0})
                
                nueva_prenda = {
                    "id": len(st.session_state.armario) + 1,
                    "nombre": nuevo_nombre,
                    "categoria": nueva_cat,
                    "color": nuevo_color,
                    "material": nuevo_material,
                    "usos": int(usos_previos),
                    "agua_l": datos_eco["agua"],
                    "co2_kg": datos_eco["co2"]
                }
                
                st.session_state.armario.append(nueva_prenda)
                st.success(f"¡'{nuevo_nombre}' se añadió con éxito! Ya puedes verla en las recomendaciones.")

# --- TAB 3: ESCÁNER INTELIGENTE ---
with tabs[2]:
    st.header("📸 Escáner de Ropa")
    st.write("Sube una foto o tómala al momento para catalogar tu prenda de forma rápida.")
    
    col_cam, col_prev = st.columns(2)
    with col_cam:
        modo_foto = st.radio("¿Cómo quieres cargar la foto?", ["Subir archivo", "Usar cámara web"])
        foto = st.file_uploader("Selecciona imagen", type=["jpg", "png", "jpeg"]) if modo_foto == "Subir archivo" else st.camera_input("Capturar foto")

    with col_prev:
        if foto is not None:
            st.image(foto, caption="Prenda capturada", width=240)
            st.success("¡Foto analizada!")
            
            auto_nom = st.text_input("Nombre detectado:", value="Casaca Ligera Tierra")
            auto_cat = st.selectbox("Categoría detectada:", ["Parte Superior", "Parte Inferior", "Calzado"])
            auto_col = st.selectbox("Color identificado:", ["Beige", "Marrón", "Verde Oliva", "Blanco", "Negro", "Azul"])
            
            if st.button("Confirmar y Guardar en mi Armario"):
                st.session_state.armario.append({
                    "id": len(st.session_state.armario) + 1,
                    "nombre": auto_nom,
                    "categoria": auto_cat,
                    "color": auto_col,
                    "material": "Algodón mixto",
                    "usos": 1,
                    "agua_l": 3100,
                    "co2_kg": 6.8
                })
                st.success(f"¡Guardado! {auto_nom} ya está disponible.")

# --- TAB 4: PERFIL Y CUERPO ---
with tabs[3]:
    st.header("🧍 Tu Silueta y Tono de Piel")
    st.write("Personaliza estos aspectos para que las recomendaciones resalten tus rasgos naturales.")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        tipo_cuerpo = st.selectbox(
            "Tu tipo de cuerpo:",
            ["Reloj de arena / Equilibrado", "Pera / Triángulo", "Triángulo Invertido", "Rectángulo", "Ovalado"],
            index=0
        )
        subtono_piel = st.selectbox(
            "Tu subtono de piel:",
            ["Cálido (Dorado / Melocotón)", "Frío (Rosado / Azulado)", "Neutro (Equilibrado)"],
            index=0
        )
        if st.button("Guardar Cambios de Perfil"):
            st.session_state.perfil["cuerpo"] = tipo_cuerpo
            st.session_state.perfil["piel"] = subtono_piel
            st.success("¡Perfil actualizado!")
            
    with col_p2:
        st.markdown("<div class='tarjeta-ropa'>", unsafe_allow_html=True)
        st.subheader("💡 Consejo Personalizado")
        if "Cálido" in subtono_piel:
            st.write("✨ **Tus mejores tonos:** Los marrones cálidos, beige arena, mostaza suave y verde oliva resaltan tu luminosidad.")
        elif "Frío" in subtono_piel:
            st.write("✨ **Tus mejores tonos:** El blanco puro, azul marino, gris ceniza y marrón chocolate oscuro te aportan un contraste sofisticado.")
        else:
            st.write("✨ **Tus mejores tonos:** Los colores neutros intermedios, topo, crema y maderas suaves armonizan perfectamente contigo.")
            
        st.write(f"📐 **Corte ({tipo_cuerpo}):** Tus sugerencias buscarán equilibrar hombros y cadera aprovechando las prendas que ya tienes.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 5: RECOMENDADOR CON AVATAR ANIMADO Y AGENDA ---
with tabs[4]:
    st.header("✨ Outfit del Día y Planificación Semanal")
    
    tops = [p for p in st.session_state.armario if p['categoria'] == 'Parte Superior']
    bottoms = [p for p in st.session_state.armario if p['categoria'] == 'Parte Inferior']
    shoes = [p for p in st.session_state.armario if p['categoria'] == 'Calzado']
    
    if not tops or not bottoms or not shoes:
        st.warning("Asegúrate de tener al menos una prenda superior, una inferior y calzado registrado para generar outfits.")
    else:
        col_rec, col_avatar = st.columns([1.1, 1])
        
        with col_rec:
            st.subheader("Sugerencia Personalizada")
            ocasion = st.selectbox("Ocasión de hoy:", ["Día a Día / Casual", "Estudio / Trabajo", "Reunión Elegante", "Salida de Fin de Semana"])
            
            if st.button("Generar otra combinación 🎲") or 'outfit_elegido' not in st.session_state:
                st.session_state.outfit_elegido = {
                    "top": random.choice(tops),
                    "bottom": random.choice(bottoms),
                    "shoes": random.choice(shoes)
                }
                
            actual = st.session_state.outfit_elegido
            
            st.markdown(f"""
            <div class="tarjeta-ropa">
                <h4>Conjunto para: {ocasion}</h4>
                <p>👕 <b>Parte Superior:</b> {actual['top']['nombre']} (<i>{actual['top']['color']}</i>)</p>
                <p>👖 <b>Parte Inferior:</b> {actual['bottom']['nombre']} (<i>{actual['bottom']['color']}</i>)</p>
                <p>👞 <b>Calzado:</b> {actual['shoes']['nombre']} (<i>{actual['shoes']['color']}</i>)</p>
                <hr>
                <p>🌱 <i>Prendas de tu propio clóset. Gasto en ropa nueva: <b>$0.00</b></i></p>
            </div>
            """, unsafe_allow_html=True)

        with col_avatar:
            st.subheader("Visualización Animada")
            # Creación del avatar animado que viste las prendas
            img_avatar = crear_avatar_animado(
                actual['top'],
                actual['bottom'],
                actual['shoes'],
                st.session_state.perfil['piel'],
                st.session_state.perfil['cuerpo']
            )
            st.image(img_avatar, caption="Representación ilustrada de tu combinación")

        st.divider()
        st.subheader("📅 Tu Agenda de Estilo para la Semana")
        st.write("Evita el estrés matutino y repite con creatividad sin comprar prendas adicionales.")
        
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        datos_semana = []
        for dia in dias_semana:
            datos_semana.append({
                "Día": dia,
                "Top": random.choice(tops)['nombre'],
                "Parte Inferior": random.choice(bottoms)['nombre'],
                "Calzado": random.choice(shoes)['nombre'],
                "Gasto Evitado": "Ahorro total"
            })
        st.dataframe(pd.DataFrame(datos_semana), use_container_width=True, hide_index=True)

# --- TAB 6: ASISTENTE IA ---
with tabs[5]:
    st.header("🤖 Asistente de Moda Circular")
    st.write("Escribe qué prenda tienes en mente o a dónde vas, y la IA te dirá cómo combinarla con tu ropa actual.")
    
    for msg in st.session_state.mensajes_ia:
        with st.chat_message(msg["rol"]):
            st.write(msg["texto"])
            
    pregunta_usuario = st.chat_input("Ej: ¿Cómo uso mi suéter beige para una presentación?")
    if pregunta_usuario:
        st.session_state.mensajes_ia.append({"rol": "user", "texto": pregunta_usuario})
        with st.chat_message("user"):
            st.write(pregunta_usuario)
            
        sup_ejemplo = random.choice(tops)['nombre'] if tops else "tu camisa favorita"
        bot_ejemplo = random.choice(bottoms)['nombre'] if bottoms else "tus pantalones cómodos"
        
        respuesta_estilista = (
            f"Para esa ocasión y aprovechando tu silueta ({st.session_state.perfil['cuerpo']}), "
            f"puedes combinarlo con tu **{bot_ejemplo}** y completar el look con **{sup_ejemplo}**. "
            f"Al mantenerte en la armonía de tus tonos tierra y neutros, logras presencia y elegancia sin consumir nada extra."
        )
        
        st.session_state.mensajes_ia.append({"rol": "assistant", "texto": respuesta_estilista})
        with st.chat_message("assistant"):
            st.write(respuesta_estilista)

# --- TAB 7: IMPACTO AMBIENTAL ---
with tabs[6]:
    st.header("🌍 Tu Ahorro Ecológico Acumulado")
    st.write("El impacto de la ropa ya fue generado al fabricarse; tu misión en EcoArmario es amortizarlo usándola muchas veces.")
    
    total_l_agua = sum(p['agua_l'] for p in st.session_state.armario)
    total_co2 = sum(p['co2_kg'] for p in st.session_state.armario)
    total_usos = sum(p['usos'] for p in st.session_state.armario)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("💧 Litros de agua amortizados", f"{total_l_agua:,} L", "Evitando comprar ropa rápida")
    m2.metric("☁️ CO2 mitigado", f"{total_co2:.1f} kg", "Por reutilización constante")
    m3.metric("🔄 Puestas totales de tu armario", f"{total_usos} usos", "Vida útil extendida")
    
    st.divider()
    st.subheader("📊 Veces que has vestido cada prenda")
    df_prendas = pd.DataFrame(st.session_state.armario)
    st.bar_chart(df_prendas.set_index("nombre")["usos"])
    st.caption("Cada barra refleja cuántas veces le diste vida a esa prenda sin dejarla olvidada en el armario.")
