import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import colorsys
from PIL import Image

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="EcoArmario 3D - Closet Digital Sostenible",
    page_icon="🌿",
    layout="wide"
)

# 2. CATÁLOGO DE COLORES Y TONOS DE PIEL
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

# Funciones de color e iluminación 3D
def hex_a_rgb(hex_str):
    if not isinstance(hex_str, str):
        return (180, 160, 140)
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        return (180, 160, 140)
    try:
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return (180, 160, 140)

def rgb_a_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(
        max(0, min(255, int(rgb[0]))),
        max(0, min(255, int(rgb[1]))),
        max(0, min(255, int(rgb[2])))
    )

def ajustar_luz_color(hex_str, factor_luz):
    """Calcula brillos y sombras 3D para cualquier color seleccionado"""
    r, g, b = [x / 255.0 for x in hex_a_rgb(hex_str)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l_nuevo = max(0.04, min(0.96, l * factor_luz))
    r2, g2, b2 = colorsys.hls_to_rgb(h, l_nuevo, s)
    return rgb_a_hex((r2 * 255, g2 * 255, b2 * 255))

def calcular_armonia_colores(hex1, hex2):
    """Calcula la compatibilidad entre dos colores cualesquiera"""
    r1, g1, b1 = [x / 255.0 for x in hex_a_rgb(hex1)]
    r2, g2, b2 = [x / 255.0 for x in hex_a_rgb(hex2)]
    h1, l1, s1 = colorsys.rgb_to_hls(r1, g1, b1)
    h2, l2, s2 = colorsys.rgb_to_hls(r2, g2, b2)

    if s1 < 0.18 or s2 < 0.18 or l1 > 0.88 or l2 > 0.88 or l1 < 0.15 or l2 < 0.15:
        return "Armonía con Neutro Comodín (98% Compatible)"
    
    diff_hue = abs(h1 - h2) * 360
    if diff_hue > 180:
        diff_hue = 360 - diff_hue

    if diff_hue < 20:
        return "Armonía Monocromática (96% Compatible)"
    elif diff_hue < 55:
        return "Armonía Análoga Suave (93% Compatible)"
    elif 150 <= diff_hue <= 210:
        return "Contraste Complementario (91% Compatible)"
    else:
        return "Combinación Equilibrada (88% Compatible)"

# 3. AUTORREPARACIÓN DE SESIÓN (Evita el KeyError en Streamlit Cloud)
PERFIL_PREDETERMINADO = {
    "cuerpo": "Reloj de arena / Equilibrado",
    "tono_nombre": "Trigueño Claro",
    "piel_hex": "#E8B993",
    "subtono": "Cálido (Dorado / Melocotón)",
    "cabello_hex": "#3B2618"
}

if 'perfil' not in st.session_state:
    st.session_state.perfil = PERFIL_PREDETERMINADO.copy()
else:
    # Si la sesión ya venía abierta de una versión previa, rellena las claves que faltaban
    for k, v in PERFIL_PREDETERMINADO.items():
        if k not in st.session_state.perfil:
            st.session_state.perfil[k] = v

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
else:
    # Asegura que cada prenda antigua tenga su código HEX
    for prenda in st.session_state.armario:
        if "hex" not in prenda:
            prenda["hex"] = CATALOGO_COLORES.get(prenda.get("color", "Camel"), "#C19A6B")
        if "material" not in prenda:
            prenda["material"] = "Algodón mixto"

if 'mensajes_ia' not in st.session_state:
    st.session_state.mensajes_ia = [
        {"rol": "assistant", "texto": "¡Hola! Soy tu asistente de estilo 3D de EcoArmario. Puedo crear combinaciones elegantes con cualquier prenda de tu clóset adaptándolas a tu silueta. ¿Para qué ocasión necesitas vestir hoy?"}
    ]

# 4. BARRA LATERAL Y ESTILOS
st.sidebar.title("🌿 EcoArmario 3D")
st.sidebar.markdown("*Moda sostenible y personal.*")
st.sidebar.divider()

st.sidebar.subheader("👁️ Accesibilidad (Daltonismo)")
modo_daltonismo = st.sidebar.selectbox(
    "Modo visual:",
    ["Estándar (Tonos Elegantes)", "Protanopia (Sin Rojo)", "Deuteranopia (Sin Verde)", "Tritanopia (Sin Azul)", "Alto Contraste"]
)
mostrar_etiquetas = st.sidebar.checkbox("Mostrar nombres y códigos de color", value=True)

paletas = {
    "Estándar (Tonos Elegantes)": {"bg": "#F8F5EE", "sec_bg": "#EFE6D8", "text": "#3D2B1F", "accent": "#8A5A36", "card": "#FFFFFF"},
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
        border: 1px solid #666; vertical-align: middle; margin-right: 6px;
    }}
    h1, h2, h3, h4, p, label {{ color: {tema['text']} !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. GENERADOR DE AVATAR 3D
def renderizar_avatar_3d(top_prenda, bottom_prenda, shoes_prenda, perfil, altura_px=565):
    cuerpo = perfil.get("cuerpo", "Reloj de arena / Equilibrado")
    tono_nombre = perfil.get("tono_nombre", "Trigueño Claro")
    piel_hex = perfil.get("piel_hex", "#E8B993")
    subtono = perfil.get("subtono", "Cálido (Dorado / Melocotón)")
    cabello_hex = perfil.get("cabello_hex", "#3B2618")

    # Adaptación anatómica de la silueta
    if "Reloj de arena" in cuerpo:
        sh_w, ch_w, wa_w, hi_w = 56, 48, 33, 54
    elif "Pera" in cuerpo:
        sh_w, ch_w, wa_w, hi_w = 44, 40, 34, 62
    elif "Invertido" in cuerpo:
        sh_w, ch_w, wa_w, hi_w = 65, 56, 40, 42
    elif "Rectángulo" in cuerpo:
        sh_w, ch_w, wa_w, hi_w = 50, 46, 44, 47
    else:
        sh_w, ch_w, wa_w, hi_w = 53, 55, 58, 52

    # Matiz según subtono de piel
    r_p, g_p, b_p = hex_a_rgb(piel_hex)
    if "Cálido" in subtono:
        piel_base = rgb_a_hex((r_p + 6, g_p + 2, b_p - 5))
    elif "Frío" in subtono:
        piel_base = rgb_a_hex((r_p + 3, g_p - 2, b_p + 6))
    else:
        piel_base = piel_hex

    piel_luz = ajustar_luz_color(piel_base, 1.18)
    piel_sombra = ajustar_luz_color(piel_base, 0.78)
    piel_oscura = ajustar_luz_color(piel_base, 0.62)

    cabello_luz = ajustar_luz_color(cabello_hex, 1.35)
    cabello_sombra = ajustar_luz_color(cabello_hex, 0.65)

    top_hex = top_prenda.get("hex", "#C19A6B")
    top_luz = ajustar_luz_color(top_hex, 1.22)
    top_sombra = ajustar_luz_color(top_hex, 0.72)

    bot_hex = bottom_prenda.get("hex", "#6F4E37")
    bot_luz = ajustar_luz_color(bot_hex, 1.20)
    bot_sombra = ajustar_luz_color(bot_hex, 0.68)

    sho_hex = shoes_prenda.get("hex", "#4B3020")
    sho_luz = ajustar_luz_color(sho_hex, 1.25)
    sho_sombra = ajustar_luz_color(sho_hex, 0.60)

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
        M {cx - hi_w} 288 L {cx + 2} 294 L {cx - 4} 345
        C {cx - 6} 390, {cx - 14} 435, {cx - 18} 468
        L {cx - 44} 468 C {cx - 46} 425, {cx - hi_w - 4} 355, {cx - hi_w} 288 Z
    """

    pierna_der = f"""
        M {cx - 2} 294 L {cx + hi_w} 288
        C {cx + hi_w + 4} 355, {cx + 46} 425, {cx + 44} 468
        L {cx + 18} 468 C {cx + 14} 435, {cx + 6} 390, {cx + 4} 345 Z
    """

    html_3d = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0; padding: 0; background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex; flex-direction: column; align-items: center;
        }}
        .escena-3d {{
            width: 390px; height: 535px;
            background: radial-gradient(circle at 50% 35%, #FFFDF9 0%, #EFE6D5 65%, #DFCFB5 100%);
            border-radius: 20px;
            box-shadow: inset 0 0 35px rgba(90,60,35,0.12), 0 10px 24px rgba(0,0,0,0.08);
            border: 2px solid #D5C3AE;
            position: relative; overflow: hidden;
            perspective: 900px;
        }}
        .contenedor-avatar {{
            width: 100%; height: 100%;
            transform-style: preserve-3d;
            transition: transform 0.2s ease-out;
            animation: respirar 3.6s ease-in-out infinite;
        }}
        @keyframes respirar {{
            0%, 100% {{ transform: translateY(0px) scaleY(1); }}
            50% {{ transform: translateY(-3.5px) scaleY(1.006); }}
        }}
        @keyframes parpadear {{
            0%, 94%, 98%, 100% {{ transform: scaleY(1); }}
            96% {{ transform: scaleY(0.1); }}
        }}
        .ojos {{
            transform-origin: 200px 102px;
            animation: parpadear 4s infinite;
        }}
        .controles-3d {{
            position: absolute; bottom: 12px; left: 16px; right: 16px;
            background: rgba(255, 255, 255, 0.90);
            backdrop-filter: blur(4px);
            border-radius: 10px; padding: 6px 14px;
            display: flex; justify-content: space-between; align-items: center;
            font-size: 12px; color: #3B281E; font-weight: 600;
        }}
        .etiqueta {{
            position: absolute; top: 12px; left: 14px;
            background: rgba(60, 40, 25, 0.85); color: #FFF;
            padding: 5px 12px; border-radius: 16px; font-size: 11px;
        }}
        input[type=range] {{ accent-color: #8A5A36; width: 140px; cursor: pointer; }}
    </style>
    </head>
    <body>
    <div class="escena-3d">
        <div class="etiqueta">✨ {cuerpo} | Piel: {tono_nombre}</div>
        <div class="contenedor-avatar" id="avatar3d">
            <svg viewBox="0 0 400 530" width="100%" height="100%">
                <defs>
                    <filter id="sombra" x="-15%" y="-15%" width="130%" height="130%">
                        <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#2A1B12" flood-opacity="0.25"/>
                    </filter>
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
                    <linearGradient id="gradCabello" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="{cabello_sombra}"/>
                        <stop offset="35%" stop-color="{cabello_hex}"/>
                        <stop offset="52%" stop-color="{cabello_luz}"/>
                        <stop offset="75%" stop-color="{cabello_hex}"/>
                        <stop offset="100%" stop-color="{cabello_sombra}"/>
                    </linearGradient>
                    <linearGradient id="gradTop" x1="0%" y1="0%" x2="100%" y2="20%">
                        <stop offset="0%" stop-color="{top_sombra}"/>
                        <stop offset="30%" stop-color="{top_luz}"/>
                        <stop offset="65%" stop-color="{top_hex}"/>
                        <stop offset="100%" stop-color="{top_sombra}"/>
                    </linearGradient>
                    <linearGradient id="gradBot" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="{bot_sombra}"/>
                        <stop offset="30%" stop-color="{bot_luz}"/>
                        <stop offset="65%" stop-color="{bot_hex}"/>
                        <stop offset="100%" stop-color="{bot_sombra}"/>
                    </linearGradient>
                    <radialGradient id="gradZap" cx="38%" cy="30%" r="70%">
                        <stop offset="0%" stop-color="{sho_luz}"/>
                        <stop offset="55%" stop-color="{sho_hex}"/>
                        <stop offset="100%" stop-color="{sho_sombra}"/>
                    </radialGradient>
                </defs>

                <!-- Sombra de piso -->
                <ellipse cx="200" cy="482" rx="85" ry="16" fill="#3D2B1F" opacity="0.22"/>

                <!-- Cabello posterior -->
                <path d="M 150 85 C 142 125, 148 160, 162 170 L 238 170 C 252 160, 258 125, 250 85 Z" fill="url(#gradCabello)"/>

                <!-- Cuello -->
                <path d="M 184 132 L 182 168 L 218 168 L 216 132 Z" fill="url(#gradPielCilindro)"/>

                <!-- Brazos -->
                <path d="M {cx - sh_w + 4} 166 C {cx - sh_w - 20} 215, {cx - sh_w - 22} 260, {cx - sh_w - 16} 305 L {cx - sh_w - 2} 305 C {cx - sh_w - 6} 260, {cx - sh_w - 4} 220, {cx - sh_w + 14} 178 Z" fill="url(#gradPielCilindro)"/>
                <path d="M {cx + sh_w - 4} 166 C {cx + sh_w + 20} 215, {cx + sh_w + 22} 260, {cx + sh_w + 16} 305 L {cx + sh_w + 2} 305 C {cx + sh_w + 6} 260, {cx + sh_w + 4} 220, {cx + sh_w - 14} 178 Z" fill="url(#gradPielCilindro)"/>
                <ellipse cx="{cx - sh_w - 9}" cy="312" rx="8" ry="11" fill="url(#gradCara)"/>
                <ellipse cx="{cx + sh_w + 9}" cy="312" rx="8" ry="11" fill="url(#gradCara)"/>

                <!-- PANTALÓN -->
                <g filter="url(#sombra)">
                    <path d="{pierna_izq}" fill="url(#gradBot)"/>
                    <path d="{pierna_der}" fill="url(#gradBot)"/>
                    <path d="M {cx} 292 L {cx} 338" stroke="{bot_sombra}" stroke-width="2"/>
                    <line x1="{cx - 30}" y1="315" x2="{cx - 30}" y2="460" stroke="{bot_luz}" stroke-width="3" opacity="0.3"/>
                    <line x1="{cx + 30}" y1="315" x2="{cx + 30}" y2="460" stroke="{bot_luz}" stroke-width="3" opacity="0.3"/>
                </g>

                <!-- PRENDA SUPERIOR -->
                <g filter="url(#sombra)">
                    <path d="M {cx - sh_w + 2} 162 C {cx - sh_w - 16} 185, {cx - sh_w - 18} 215, {cx - sh_w - 18} 230 L {cx - sh_w - 2} 234 L {cx - ch_w + 4} 195 Z" fill="url(#gradTop)"/>
                    <path d="M {cx + sh_w - 2} 162 C {cx + sh_w + 16} 185, {cx + sh_w + 18} 215, {cx + sh_w + 18} 230 L {cx + sh_w + 2} 234 L {cx + ch_w - 4} 195 Z" fill="url(#gradTop)"/>
                    <path d="{torso_path}" fill="url(#gradTop)"/>
                    <!-- Cuello en V -->
                    <path d="M 180 158 L 200 184 L 220 158" fill="{piel_base}" stroke="{top_sombra}" stroke-width="2"/>
                </g>

                <!-- ZAPATOS -->
                <g filter="url(#sombra)">
                    <path d="M {cx - 46} 465 C {cx - 52} 478, {cx - 50} 488, {cx - 32} 490 L {cx - 14} 490 C {cx - 12} 482, {cx - 14} 470, {cx - 18} 465 Z" fill="url(#gradZap)"/>
                    <path d="M {cx + 18} 465 C {cx + 14} 470, {cx + 12} 482, {cx + 14} 490 L {cx + 32} 490 C {cx + 50} 488, {cx + 52} 478, {cx + 46} 465 Z" fill="url(#gradZap)"/>
                </g>

                <!-- CABEZA Y ROSTRO -->
                <g filter="url(#sombra)">
                    <ellipse cx="156" cy="104" rx="6" ry="10" fill="{piel_sombra}"/>
                    <ellipse cx="244" cy="104" rx="6" ry="10" fill="{piel_sombra}"/>
                    <path d="M 158 84 C 158 52, 242 52, 242 84 C 242 116, 224 142, 200 145 C 176 142, 158 116, 158 84 Z" fill="url(#gradCara)"/>
                    
                    <!-- Ojos y Pestañas -->
                    <g class="ojos">
                        <ellipse cx="181" cy="101" rx="8" ry="5.5" fill="#FFF"/>
                        <circle cx="181" cy="101" r="4.2" fill="#3E2723"/>
                        <circle cx="182.5" cy="99.5" r="1.5" fill="#FFF"/>
                        <path d="M 172 99 Q 181 93 190 100" stroke="#221510" stroke-width="2" fill="none"/>

                        <ellipse cx="219" cy="101" rx="8" ry="5.5" fill="#FFF"/>
                        <circle cx="219" cy="101" r="4.2" fill="#3E2723"/>
                        <circle cx="220.5" cy="99.5" r="1.5" fill="#FFF"/>
                        <path d="M 210 100 Q 219 93 228 99" stroke="#221510" stroke-width="2" fill="none"/>
                    </g>

                    <!-- Cejas y Nariz -->
                    <path d="M 172 90 Q 181 86 190 90" stroke="{cabello_sombra}" stroke-width="2.5" fill="none"/>
                    <path d="M 210 90 Q 219 86 228 90" stroke="{cabello_sombra}" stroke-width="2.5" fill="none"/>
                    <path d="M 199 97 L 197 112 Q 200 115 203 112" stroke="{piel_oscura}" stroke-width="1.6" fill="none"/>

                    <!-- Sonrisa -->
                    <path d="M 188 124 Q 200 132 212 124 Q 200 134 188 124 Z" fill="#C96F69"/>

                    <!-- Cabello Frontal -->
                    <path d="M 154 92 C 148 56, 178 40, 204 42 C 232 42, 252 60, 246 92 C 238 72, 222 66, 202 68 C 180 68, 164 74, 154 92 Z" fill="url(#gradCabello)"/>
                </g>
            </svg>
        </div>

        <div class="controles-3d">
            <span>🔄 Rotación:</span>
            <input type="range" min="-28" max="28" value="0" oninput="document.getElementById('avatar3d').style.transform='rotateY('+this.value+'deg)'">
        </div>
    </div>
    </body>
    </html>
    """
    components.html(html_3d, height=altura_px)

# 6. ENCABEZADO Y PESTAÑAS
st.title("🧥 EcoArmario 3D")
st.write("Tu clóset digital interactivo: combina lo que ya tienes, adapta tu ropa a tu silueta y cuida el planeta.")

tabs = st.tabs([
    "👗 Mi Armario",
    "➕ Agregar Prenda",
    "📸 Escáner IA",
    "🧍 Mi Silueta y Avatar 3D",
    "✨ Recomendador 3D y Agenda",
    "🤖 Asistente IA",
    "🌍 Impacto Ambiental"
])

# --- TAB 1: MI ARMARIO ---
with tabs[0]:
    st.header("Tus Prendas")
    filtro_cat = st.radio("Filtrar por categoría:", ["Todas", "Parte Superior", "Parte Inferior", "Calzado"], horizontal=True)
    prendas_filtradas = st.session_state.armario if filtro_cat == "Todas" else [p for p in st.session_state.armario if p.get('categoria') == filtro_cat]

    cols = st.columns(3)
    for idx, p in enumerate(prendas_filtradas):
        with cols[idx % 3]:
            hex_c = p.get("hex", "#C19A6B")
            etiqueta = f"<span class='muestra-color' style='background:{hex_c};'></span><b>{p.get('color','Tono')}</b> ({hex_c})" if mostrar_etiquetas else f"<span class='muestra-color' style='background:{hex_c};'></span>{p.get('color','Tono')}"
            st.markdown(f"""
            <div class="tarjeta-ropa">
                <h4>{p.get('nombre', 'Prenda')}</h4>
                <p>📁 <b>Tipo:</b> {p.get('categoria', 'Ropa')}</p>
                <p>🎨 <b>Color:</b> {etiqueta}</p>
                <p>🧵 <b>Material:</b> {p.get('material', 'Textil')}</p>
                <p>🔄 <b>Puestas:</b> {p.get('usos', 1)} veces</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Usada hoy ➕", key=f"btn_u_{p.get('id', idx)}"):
                p['usos'] = p.get('usos', 0) + 1
                st.rerun()

# --- TAB 2: AGREGAR PRENDA CON CUALQUIER COLOR ---
with tabs[1]:
    st.header("➕ Añadir Nueva Prenda")
    c1, c2 = st.columns(2)
    with c1:
        nom_in = st.text_input("Nombre de la prenda:", placeholder="Ej: Chompa cuello alto")
        cat_in = st.selectbox("Categoría:", ["Parte Superior", "Parte Inferior", "Calzado"])
        mat_in = st.selectbox("Material:", ["Algodón", "Lino", "Lana", "Denim", "Poliéster", "Cuero", "Lona"])
        usos_in = st.number_input("Veces que ya la has usado:", min_value=1, value=3)

    with c2:
        modo_c = st.radio("Selección de color:", ["Catálogo de 40+ Tonos", "Selector Libre de Color"])
        if modo_c == "Catálogo de 40+ Tonos":
            nom_c = st.selectbox("Color:", list(CATALOGO_COLORES.keys()))
            hex_c = CATALOGO_COLORES[nom_c]
        else:
            hex_c = st.color_picker("Elige cualquier color exacto:", "#8A5A36")
            nom_c = st.text_input("Nombre que le das a ese color:", value="Color Personalizado")
        st.markdown(f"Vista previa: <span class='muestra-color' style='background:{hex_c};width:24px;height:24px;'></span> `{hex_c}`", unsafe_allow_html=True)

    if st.button("Guardar en EcoArmario 🌿"):
        if not nom_in.strip():
            st.error("Escribe el nombre de la prenda.")
        else:
            huellas = {"Parte Superior": (2700, 5.5), "Parte Inferior": (7500, 15.0), "Calzado": (6000, 12.0)}
            ag, co = huellas[cat_in]
            st.session_state.armario.append({
                "id": len(st.session_state.armario) + 1,
                "nombre": nom_in,
                "categoria": cat_in,
                "color": nom_c,
                "hex": hex_c,
                "material": mat_in,
                "usos": int(usos_in),
                "agua_l": ag,
                "co2_kg": co
            })
            st.success(f"¡'{nom_in}' guardado exitosamente!")

# --- TAB 3: ESCÁNER IA ---
with tabs[2]:
    st.header("📸 Escáner de Ropa")
    c_sub, c_res = st.columns(2)
    with c_sub:
        tipo_cam = st.radio("Método:", ["Subir foto", "Usar cámara"])
        foto = st.file_uploader("Sube tu prenda", type=["jpg", "png", "jpeg"]) if tipo_cam == "Subir foto" else st.camera_input("Captura tu prenda")

    with c_res:
        if foto is not None:
            foto.seek(0)
            st.image(foto, caption="Prenda capturada", width=220)
            try:
                foto.seek(0)
                img_p = Image.open(foto).convert("RGB").resize((40, 40))
                color_auto_hex = rgb_a_hex(img_p.getpixel((20, 20)))
            except Exception:
                color_auto_hex = "#8A5A36"

            st.success("¡Color extraído con éxito!")
            nom_scan = st.text_input("Nombre detectado:", value="Prenda Escaneada")
            cat_scan = st.selectbox("Categoría:", ["Parte Superior", "Parte Inferior", "Calzado"], key="sc_c")
            hex_scan = st.color_picker("Tono detectado:", color_auto_hex)
            
            if st.button("Guardar Prenda Escaneada"):
                st.session_state.armario.append({
                    "id": len(st.session_state.armario) + 1,
                    "nombre": nom_scan,
                    "categoria": cat_scan,
                    "color": "Tono Escaneado",
                    "hex": hex_scan,
                    "material": "Algodón mixto",
                    "usos": 1,
                    "agua_l": 3200,
                    "co2_kg": 7.0
                })
                st.success(f"¡'{nom_scan}' agregada a tu clóset!")

# --- TAB 4: PERFIL Y AVATAR 3D EN VIVO ---
with tabs[3]:
    st.header("🧍 Tu Silueta y Tono de Piel en 3D")
    st.write("Configura tus rasgos. **El avatar 3D se actualizará al instante**.")

    col_p, col_av = st.columns([1.1, 1])
    with col_p:
        opciones_cuerpo = [
            "Reloj de arena / Equilibrado",
            "Pera / Triángulo",
            "Triángulo Invertido",
            "Rectángulo",
            "Ovalado / Manzana"
        ]
        cuerpo_actual = st.session_state.perfil.get("cuerpo", opciones_cuerpo[0])
        idx_cuerpo = opciones_cuerpo.index(cuerpo_actual) if cuerpo_actual in opciones_cuerpo else 0

        cuerpo_sel = st.selectbox("1. Tu tipo de cuerpo:", opciones_cuerpo, index=idx_cuerpo)

        opciones_tono = list(TONOS_PIEL.keys())
        tono_actual = st.session_state.perfil.get("tono_nombre", opciones_tono[2])
        idx_tono = opciones_tono.index(tono_actual) if tono_actual in opciones_tono else 0

        tono_sel = st.selectbox("2. Tono de piel general:", opciones_tono, index=idx_tono)
        piel_sel = st.color_picker("O ajusta el tono exacto:", st.session_state.perfil.get("piel_hex", TONOS_PIEL[tono_sel]))

        opciones_subtono = ["Cálido (Dorado / Melocotón)", "Frío (Rosado / Azulado)", "Neutro (Equilibrado)"]
        subtono_actual = st.session_state.perfil.get("subtono", opciones_subtono[0])
        idx_subtono = opciones_subtono.index(subtono_actual) if subtono_actual in opciones_subtono else 0

        subtono_sel = st.selectbox("3. Subtono de piel:", opciones_subtono, index=idx_subtono)

        # Aquí ocurría el error: ahora usa .get() seguro con valor por defecto
        cabello_sel = st.color_picker("4. Color de cabello del avatar:", st.session_state.perfil.get("cabello_hex", "#3B2618"))

        # Actualiza el perfil activo en vivo
        st.session_state.perfil = {
            "cuerpo": cuerpo_sel,
            "tono_nombre": tono_sel,
            "piel_hex": piel_sel,
            "subtono": subtono_sel,
            "cabello_hex": cabello_sel
        }

        st.markdown(f"""
        <div class="tarjeta-ropa">
            <h4>💡 Adaptación Activa</h4>
            <p>El avatar refleja tu cuerpo <b>{cuerpo_sel}</b> con piel <b>{tono_sel}</b> ({subtono_sel}).</p>
        </div>
        """, unsafe_allow_html=True)

    with col_av:
        tops_d = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Superior']
        bots_d = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Inferior']
        shos_d = [p for p in st.session_state.armario if p.get('categoria') == 'Calzado']
        p_top = tops_d[0] if tops_d else {"hex": "#C19A6B"}
        p_bot = bots_d[0] if bots_d else {"hex": "#6F4E37"}
        p_sho = shos_d[0] if shos_d else {"hex": "#4B3020"}
        renderizar_avatar_3d(p_top, p_bot, p_sho, st.session_state.perfil)

# --- TAB 5: RECOMENDADOR Y AGENDA ---
with tabs[4]:
    st.header("✨ Recomendador 3D")
    tops = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Superior']
    bottoms = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Inferior']
    shoes = [p for p in st.session_state.armario if p.get('categoria') == 'Calzado']

    if not tops or not bottoms or not shoes:
        st.info("Agrega al menos una prenda de cada categoría para generar recomendaciones.")
    else:
        col_rec, col_3d_rec = st.columns([1.15, 1])
        with col_rec:
            if st.button("Generar Nueva Combinación 🎲") or 'outfit_3d' not in st.session_state:
                st.session_state.outfit_3d = {
                    "top": random.choice(tops),
                    "bottom": random.choice(bottoms),
                    "shoes": random.choice(shoes)
                }

            out = st.session_state.outfit_3d
            arm_top_bot = calcular_armonia_colores(out['top'].get('hex', '#FFF'), out['bottom'].get('hex', '#333'))

            st.markdown(f"""
            <div class="tarjeta-ropa">
                <h4>Combinación Sugerida</h4>
                <p>👕 <b>Top:</b> <span class="muestra-color" style="background:{out['top'].get('hex')};"></span> {out['top']['nombre']} (<i>{out['top']['color']}</i>)</p>
                <p>👖 <b>Pantalón:</b> <span class="muestra-color" style="background:{out['bottom'].get('hex')};"></span> {out['bottom']['nombre']} (<i>{out['bottom']['color']}</i>)</p>
                <p>👞 <b>Calzado:</b> <span class="muestra-color" style="background:{out['shoes'].get('hex')};"></span> {out['shoes']['nombre']} (<i>{out['shoes']['color']}</i>)</p>
                <hr>
                <p>🎨 <b>Armonía de Color:</b> {arm_top_bot}</p>
                <p>🌱 <i>Prendas que ya tienes. Gasto en ropa nueva: $0.00</i></p>
            </div>
            """, unsafe_allow_html=True)

        with col_3d_rec:
            renderizar_avatar_3d(out['top'], out['bottom'], out['shoes'], st.session_state.perfil)

        st.divider()
        st.subheader("📅 Plan de Outfits para la Semana")
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        agenda = []
        for d in dias:
            t = random.choice(tops)
            b = random.choice(bottoms)
            s = random.choice(shoes)
            agenda.append({
                "Día": d,
                "Parte Superior": f"{t['nombre']} ({t['color']})",
                "Parte Inferior": f"{b['nombre']} ({b['color']})",
                "Calzado": f"{s['nombre']} ({s['color']})",
                "Armonía": calcular_armonia_colores(t.get('hex', '#FFF'), b.get('hex', '#000'))
            })
        st.dataframe(pd.DataFrame(agenda), use_container_width=True, hide_index=True)

# --- TAB 6: ASISTENTE IA ---
with tabs[5]:
    st.header("🤖 Asistente de Estilo Sostenible")
    for m in st.session_state.mensajes_ia:
        with st.chat_message(m["rol"]):
            st.write(m["texto"])

    pregunta = st.chat_input("Escribe tu duda de estilo o combinación...")
    if pregunta:
        st.session_state.mensajes_ia.append({"rol": "user", "texto": pregunta})
        with st.chat_message("user"):
            st.write(pregunta)

        sug_top = random.choice(tops)['nombre'] if tops else "tu camisa favorita"
        sug_bot = random.choice(bottoms)['nombre'] if bottoms else "tus pantalones"
        resp = f"Para tu silueta ({st.session_state.perfil.get('cuerpo')}) te recomiendo combinar tu **{sug_top}** con **{sug_bot}**. Los tonos tierra y neutros de tu armario crean una combinación clásica sin gastar de más."
        
        st.session_state.mensajes_ia.append({"rol": "assistant", "texto": resp})
        with st.chat_message("assistant"):
            st.write(resp)

# --- TAB 7: IMPACTO AMBIENTAL ---
with tabs[6]:
    st.header("🌍 Tu Huella Positiva")
    tot_agua = sum(p.get('agua_l', 0) for p in st.session_state.armario)
    tot_co2 = sum(p.get('co2_kg', 0) for p in st.session_state.armario)
    tot_usos = sum(p.get('usos', 0) for p in st.session_state.armario)

    c1, c2, c3 = st.columns(3)
    c1.metric("💧 Agua Amortizada", f"{tot_agua:,} L", "Al no comprar ropa desechable")
    c2.metric("☁️ CO2 Evitado", f"{tot_co2:.1f} kg CO2", "Reutilizando tu clóset")
    c3.metric("🔄 Usos Totales", f"{tot_usos} puestas", "Vida útil extendida")

    st.divider()
    df_arm = pd.DataFrame(st.session_state.armario)
    st.bar_chart(df_arm.set_index("nombre")["usos"])
