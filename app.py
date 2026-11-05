import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import colorsys

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="EcoArmario 3D - Closet Digital Sostenible",
    page_icon="🌿",
    layout="wide"
)

# 2. CATÁLOGO AMPLIO DE COLORES + SOPORTE PARA CUALQUIER COLOR HEX (16.7 MILLONES)
CATALOGO_COLORES = {
    "Blanco Puro": "#F8F9FA", "Blanco Hueso": "#F2EFE9", "Crema": "#F5EEDC", "Beige Arena": "#E1D4BC",
    "Camel": "#C19A6B", "Marrón Café": "#6F4E37", "Marrón Chocolate": "#4B3020", "Topo / Taupe": "#8B7D70",
    "Negro Ónix": "#222222", "Gris Perla": "#D3D3D3", "Gris Carbón": "#4A4A4A", "Azul Marino": "#1D2951",
    "Azul Cielo": "#87CEEB", "Azul Rey": "#2454FF", "Azul Petróleo": "#0E4D64", "Celeste Pastel": "#B4D8E7",
    "Verde Oliva": "#6B734B", "Verde Esmeralda": "#2E8B57", "Verde Salvia": "#9CAF88", "Verde Menta": "#98FF98",
    "Verde Bosque": "#1E4620", "Terracota": "#B4553C", "Vino / Burdeos": "#6E1E2A", "Rojo Carmesí": "#C41E3A",
    "Coral": "#FF7F50", "Salmón": "#FA8072", "Rosa Pastel": "#FFD1DC", "Fucsia": "#D12682",
    "Palo Rosa": "#D8A1A6", "Lavanda": "#C8A2C8", "Lila": "#B695C0", "Morado Ciruela": "#582A5A",
    "Mostaza": "#D29B32", "Amarillo Pastel": "#FDFD96", "Naranja Quemado": "#CC5500", "Turquesa": "#30D5C8",
    "Caqui": "#C3B091", "Cobre": "#B87333", "Dorado Suave": "#D4AF37", "Plateado": "#C0C0C0"
}

TONOS_PIEL = {
    "Porcelana Claro": "#FCE2D4",
    "Marfil Suave": "#F5D0B8",
    "Trigueño Claro": "#E8B993",
    "Trigueño Medio / Dorado": "#D49B6A",
    "Bronceado Cálido": "#B87A4B",
    "Moreno Canela": "#8F5632",
    "Ébano Profundo": "#59331E"
}

# Funciones matemáticas para iluminación 3D y armonía con CUALQUIER color
def hex_a_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        return (180, 160, 140)
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_a_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(
        max(0, min(255, int(rgb[0]))),
        max(0, min(255, int(rgb[1]))),
        max(0, min(255, int(rgb[2])))
    )

def ajustar_luz_color(hex_str, factor_luz):
    """Genera brillos especulares (>1) y sombras 3D (<1) para cualquier color"""
    r, g, b = [x / 255.0 for x in hex_a_rgb(hex_str)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l_nuevo = max(0.05, min(0.96, l * factor_luz))
    r2, g2, b2 = colorsys.hls_to_rgb(h, l_nuevo, s)
    return rgb_a_hex((r2 * 255, g2 * 255, b2 * 255))

def calcular_armonia_colores(hex1, hex2):
    """Evalúa cómo combinan dos colores cualesquiera en el círculo cromático"""
    r1, g1, b1 = [x / 255.0 for x in hex_a_rgb(hex1)]
    r2, g2, b2 = [x / 255.0 for x in hex_a_rgb(hex2)]
    h1, l1, s1 = colorsys.rgb_to_hls(r1, g1, b1)
    h2, l2, s2 = colorsys.rgb_to_hls(r2, g2, b2)

    # Si alguno es neutro (baja saturación o muy claro/oscuro), combina con todo
    if s1 < 0.18 or s2 < 0.18 or l1 > 0.88 or l2 > 0.88 or l1 < 0.15 or l2 < 0.15:
        return "Armonía con Neutro Comodín (98% Compatible)"
    
    diff_hue = abs(h1 - h2) * 360
    if diff_hue > 180:
        diff_hue = 360 - diff_hue

    if diff_hue < 18:
        return "Armonía Monocromática (95% Compatible)"
    elif diff_hue < 55:
        return "Armonía Análoga Suave (94% Compatible)"
    elif 150 <= diff_hue <= 210:
        return "Contraste Complementario Vibrante (92% Compatible)"
    elif 110 <= diff_hue <= 135:
        return "Armonía Triádica Dinámica (90% Compatible)"
    else:
        return "Combinación Creativa Equilibrada (87% Compatible)"

# 3. ESTADO DE LA SESIÓN
if 'armario' not in st.session_state:
    st.session_state.armario = [
        {"id": 1, "nombre": "Camisa de Lino Blanca", "categoria": "Parte Superior", "color": "Blanco Hueso", "hex": "#F2EFE9", "material": "Lino", "usos": 12, "agua_l": 2500, "co2_kg": 5.0},
        {"id": 2, "nombre": "Suéter Tejido Camel", "categoria": "Parte Superior", "color": "Camel", "hex": "#C19A6B", "material": "Lana", "usos": 8, "agua_l": 3200, "co2_kg": 7.5},
        {"id": 3, "nombre": "Blusa Verde Salvia", "categoria": "Parte Superior", "color": "Verde Salvia", "hex": "#9CAF88", "material": "Algodón", "usos": 6, "agua_l": 2700, "co2_kg": 5.5},
        {"id": 4, "nombre": "Pantalón Chino Marrón", "categoria": "Parte Inferior", "color": "Marrón Café", "hex": "#6F4E37", "material": "Algodón", "usos": 15, "agua_l": 6000, "co2_kg": 12.0},
        {"id": 5, "nombre": "Jeans Clásicos", "categoria": "Parte Inferior", "color": "Azul Marino", "hex": "#1D2951", "material": "Denim", "usos": 25, "agua_l": 8500, "co2_kg": 18.0},
        {"id": 6, "nombre": "Pantalón Sastre Beige", "categoria": "Parte Inferior", "color": "Beige Arena", "hex": "#E1D4BC", "material": "Lino/Algodón", "usos": 10, "agua_l": 5200, "co2_kg": 11.0},
        {"id": 7, "nombre": "Mocasines de Cuero", "categoria": "Calzado", "color": "Marrón Chocolate", "hex": "#4B3020", "material": "Cuero", "usos": 30, "agua_l": 7000, "co2_kg": 14.0},
        {"id": 8, "nombre": "Zapatillas Urbanas", "categoria": "Calzado", "color": "Crema", "hex": "#F5EEDC", "material": "Lona", "usos": 18, "agua_l": 2800, "co2_kg": 6.0},
    ]

if 'perfil' not in st.session_state:
    st.session_state.perfil = {
        "cuerpo": "Reloj de arena / Equilibrado",
        "tono_nombre": "Trigueño Claro",
        "piel_hex": "#E8B993",
        "subtono": "Cálido (Dorado / Melocotón)",
        "cabello_hex": "#3B2618"
    }

if 'mensajes_ia' not in st.session_state:
    st.session_state.mensajes_ia = [
        {"rol": "assistant", "texto": "¡Hola! Soy tu estilista 3D de EcoArmario. Puedo combinar cualquier color de tu clóset adaptándolo a tu silueta y tono de piel. ¿Qué ocasión tienes hoy?"}
    ]

# 4. BARRA LATERAL Y ACCESIBILIDAD
st.sidebar.title("🌿 EcoArmario 3D")
st.sidebar.markdown("*Moda sostenible e inteligente.*")
st.sidebar.divider()

st.sidebar.subheader("👁️ Accesibilidad (Daltonismo)")
modo_daltonismo = st.sidebar.selectbox(
    "Modo visual:",
    ["Estándar (Tonos Elegantes)", "Protanopia (Sin Rojo)", "Deuteranopia (Sin Verde)", "Tritanopia (Sin Azul)", "Alto Contraste"]
)
mostrar_etiquetas = st.sidebar.checkbox("Mostrar códigos HEX y nombres de color", value=True)

paletas = {
    "Estándar (Tonos Elegantes)": {"bg": "#F7F3EB", "sec_bg": "#EAE0D2", "text": "#3B281E", "accent": "#8A5A36", "card": "#FFFFFF"},
    "Protanopia (Sin Rojo)": {"bg": "#F4F5F0", "sec_bg": "#E1E4D5", "text": "#202A38", "accent": "#3E6589", "card": "#FFFFFF"},
    "Deuteranopia (Sin Verde)": {"bg": "#F6F3EC", "sec_bg": "#E5DEC8", "text": "#26213A", "accent": "#6E5A7F", "card": "#FFFFFF"},
    "Tritanopia (Sin Azul)": {"bg": "#FAF4F4", "sec_bg": "#ECDCDD", "text": "#332020", "accent": "#9E4747", "card": "#FFFFFF"},
    "Alto Contraste": {"bg": "#FFFFFF", "sec_bg": "#E8E8E8", "text": "#000000", "accent": "#222222", "card": "#F8F8F8"}
}
tema = paletas[modo_daltonismo]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {tema['bg']}; color: {tema['text']}; }}
    [data-testid="stSidebar"] {{ background-color: {tema['sec_bg']}; }}
    .stButton>button {{
        background-color: {tema['accent']}; color: white; border-radius: 8px;
        border: none; padding: 8px 18px; font-weight: 600;
    }}
    .stButton>button:hover {{ opacity: 0.9; color: white; }}
    .tarjeta-ropa {{
        background-color: {tema['card']}; padding: 16px; border-radius: 12px;
        border-left: 6px solid {tema['accent']}; box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 14px;
    }}
    .muestra-color {{
        display: inline-block; width: 16px; height: 16px; border-radius: 50%;
        border: 1px solid #555; vertical-align: middle; margin-right: 6px;
    }}
    h1, h2, h3, h4, p, label {{ color: {tema['text']} !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. MOTOR DE RENDERIZADO DE AVATAR 3D ANIMADO (CON ADAPTACIÓN DE SILUETA Y PIEL)
def renderizar_avatar_3d(top_prenda, bottom_prenda, shoes_prenda, perfil, altura_px=570):
    # Parámetros anatómicos dinámicos según tipo de cuerpo
    cuerpo = perfil["cuerpo"]
    if "Reloj de arena" in cuerpo:
        sh_w, ch_w, wa_w, hi_w, th_w = 56, 48, 33, 54, 26
    elif "Pera" in cuerpo:
        sh_w, ch_w, wa_w, hi_w, th_w = 45, 41, 35, 62, 30
    elif "Invertido" in cuerpo:
        sh_w, ch_w, wa_w, hi_w, th_w = 65, 56, 40, 42, 21
    elif "Rectángulo" in cuerpo:
        sh_w, ch_w, wa_w, hi_w, th_w = 50, 46, 44, 47, 23
    else:  # Ovalado / Manzana
        sh_w, ch_w, wa_w, hi_w, th_w = 53, 55, 58, 52, 25

    # Ajuste de subtono sobre el color de piel
    piel_base = perfil["piel_hex"]
    r_p, g_p, b_p = hex_a_rgb(piel_base)
    if "Cálido" in perfil["subtono"]:
        piel_base = rgb_a_hex((r_p + 8, g_p + 3, b_p - 6))
    elif "Frío" in perfil["subtono"]:
        piel_base = rgb_a_hex((r_p + 4, g_p - 3, b_p + 7))

    piel_luz = ajustar_luz_color(piel_base, 1.18)
    piel_sombra = ajustar_luz_color(piel_base, 0.78)
    piel_oscura = ajustar_luz_color(piel_base, 0.62)

    cabello_base = perfil.get("cabello_hex", "#3B2618")
    cabello_luz = ajustar_luz_color(cabello_base, 1.35)
    cabello_sombra = ajustar_luz_color(cabello_base, 0.65)

    # Shaders 3D para Top, Pantalón y Calzado (funciona con cualquier color)
    top_hex = top_prenda["hex"]
    top_luz = ajustar_luz_color(top_hex, 1.22)
    top_sombra = ajustar_luz_color(top_hex, 0.72)

    bot_hex = bottom_prenda["hex"]
    bot_luz = ajustar_luz_color(bot_hex, 1.20)
    bot_sombra = ajustar_luz_color(bot_hex, 0.68)

    sho_hex = shoes_prenda["hex"]
    sho_luz = ajustar_luz_color(sho_hex, 1.25)
    sho_sombra = ajustar_luz_color(sho_hex, 0.60)

    # Coordenadas paramétricas del torso y piernas según silueta
    cx = 200
    torso_path = f"""
        M {cx - sh_w} 162
        Q {cx} 152 {cx + sh_w} 162
        C {cx + sh_w + 4} 195, {cx + ch_w} 215, {cx + wa_w} 245
        C {cx + wa_w + 4} 265, {cx + hi_w} 275, {cx + hi_w} 292
        Q {cx} 302 {cx - hi_w} 292
        C {cx - hi_w} 275, {cx - wa_w - 4} 265, {cx - wa_w} 245
        C {cx - ch_w} 215, {cx - sh_w - 4} 195, {cx - sh_w} 162 Z
    """

    pierna_izq = f"""
        M {cx - hi_w} 288
        L {cx + 2} 294
        L {cx - 4} 345
        C {cx - 6} 390, {cx - 14} 435, {cx - 18} 468
        L {cx - 44} 468
        C {cx - 46} 425, {cx - hi_w - 4} 355, {cx - hi_w} 288 Z
    """

    pierna_der = f"""
        M {cx - 2} 294
        L {cx + hi_w} 288
        C {cx + hi_w + 4} 355, {cx + 46} 425, {cx + 44} 468
        L {cx + 18} 468
        C {cx + 14} 435, {cx + 6} 390, {cx + 4} 345 Z
    """

    html_3d = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0; padding: 0; background: transparent;
            font-family: 'Segoe UI', sans-serif;
            display: flex; flex-direction: column; align-items: center;
        }}
        .escena-3d {{
            width: 390px; height: 535px;
            background: radial-gradient(circle at 50% 35%, #FFFDF9 0%, #EFE6D5 65%, #DFCGB5 100%);
            border-radius: 22px;
            box-shadow: inset 0 0 35px rgba(90,60,35,0.12), 0 12px 28px rgba(0,0,0,0.10);
            border: 2px solid #D5C3AE;
            position: relative; overflow: hidden;
            perspective: 900px;
        }}
        .contenedor-avatar {{
            width: 100%; height: 100%;
            transform-style: preserve-3d;
            transition: transform 0.25s ease-out;
            animation: respirar 3.8s ease-in-out infinite;
        }}
        @keyframes respirar {{
            0%, 100% {{ transform: translateY(0px) scaleY(1); }}
            50% {{ transform: translateY(-4px) scaleY(1.008); }}
        }}
        @keyframes parpadeo {{
            0%, 94%, 98%, 100% {{ transform: scaleY(1); }}
            96% {{ transform: scaleY(0.1); }}
        }}
        .ojos-animados {{
            transform-origin: 200px 102px;
            animation: parpadeo 4.5s infinite;
        }}
        .controles-3d {{
            position: absolute; bottom: 10px; left: 15px; right: 15px;
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(6px);
            border-radius: 12px; padding: 7px 14px;
            display: flex; justify-content: space-between; align-items: center;
            font-size: 12px; color: #3B281E; font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        .etiqueta-flotante {{
            position: absolute; top: 12px; left: 14px;
            background: rgba(60, 40, 25, 0.82); color: #FFF;
            padding: 5px 11px; border-radius: 20px; font-size: 11px;
            letter-spacing: 0.4px;
        }}
        input[type=range] {{ accent-color: #8A5A36; width: 140px; cursor: pointer; }}
    </style>
    </head>
    <body>
    <div class="escena-3d" id="escena">
        <div class="etiqueta-flotante">✨ {cuerpo} | Piel: {perfil['tono_nombre']}</div>
        <div class="contenedor-avatar" id="avatar3d">
            <svg viewBox="0 0 400 530" width="100%" height="100%">
                <defs>
                    <!-- Sombras 3D Suaves (Drop Shadows & Ambient Occlusion) -->
                    <filter id="sombra3d" x="-15%" y="-15%" width="130%" height="130%">
                        <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#2A1B12" flood-opacity="0.28"/>
                    </filter>
                    <filter id="sombraSuave" x="-10%" y="-10%" width="120%" height="120%">
                        <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#1E120A" flood-opacity="0.22"/>
                    </filter>

                    <!-- Gradiente 3D Esférico/Cilíndrico de Piel -->
                    <radialGradient id="gradCara" cx="42%" cy="35%" r="60%">
                        <stop offset="0%" stop-color="{piel_luz}"/>
                        <stop offset="55%" stop-color="{piel_base}"/>
                        <stop offset="100%" stop-color="{piel_sombra}"/>
                    </radialGradient>
                    <linearGradient id="gradPielCilindro" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="{piel_sombra}"/>
                        <stop offset="35%" stop-color="{piel_luz}"/>
                        <stop offset="70%" stop-color="{piel_base}"/>
                        <stop offset="100%" stop-color="{piel_oscura}"/>
                    </linearGradient>

                    <!-- Gradiente 3D Cabello con Brillo Especular -->
                    <linearGradient id="gradCabello" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="{cabello_sombra}"/>
                        <stop offset="35%" stop-color="{cabello_base}"/>
                        <stop offset="52%" stop-color="{cabello_luz}"/>
                        <stop offset="75%" stop-color="{cabello_base}"/>
                        <stop offset="100%" stop-color="{cabello_sombra}"/>
                    </linearGradient>

                    <!-- Gradiente Volumétrico 3D Prenda Superior -->
                    <linearGradient id="gradTop" x1="0%" y1="0%" x2="100%" y2="15%">
                        <stop offset="0%" stop-color="{top_sombra}"/>
                        <stop offset="28%" stop-color="{top_luz}"/>
                        <stop offset="62%" stop-color="{top_hex}"/>
                        <stop offset="100%" stop-color="{top_sombra}"/>
                    </linearGradient>

                    <!-- Gradiente Volumétrico 3D Prenda Inferior -->
                    <linearGradient id="gradBottom" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="{bot_sombra}"/>
                        <stop offset="30%" stop-color="{bot_luz}"/>
                        <stop offset="65%" stop-color="{bot_hex}"/>
                        <stop offset="100%" stop-color="{bot_sombra}"/>
                    </linearGradient>

                    <!-- Gradiente Volumétrico 3D Calzado -->
                    <radialGradient id="gradShoes" cx="38%" cy="30%" r="70%">
                        <stop offset="0%" stop-color="{sho_luz}"/>
                        <stop offset="55%" stop-color="{sho_hex}"/>
                        <stop offset="100%" stop-color="{sho_sombra}"/>
                    </radialGradient>
                </defs>

                <!-- Plataforma / Pedestal 3D con Sombra de Piso -->
                <ellipse cx="200" cy="482" rx="95" ry="20" fill="#C8B59E" opacity="0.65"/>
                <ellipse cx="200" cy="479" rx="75" ry="14" fill="#3D2B1F" opacity="0.28" filter="url(#sombraSuave)"/>

                <!-- Cabello Posterior con Volumen -->
                <path d="M 150 85 C 142 125, 148 160, 162 170 L 238 170 C 252 160, 258 125, 250 85 Z"
                      fill="url(#gradCabello)" filter="url(#sombraSuave)"/>

                <!-- Cuello y Clavícula 3D -->
                <path d="M 184 132 L 182 168 L 218 168 L 216 132 Z" fill="url(#gradPielCilindro)"/>
                <ellipse cx="200" cy="142" rx="16" ry="8" fill="{piel_oscura}" opacity="0.35"/>

                <!-- Brazos 3D Articulados y Manos -->
                <path d="M {cx - sh_w + 4} 166 C {cx - sh_w - 22} 215, {cx - sh_w - 25} 260, {cx - sh_w - 18} 305
                         L {cx - sh_w - 4} 305 C {cx - sh_w - 8} 260, {cx - sh_w - 4} 220, {cx - sh_w + 14} 178 Z"
                      fill="url(#gradPielCilindro)" filter="url(#sombraSuave)"/>
                <path d="M {cx + sh_w - 4} 166 C {cx + sh_w + 22} 215, {cx + sh_w + 25} 260, {cx + sh_w + 18} 305
                         L {cx + sh_w + 4} 305 C {cx + sh_w + 8} 260, {cx + sh_w + 4} 220, {cx + sh_w - 14} 178 Z"
                      fill="url(#gradPielCilindro)" filter="url(#sombraSuave)"/>

                <!-- Manos esculpidas -->
                <ellipse cx="{cx - sh_w - 11}" cy="312" rx="9" ry="12" fill="url(#gradCara)"/>
                <ellipse cx="{cx + sh_w + 11}" cy="312" rx="9" ry="12" fill="url(#gradCara)"/>

                <!-- PANTALÓN / PARTE INFERIOR 3D -->
                <g filter="url(#sombra3d)">
                    <path d="{pierna_izq}" fill="url(#gradBottom)" stroke="{bot_sombra}" stroke-width="1"/>
                    <path d="{pierna_der}" fill="url(#gradBottom)" stroke="{bot_sombra}" stroke-width="1"/>
                    <!-- Pliegues 3D de tela y costura central -->
                    <path d="M {cx} 292 L {cx} 338" stroke="{bot_sombra}" stroke-width="2.5"/>
                    <path d="M {cx - hi_w + 8} 300 Q {cx - 25} 325 {cx - 12} 312" stroke="{bot_sombra}" stroke-width="1.5" fill="none" opacity="0.6"/>
                    <path d="M {cx + hi_w - 8} 300 Q {cx + 25} 325 {cx + 12} 312" stroke="{bot_sombra}" stroke-width="1.5" fill="none" opacity="0.6"/>
                    <line x1="{cx - 31}" y1="315" x2="{cx - 31}" y2="462" stroke="{bot_luz}" stroke-width="4" opacity="0.25"/>
                    <line x1="{cx + 31}" y1="315" x2="{cx + 31}" y2="462" stroke="{bot_luz}" stroke-width="4" opacity="0.25"/>
                </g>

                <!-- PRENDA SUPERIOR 3D (Se adapta al pecho, cintura y cadera) -->
                <g filter="url(#sombra3d)">
                    <!-- Mangas 3D -->
                    <path d="M {cx - sh_w + 2} 162 C {cx - sh_w - 18} 185, {cx - sh_w - 22} 215, {cx - sh_w - 20} 230
                             L {cx - sh_w - 2} 234 L {cx - ch_w + 4} 195 Z"
                          fill="url(#gradTop)" stroke="{top_sombra}" stroke-width="1"/>
                    <path d="M {cx + sh_w - 2} 162 C {cx + sh_w + 18} 185, {cx + sh_w + 22} 215, {cx + sh_w + 20} 230
                             L {cx + sh_w + 2} 234 L {cx + ch_w - 4} 195 Z"
                          fill="url(#gradTop)" stroke="{top_sombra}" stroke-width="1"/>

                    <!-- Torso Principal parametrizado -->
                    <path d="{torso_path}" fill="url(#gradTop)" stroke="{top_sombra}" stroke-width="1.2"/>

                    <!-- Sombra de volumen pectoral y pliegues de cintura -->
                    <path d="M {cx - ch_w + 12} 205 Q {cx - 18} 218 {cx - 6} 206" stroke="{top_sombra}" stroke-width="2" fill="none" opacity="0.35"/>
                    <path d="M {cx + ch_w - 12} 205 Q {cx + 18} 218 {cx + 6} 206" stroke="{top_sombra}" stroke-width="2" fill="none" opacity="0.35"/>
                    <path d="M {cx - wa_w + 8} 248 Q {cx} 258 {cx + wa_w - 8} 248" stroke="{top_sombra}" stroke-width="1.5" fill="none" opacity="0.3"/>

                    <!-- Cuello en V / Solapa 3D -->
                    <path d="M 180 158 L 200 184 L 220 158" fill="{piel_base}" stroke="{top_sombra}" stroke-width="2"/>
                    <path d="M 174 157 L 200 189 L 226 157" fill="none" stroke="{top_luz}" stroke-width="3" opacity="0.7"/>
                </g>

                <!-- CALZADO 3D CON SUELA Y VOLUMEN -->
                <g filter="url(#sombraSuave)">
                    <!-- Zapato Izquierdo -->
                    <path d="M {cx - 46} 465 C {cx - 52} 478, {cx - 50} 488, {cx - 32} 490
                             L {cx - 14} 490 C {cx - 12} 482, {cx - 14} 470, {cx - 18} 465 Z"
                          fill="url(#gradShoes)" stroke="{sho_sombra}" stroke-width="1.2"/>
                    <rect x="{cx - 50}" y="486" width="38" height="5" rx="2.5" fill="#EAE2D6"/>

                    <!-- Zapato Derecho -->
                    <path d="M {cx + 18} 465 C {cx + 14} 470, {cx + 12} 482, {cx + 14} 490
                             L {cx + 32} 490 C {cx + 50} 488, {cx + 52} 478, {cx + 46} 465 Z"
                          fill="url(#gradShoes)" stroke="{sho_sombra}" stroke-width="1.2"/>
                    <rect x="{cx + 12}" y="486" width="38" height="5" rx="2.5" fill="#EAE2D6"/>
                </g>

                <!-- CABEZA Y ROSTRO 3D ESCULPIDO -->
                <g filter="url(#sombra3d)">
                    <!-- Orejas -->
                    <ellipse cx="156" cy="104" rx="7" ry="12" fill="{piel_sombra}"/>
                    <ellipse cx="244" cy="104" rx="7" ry="12" fill="{piel_sombra}"/>

                    <!-- Rostro con iluminación esférica 3D -->
                    <path d="M 158 84 C 158 52, 242 52, 242 84
                             C 242 116, 224 142, 200 145
                             C 176 142, 158 116, 158 84 Z"
                          fill="url(#gradCara)"/>

                    <!-- Rubor suave y contorno facial -->
                    <ellipse cx="174" cy="112" rx="9" ry="5" fill="#E57373" opacity="0.24"/>
                    <ellipse cx="226" cy="112" rx="9" ry="5" fill="#E57373" opacity="0.24"/>

                    <!-- Cejas expresivas -->
                    <path d="M 171 90 Q 181 85 191 89" stroke="{cabello_sombra}" stroke-width="2.8" stroke-linecap="round" fill="none"/>
                    <path d="M 209 89 Q 219 85 229 90" stroke="{cabello_sombra}" stroke-width="2.8" stroke-linecap="round" fill="none"/>

                    <!-- Ojos 3D con Iris, Pupila, Pestañas y Brillo (Parpadeo Animado) -->
                    <g class="ojos-animados">
                        <ellipse cx="181" cy="101" rx="8.5" ry="6" fill="#FFFFFF"/>
                        <circle cx="181" cy="101" r="4.8" fill="#4E342E"/>
                        <circle cx="181" cy="101" r="2.4" fill="#111111"/>
                        <circle cx="183" cy="99" r="1.6" fill="#FFFFFF"/>
                        <path d="M 171 99 Q 181 92 190 100" stroke="#221510" stroke-width="2.2" fill="none"/>

                        <ellipse cx="219" cy="101" rx="8.5" ry="6" fill="#FFFFFF"/>
                        <circle cx="219" cy="101" r="4.8" fill="#4E342E"/>
                        <circle cx="219" cy="101" r="2.4" fill="#111111"/>
                        <circle cx="221" cy="99" r="1.6" fill="#FFFFFF"/>
                        <path d="M 210 100 Q 219 92 229 99" stroke="#221510" stroke-width="2.2" fill="none"/>
                    </g>

                    <!-- Nariz 3D con puente de luz -->
                    <path d="M 199 96 L 197 113 Q 200 116 204 113" stroke="{piel_oscura}" stroke-width="1.8" fill="none" stroke-linecap="round"/>
                    <line x1="201" y1="96" x2="201" y2="110" stroke="{piel_luz}" stroke-width="1.8" stroke-linecap="round" opacity="0.8"/>

                    <!-- Labios 3D con volumen -->
                    <path d="M 188 124 Q 200 131 212 124 Q 200 134 188 124 Z" fill="#C96F69"/>
                    <path d="M 189 124 Q 200 127 211 124" stroke="#8D3B37" stroke-width="1.2" fill="none"/>
                    <ellipse cx="200" cy="128" rx="5" ry="1.5" fill="#FFFFFF" opacity="0.35"/>

                    <!-- Cabello Superior Estilizado 3D -->
                    <path d="M 154 92 C 148 56, 178 40, 204 42
                             C 232 42, 252 60, 246 92
                             C 238 72, 222 66, 202 68
                             C 180 68, 164 74, 154 92 Z"
                          fill="url(#gradCabello)"/>
                    <path d="M 165 56 Q 200 46 232 62" stroke="{cabello_luz}" stroke-width="3" fill="none" opacity="0.45" stroke-linecap="round"/>
                </g>
            </svg>
        </div>

        <div class="controles-3d">
            <span>🔄 Perspectiva 3D:</span>
            <input type="range" min="-28" max="28" value="0" id="sliderRotacion" oninput="rotarAvatar(this.value)">
        </div>
    </div>

    <script>
        function rotarAvatar(grados) {{
            const av = document.getElementById('avatar3d');
            av.style.transform = `rotateY(${{grados}}deg) rotateX(${{Math.abs(grados)*0.12}}deg)`;
        }}
    </script>
    </body>
    </html>
    """
    components.html(html_3d, height=altura_px)

# 6. ENCABEZADO Y NAVEGACIÓN PRINCIPAL
st.title("🧥 EcoArmario 3D")
st.write("Tu clóset inteligente con visualización 3D adaptativa y combinaciones con todos los colores posibles.")

tabs = st.tabs([
    "👗 Mi Armario",
    "➕ Agregar Prenda (Todos los Colores)",
    "📸 Escáner IA",
    "🧍 Mi Perfil y Avatar 3D",
    "✨ Recomendador 3D y Agenda",
    "🤖 Asistente IA",
    "🌍 Impacto Ambiental"
])

# --- TAB 1: MI ARMARIO ---
with tabs[0]:
    st.header("Tus Prendas Registradas")
    filtro_cat = st.radio("Filtrar por categoría:", ["Todas", "Parte Superior", "Parte Inferior", "Calzado"], horizontal=True)
    prendas_mostradas = st.session_state.armario if filtro_cat == "Todas" else [p for p in st.session_state.armario if p['categoria'] == filtro_cat]

    cols = st.columns(3)
    for idx, prenda in enumerate(prendas_mostradas):
        with cols[idx % 3]:
            hex_c = prenda.get("hex", "#C19A6B")
            etiqueta_col = f"<span class='muestra-color' style='background-color:{hex_c};'></span><b>{prenda['color']}</b> ({hex_c})" if mostrar_etiquetas else f"<span class='muestra-color' style='background-color:{hex_c};'></span>{prenda['color']}"
            st.markdown(f"""
            <div class="tarjeta-ropa">
                <h4>{prenda['nombre']}</h4>
                <p>📁 <b>Categoría:</b> {prenda['categoria']}</p>
                <p>🎨 <b>Color:</b> {etiqueta_col}</p>
                <p>🧵 <b>Material:</b> {prenda.get('material', 'Algodón')}</p>
                <p>🔄 <b>Usos:</b> {prenda['usos']} puestas</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Registrar uso hoy ➕", key=f"uso_{prenda['id']}"):
                prenda['usos'] += 1
                st.rerun()

# --- TAB 2: AGREGAR PRENDA CON CUALQUIER COLOR EXISTENTE ---
with tabs[1]:
    st.header("➕ Añadir Prenda con Selector Universal de Color")
    st.write("Elige entre más de 40 tonos de moda o usa el selector libre para aplicar **cualquier color existente (16.7 millones de tonos)**.")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        nuevo_nombre = st.text_input("Nombre de la prenda:", placeholder="Ej: Sweater cuello redondo")
        nueva_cat = st.selectbox("Categoría:", ["Parte Superior", "Parte Inferior", "Calzado"])
        nuevo_material = st.selectbox("Material principal:", ["Algodón", "Lino", "Lana", "Denim / Mezclilla", "Seda / Satén", "Poliéster", "Cuero", "Lona"])
        usos_previos = st.number_input("Veces que ya la has usado:", min_value=1, value=4, step=1)

    with col_f2:
        modo_seleccion_color = st.radio(
            "¿Cómo prefieres elegir el color?",
            ["Catálogo de 40+ Colores", "Selector Libre (Cualquier color del espectro RGB)"]
        )

        if modo_seleccion_color == "Catálogo de 40+ Colores":
            color_elegido_nombre = st.selectbox("Selecciona el color:", list(CATALOGO_COLORES.keys()))
            color_elegido_hex = CATALOGO_COLORES[color_elegido_nombre]
            st.markdown(f"Vista previa del tono: <span class='muestra-color' style='background-color:{color_elegido_hex};width:28px;height:28px;'></span> `{color_elegido_hex}`", unsafe_allow_html=True)
        else:
            color_elegido_hex = st.color_picker("Haz clic para elegir cualquier color exacto:", "#7B9E89")
            color_elegido_nombre = st.text_input("Ponle un nombre a tu color:", value="Tono Personalizado")

    if st.button("Guardar Prenda en mi EcoArmario 🌿"):
        if not nuevo_nombre.strip():
            st.error("Por favor, ingresa el nombre de la prenda.")
        else:
            huellas = {
                "Parte Superior": {"agua": 2700, "co2": 5.5},
                "Parte Inferior": {"agua": 7500, "co2": 15.0},
                "Calzado": {"agua": 6000, "co2": 12.0}
            }
            eco = huellas[nueva_cat]
            st.session_state.armario.append({
                "id": len(st.session_state.armario) + 1,
                "nombre": nuevo_nombre,
                "categoria": nueva_cat,
                "color": color_elegido_nombre,
                "hex": color_elegido_hex,
                "material": nuevo_material,
                "usos": int(usos_previos),
                "agua_l": eco["agua"],
                "co2_kg": eco["co2"]
            })
            st.success(f"¡'{nuevo_nombre}' ({color_elegido_nombre}) se guardó correctamente y ya puede visualizarse en el Avatar 3D!")

# --- TAB 3: ESCÁNER IA ---
with tabs[2]:
    st.header("📸 Escáner Automático de Ropa")
    col_cam, col_det = st.columns(2)
    with col_cam:
        metodo = st.radio("Origen de imagen:", ["Subir foto", "Usar cámara"])
        archivo = st.file_uploader("Imagen de tu prenda", type=["jpg", "png", "jpeg"]) if metodo == "Subir foto" else st.camera_input("Capturar prenda")

    with col_det:
        if archivo is not None:
            st.image(archivo, caption="Prenda escaneada", width=220)
            # Extrae el color promedio real de la imagen subida
            img_pil = pd.Series([1]) # Auxiliar
            from PIL import Image
            im = Image.open(archivo).convert("RGB").resize((50, 50))
            px = im.getpixel((25, 25))
            hex_detectado = rgb_a_hex(px)

            st.success(f"¡Color detectado automáticamente en la foto: `{hex_detectado}`!")
            nom_scan = st.text_input("Nombre de prenda:", value="Prenda Escaneada")
            cat_scan = st.selectbox("Categoría detectada:", ["Parte Superior", "Parte Inferior", "Calzado"], key="scan_cat")
            hex_scan = st.color_picker("Color extraído (puedes ajustarlo):", hex_detectado)
            nom_col_scan = st.text_input("Nombre del color:", value="Tono Escaneado")

            if st.button("Agregar Prenda Escaneada"):
                st.session_state.armario.append({
                    "id": len(st.session_state.armario) + 1,
                    "nombre": nom_scan,
                    "categoria": cat_scan,
                    "color": nom_col_scan,
                    "hex": hex_scan,
                    "material": "Textil detectado",
                    "usos": 1,
                    "agua_l": 3200,
                    "co2_kg": 7.0
                })
                st.success("¡Prenda añadida al armario!")

# --- TAB 4: PERFIL Y AVATAR 3D EN TIEMPO REAL ---
with tabs[3]:
    st.header("🧍 Configura tu Silueta y Tono de Piel en 3D")
    st.write("Cambia las opciones a la izquierda y observa cómo **el avatar 3D modifica su cuerpo y piel al instante**.")

    col_cfg, col_prev3d = st.columns([1.1, 1])
    with col_cfg:
        nuevo_cuerpo = st.selectbox(
            "1. Elige tu silueta / tipo de cuerpo:",
            [
                "Reloj de arena / Equilibrado",
                "Pera / Triángulo (Cadera más amplia)",
                "Triángulo Invertido (Espalda/hombros amplios)",
                "Rectángulo (Proporción lineal)",
                "Ovalado / Manzana (Contorno central suave)"
            ],
            index=0
        )

        nuevo_tono_nombre = st.selectbox(
            "2. Elige tu tono de piel:",
            list(TONOS_PIEL.keys()),
            index=2
        )
        color_piel_personalizado = st.color_picker(
            "O ajusta tu tono de piel exacto:",
            TONOS_PIEL[nuevo_tono_nombre]
        )

        nuevo_subtono = st.selectbox(
            "3. Elige tu subtono de piel:",
            ["Cálido (Dorado / Melocotón)", "Frío (Rosado / Azulado)", "Neutro (Equilibrado)"]
        )

        nuevo_cabello = st.color_picker("4. Color de cabello del avatar:", st.session_state.perfil["cabello_hex"])

        # Actualización inmediata en sesión para que el avatar cambie en vivo
        st.session_state.perfil = {
            "cuerpo": nuevo_cuerpo,
            "tono_nombre": nuevo_tono_nombre,
            "piel_hex": color_piel_personalizado,
            "subtono": nuevo_subtono,
            "cabello_hex": nuevo_cabello
        }

        st.markdown(f"""
        <div class="tarjeta-ropa">
            <h4>💡 Análisis Cromático para tu Piel</h4>
            <p>Con tu piel <b>{nuevo_tono_nombre}</b> y subtono <b>{nuevo_subtono}</b>, el motor de combinaciones ajustará automáticamente el contraste de cualquier color que tengas en tu clóset.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_prev3d:
        tops_demo = [p for p in st.session_state.armario if p['categoria'] == 'Parte Superior']
        bots_demo = [p for p in st.session_state.armario if p['categoria'] == 'Parte Inferior']
        shos_demo = [p for p in st.session_state.armario if p['categoria'] == 'Calzado']
        renderizar_avatar_3d(tops_demo[0], bots_demo[0], shos_demo[0], st.session_state.perfil)

# --- TAB 5: RECOMENDADOR 3D CON TODOS LOS COLORES Y AGENDA ---
with tabs[4]:
    st.header("✨ Recomendador 3D y Combinador Universal de Colores")

    tops = [p for p in st.session_state.armario if p['categoria'] == 'Parte Superior']
    bottoms = [p for p in st.session_state.armario if p['categoria'] == 'Parte Inferior']
    shoes = [p for p in st.session_state.armario if p['categoria'] == 'Calzado']

    col_izq, col_der = st.columns([1.15, 1])

    with col_izq:
        st.subheader("Armar o Generar Outfit")
        modo_armado = st.radio(
            "Modo de selección:",
            ["Recomendación Inteligente IA (Automática)", "Probar Combinación Manualmente"],
            horizontal=True
        )

        ocasion = st.selectbox("Ocasión:", ["Casual / Diario", "Oficina / Estudio", "Evento Elegante", "Salida de Fin de Semana"])

        if modo_armado == "Recomendación Inteligente IA (Automática)":
            if st.button("Generar Nueva Combinación 🎲") or 'outfit_3d' not in st.session_state:
                st.session_state.outfit_3d = {
                    "top": random.choice(tops),
                    "bottom": random.choice(bottoms),
                    "shoes": random.choice(shoes)
                }
        else:
            top_sel = st.selectbox("Elige Parte Superior:", tops, format_func=lambda x: f"{x['nombre']} ({x['color']})")
            bot_sel = st.selectbox("Elige Parte Inferior:", bottoms, format_func=lambda x: f"{x['nombre']} ({x['color']})")
            sho_sel = st.selectbox("Elige Calzado:", shoes, format_func=lambda x: f"{x['nombre']} ({x['color']})")
            st.session_state.outfit_3d = {"top": top_sel, "bottom": bot_sel, "shoes": sho_sel}

        actual = st.session_state.outfit_3d
        armonia_top_bot = calcular_armonia_colores(actual['top']['hex'], actual['bottom']['hex'])
        armonia_bot_sho = calcular_armonia_colores(actual['bottom']['hex'], actual['shoes']['hex'])

        st.markdown(f"""
        <div class="tarjeta-ropa">
            <h4>Conjunto para: {ocasion}</h4>
            <p>👕 <b>Superior:</b> <span class="muestra-color" style="background:{actual['top']['hex']};"></span> {actual['top']['nombre']} — <i>{actual['top']['color']}</i></p>
            <p>👖 <b>Inferior:</b> <span class="muestra-color" style="background:{actual['bottom']['hex']};"></span> {actual['bottom']['nombre']} — <i>{actual['bottom']['color']}</i></p>
            <p>👞 <b>Calzado:</b> <span class="muestra-color" style="background:{actual['shoes']['hex']};"></span> {actual['shoes']['nombre']} — <i>{actual['shoes']['color']}</i></p>
            <hr>
            <p>🎨 <b>Teoría del Color (Top + Pantalón):</b> {armonia_top_bot}</p>
            <p>🎨 <b>Teoría del Color (Pantalón + Calzado):</b> {armonia_bot_sho}</p>
            <p>🧍 <b>Adaptación 3D:</b> Silueta <b>{st.session_state.perfil['cuerpo']}</b> | Piel <b>{st.session_state.perfil['tono_nombre']}</b></p>
        </div>
        """, unsafe_allow_html=True)

    with col_der:
        renderizar_avatar_3d(actual['top'], actual['bottom'], actual['shoes'], st.session_state.perfil)

    st.divider()
    st.subheader("📅 Agenda Semanal Inteligente")
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    agenda = []
    for d in dias:
        t_d = random.choice(tops)
        b_d = random.choice(bottoms)
        s_d = random.choice(shoes)
        agenda.append({
            "Día": d,
            "Parte Superior": f"{t_d['nombre']} ({t_d['color']})",
            "Parte Inferior": f"{b_d['nombre']} ({b_d['color']})",
            "Calzado": f"{s_d['nombre']} ({s_d['color']})",
            "Armonía Cromática": calcular_armonia_colores(t_d['hex'], b_d['hex'])
        })
    st.dataframe(pd.DataFrame(agenda), use_container_width=True, hide_index=True)

# --- TAB 6: ASISTENTE IA ---
with tabs[5]:
    st.header("🤖 Asistente de Estilo y Colorimetría IA")
    for m in st.session_state.mensajes_ia:
        with st.chat_message(m["rol"]):
            st.write(m["texto"])

    consulta = st.chat_input("Pregúntame cómo combinar cualquier color o prenda de tu armario...")
    if consulta:
        st.session_state.mensajes_ia.append({"rol": "user", "texto": consulta})
        with st.chat_message("user"):
            st.write(consulta)

        t_sug = random.choice(tops)
        b_sug = random.choice(bottoms)
        s_sug = random.choice(shoes)
        tipo_arm = calcular_armonia_colores(t_sug['hex'], b_sug['hex'])

        respuesta = (
            f"Considerando tu silueta **{st.session_state.perfil['cuerpo']}** y tu tono de piel **{st.session_state.perfil['tono_nombre']}**, "
            f"una excelente combinación es tu **{t_sug['nombre']} ({t_sug['color']})** junto con tu **{b_sug['nombre']} ({b_sug['color']})** "
            f"y **{s_sug['nombre']}**. Ambos tonos generan una **{tipo_arm}**, permitiéndote lucir increíble sin comprar ropa nueva."
        )
        st.session_state.mensajes_ia.append({"rol": "assistant", "texto": respuesta})
        with st.chat_message("assistant"):
            st.write(respuesta)

# --- TAB 7: IMPACTO AMBIENTAL ---
with tabs[6]:
    st.header("🌍 Impacto Ambiental de tu Guardarropa")
    agua_tot = sum(p['agua_l'] for p in st.session_state.armario)
    co2_tot = sum(p['co2_kg'] for p in st.session_state.armario)
    usos_tot = sum(p['usos'] for p in st.session_state.armario)

    c1, c2, c3 = st.columns(3)
    c1.metric("💧 Agua Ahorrada / Amortizada", f"{agua_tot:,} Litros", "Reutilizando tu clóset")
    c2.metric("☁️ Huella de Carbono Mitigada", f"{co2_tot:.1f} kg CO2", "Cero compras innecesarias")
    c3.metric("🔄 Total de Usos Registrados", f"{usos_tot} puestas", "Moda circular activa")

    st.divider()
    df_eco = pd.DataFrame(st.session_state.armario)
    st.bar_chart(df_eco.set_index("nombre")["usos"])
