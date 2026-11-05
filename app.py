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

# 2. CATÁLOGOS DE COLORES, DISEÑOS Y PIEL
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

DISENOS_POR_CATEGORIA = {
    "Parte Superior": [
        "Camisa (Cuello y Botones)",
        "Suéter / Chompa (Manga Larga)",
        "Polo / Blusa (Manga Corta)",
        "Blazer / Casaca (Con Solapa)"
    ],
    "Parte Inferior": [
        "Pantalón Sastre / Chino (Recto)",
        "Jeans / Denim (Con Bolsillos)",
        "Pantalón Ancho / Palazzo",
        "Bermuda / Falda Corta"
    ],
    "Calzado": [
        "Mocasines / Zapatos de Vestir",
        "Zapatillas Urbanas (Con Pasadores)",
        "Botines / Botas"
    ]
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

# Funciones auxiliares de color y diseño
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
    r, g, b = [x / 255.0 for x in hex_a_rgb(hex_str)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l_nuevo = max(0.05, min(0.95, l * factor_luz))
    r2, g2, b2 = colorsys.hls_to_rgb(h, l_nuevo, s)
    return rgb_a_hex((r2 * 255, g2 * 255, b2 * 255))

def inferir_diseno(nombre, categoria):
    n = str(nombre).lower()
    if categoria == "Parte Superior":
        if any(p in n for p in ["camisa", "blusa formal"]):
            return "Camisa (Cuello y Botones)"
        elif any(p in n for p in ["suéter", "sueter", "chompa", "tejido", "abrigo"]):
            return "Suéter / Chompa (Manga Larga)"
        elif any(p in n for p in ["blazer", "casaca", "chaqueta", "saco"]):
            return "Blazer / Casaca (Con Solapa)"
        return "Polo / Blusa (Manga Corta)"
    elif categoria == "Parte Inferior":
        if any(p in n for p in ["jean", "denim", "mezclilla"]):
            return "Jeans / Denim (Con Bolsillos)"
        elif any(p in n for p in ["ancho", "palazzo", "cargo", "holgado"]):
            return "Pantalón Ancho / Palazzo"
        elif any(p in n for p in ["bermuda", "short", "falda"]):
            return "Bermuda / Falda Corta"
        return "Pantalón Sastre / Chino (Recto)"
    else:
        if any(p in n for p in ["zapatilla", "sneaker", "lona", "deportiv"]):
            return "Zapatillas Urbanas (Con Pasadores)"
        elif any(p in n for p in ["botín", "botin", "bota"]):
            return "Botines / Botas"
        return "Mocasines / Zapatos de Vestir"

def calcular_armonia_colores(hex1, hex2):
    r1, g1, b1 = [x / 255.0 for x in hex_a_rgb(hex1)]
    r2, g2, b2 = [x / 255.0 for x in hex_a_rgb(hex2)]
    h1, l1, s1 = colorsys.rgb_to_hls(r1, g1, b1)
    h2, l2, s2 = colorsys.rgb_to_hls(r2, g2, b2)

    if s1 < 0.18 or s2 < 0.18 or l1 > 0.88 or l2 > 0.88 or l1 < 0.15 or l2 < 0.15:
        return "Armonía con Neutro Comodín (98% Compatible)"
    diff_hue = abs(h1 - h2) * 360
    if diff_hue > 180:
        diff_hue = 360 - diff_hue
    if diff_hue < 22:
        return "Armonía Monocromática — Estiliza tu altura (96% Compatible)"
    elif diff_hue < 58:
        return "Armonía Análoga Suave (93% Compatible)"
    elif 150 <= diff_hue <= 210:
        return "Contraste Complementario (91% Compatible)"
    return "Combinación Creativa Equilibrada (88% Compatible)"

def obtener_consejo_altura(altura_cm, genero):
    if altura_cm < 162:
        return (
            f"📏 **Estatura Baja ({altura_cm} cm):** Te favorecen los **looks monocromáticos** (tonos parecidos arriba y abajo) "
            "porque crean una línea vertical continua que alarga tus piernas. Prioriza **Camisas con cuello en V**, "
            "**Pantalones Sastre de tiro alto** y evita cortes muy anchos que resten altura."
        )
    elif altura_cm <= 175:
        return (
            f"📏 **Estatura Media ({altura_cm} cm):** Tienes una proporción muy versátil. Puedes alternar tanto **Blazers y Suéteres** "
            "como **Jeans o Pantalones Rectos**, jugando libremente con contrastes de color y superposición de prendas."
        )
    else:
        return (
            f"📏 **Estatura Alta ({altura_cm} cm):** Tu altura luce increíble con **bloques de color contrastantes** entre la parte "
            "superior e inferior (por ejemplo, tonos claros arriba y oscuros abajo). Te quedan muy bien los **Pantalones Anchos o Jeans**, "
            "**Blazers estructurados**, **Suéteres tejidos** y **Botines o Zapatillas**."
        )

# 3. AUTORREPARACIÓN DE SESIÓN
PERFIL_PREDETERMINADO = {
    "genero": "Femenino",
    "altura_cm": 165,
    "cuerpo": "Reloj de arena / Equilibrado",
    "tono_nombre": "Trigueño Claro",
    "piel_hex": "#E8B993",
    "subtono": "Cálido (Dorado / Melocotón)",
    "cabello_hex": "#3B2618"
}

if 'perfil' not in st.session_state:
    st.session_state.perfil = PERFIL_PREDETERMINADO.copy()
else:
    for k, v in PERFIL_PREDETERMINADO.items():
        if k not in st.session_state.perfil:
            st.session_state.perfil[k] = v

if 'armario' not in st.session_state:
    st.session_state.armario = [
        {"id": 1, "nombre": "Camisa de Lino Blanca", "categoria": "Parte Superior", "diseno": "Camisa (Cuello y Botones)", "color": "Blanco Hueso", "hex": "#F2EFE9", "material": "Lino", "usos": 12, "agua_l": 2500, "co2_kg": 5.0},
        {"id": 2, "nombre": "Suéter Tejido Camel", "categoria": "Parte Superior", "diseno": "Suéter / Chompa (Manga Larga)", "color": "Camel", "hex": "#C19A6B", "material": "Lana", "usos": 8, "agua_l": 3200, "co2_kg": 7.5},
        {"id": 3, "nombre": "Polo Básico Verde Salvia", "categoria": "Parte Superior", "diseno": "Polo / Blusa (Manga Corta)", "color": "Verde Salvia", "hex": "#9CAF88", "material": "Algodón", "usos": 10, "agua_l": 2200, "co2_kg": 4.5},
        {"id": 4, "nombre": "Blazer Estructurado Topo", "categoria": "Parte Superior", "diseno": "Blazer / Casaca (Con Solapa)", "color": "Topo / Taupe", "hex": "#8B7D70", "material": "Algodón/Lino", "usos": 7, "agua_l": 3800, "co2_kg": 8.5},
        {"id": 5, "nombre": "Pantalón Chino Marrón", "categoria": "Parte Inferior", "diseno": "Pantalón Sastre / Chino (Recto)", "color": "Marrón Café", "hex": "#6F4E37", "material": "Algodón", "usos": 15, "agua_l": 6000, "co2_kg": 12.0},
        {"id": 6, "nombre": "Jeans Clásicos Azules", "categoria": "Parte Inferior", "diseno": "Jeans / Denim (Con Bolsillos)", "color": "Azul Marino", "hex": "#1D2951", "material": "Denim", "usos": 25, "agua_l": 8500, "co2_kg": 18.0},
        {"id": 7, "nombre": "Pantalón Holgado Arena", "categoria": "Parte Inferior", "diseno": "Pantalón Ancho / Palazzo", "color": "Beige Arena", "hex": "#E1D4BC", "material": "Lino", "usos": 11, "agua_l": 5000, "co2_kg": 10.5},
        {"id": 8, "nombre": "Mocasines de Cuero", "categoria": "Calzado", "diseno": "Mocasines / Zapatos de Vestir", "color": "Marrón Chocolate", "hex": "#4B3020", "material": "Cuero", "usos": 30, "agua_l": 7000, "co2_kg": 14.0},
        {"id": 9, "nombre": "Zapatillas de Lona", "categoria": "Calzado", "diseno": "Zapatillas Urbanas (Con Pasadores)", "color": "Crema", "hex": "#F5EEDC", "material": "Lona", "usos": 18, "agua_l": 2800, "co2_kg": 6.0},
        {"id": 10, "nombre": "Botines Terracota", "categoria": "Calzado", "diseno": "Botines / Botas", "color": "Terracota", "hex": "#B4553C", "material": "Cuero Vegano", "usos": 14, "agua_l": 4500, "co2_kg": 9.5},
    ]
else:
    for prenda in st.session_state.armario:
        if "hex" not in prenda:
            prenda["hex"] = CATALOGO_COLORES.get(prenda.get("color", "Camel"), "#C19A6B")
        if "material" not in prenda:
            prenda["material"] = "Algodón"
        if "diseno" not in prenda:
            prenda["diseno"] = inferir_diseno(prenda.get("nombre", ""), prenda.get("categoria", "Parte Superior"))

if 'mensajes_ia' not in st.session_state:
    st.session_state.mensajes_ia = [
        {"rol": "assistant", "texto": "¡Hola! Soy tu estilista 3D de EcoArmario. Ahora tomo en cuenta tu género, tu altura en centímetros, tu silueta y el diseño de cada prenda. ¿Qué combinación quieres probar hoy?"}
    ]

# 4. BARRA LATERAL Y ACCESIBILIDAD
st.sidebar.title("🌿 EcoArmario 3D")
st.sidebar.markdown("*Viste elegante, cuida el planeta.*")
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

# 5. MOTOR DE AVATAR 3D CON ROTACIÓN 360°, GÉNERO, ALTURA Y DISEÑOS DE ROPA
def renderizar_avatar_3d(top_prenda, bottom_prenda, shoes_prenda, perfil, id_unico="av1", altura_px=600):
    genero = perfil.get("genero", "Femenino")
    altura_cm = int(perfil.get("altura_cm", 165))
    cuerpo = perfil.get("cuerpo", "Reloj de arena / Equilibrado")
    tono_nombre = perfil.get("tono_nombre", "Trigueño Claro")
    piel_hex = perfil.get("piel_hex", "#E8B993")
    subtono = perfil.get("subtono", "Cálido (Dorado / Melocotón)")
    cabello_hex = perfil.get("cabello_hex", "#3B2618")

    # Escala vertical proporcional a la estatura (140 cm a 200 cm)
    escala_altura = 0.88 + ((altura_cm - 140) / 60.0) * 0.18
    escala_altura = max(0.86, min(1.06, escala_altura))

    # Proporciones anatómicas según Género + Tipo de Cuerpo
    es_masc = (genero == "Masculino")
    if "Reloj de arena" in cuerpo:
        sh_w, ch_w, wa_w, hi_w = (62, 54, 44, 50) if es_masc else (54, 48, 33, 55)
    elif "Pera" in cuerpo:
        sh_w, ch_w, wa_w, hi_w = (50, 48, 44, 58) if es_masc else (44, 41, 35, 63)
    elif "Invertido" in cuerpo:
        sh_w, ch_w, wa_w, hi_w = (68, 58, 43, 44) if es_masc else (62, 52, 39, 43)
    elif "Rectángulo" in cuerpo:
        sh_w, ch_w, wa_w, hi_w = (58, 53, 50, 50) if es_masc else (50, 45, 43, 47)
    else:  # Ovalado / Manzana
        sh_w, ch_w, wa_w, hi_w = (58, 60, 62, 54) if es_masc else (52, 55, 58, 53)

    # Matiz de piel
    r_p, g_p, b_p = hex_a_rgb(piel_hex)
    if "Cálido" in subtono:
        piel_base = rgb_a_hex((r_p + 6, g_p + 2, b_p - 5))
    elif "Frío" in subtono:
        piel_base = rgb_a_hex((r_p + 3, g_p - 2, b_p + 6))
    else:
        piel_base = piel_hex

    piel_luz = ajustar_luz_color(piel_base, 1.18)
    piel_sombra = ajustar_luz_color(piel_base, 0.78)
    piel_oscura = ajustar_luz_color(piel_base, 0.60)

    cabello_luz = ajustar_luz_color(cabello_hex, 1.35)
    cabello_sombra = ajustar_luz_color(cabello_hex, 0.65)

    # Colores e iluminación 3D de las prendas
    top_hex = top_prenda.get("hex", "#C19A6B")
    top_luz = ajustar_luz_color(top_hex, 1.22)
    top_sombra = ajustar_luz_color(top_hex, 0.70)
    top_diseno = top_prenda.get("diseno", inferir_diseno(top_prenda.get("nombre", ""), "Parte Superior"))

    bot_hex = bottom_prenda.get("hex", "#6F4E37")
    bot_luz = ajustar_luz_color(bot_hex, 1.20)
    bot_sombra = ajustar_luz_color(bot_hex, 0.68)
    bot_diseno = bottom_prenda.get("diseno", inferir_diseno(bottom_prenda.get("nombre", ""), "Parte Inferior"))

    sho_hex = shoes_prenda.get("hex", "#4B3020")
    sho_luz = ajustar_luz_color(sho_hex, 1.25)
    sho_sombra = ajustar_luz_color(sho_hex, 0.60)
    sho_diseno = shoes_prenda.get("diseno", inferir_diseno(shoes_prenda.get("nombre", ""), "Calzado"))

    cx = 200

    # --- GEOMETRÍA SEGÚN GÉNERO ---
    ancho_cuello = 20 if es_masc else 15
    rostro_path = (
        "M 157 82 C 157 50, 243 50, 243 82 C 243 114, 232 140, 200 145 C 168 140, 157 114, 157 82 Z"
        if es_masc else
        "M 160 84 C 160 52, 240 52, 240 84 C 240 116, 223 142, 200 145 C 177 142, 160 116, 160 84 Z"
    )
    cabello_trasero_frente = (
        f'<path d="M 154 78 C 150 96, 154 115, 160 122 L 240 122 C 246 115, 250 96, 246 78 Z" fill="url(#gradCabello_{id_unico})"/>'
        if es_masc else
        f'<path d="M 146 82 C 136 128, 142 172, 158 182 L 242 182 C 258 172, 264 128, 254 82 Z" fill="url(#gradCabello_{id_unico})"/>'
    )
    cabello_delantero = (
        f'<path d="M 154 88 C 150 52, 176 38, 200 39 C 226 39, 250 52, 246 88 C 238 66, 220 58, 200 59 C 180 58, 162 66, 154 88 Z" fill="url(#gradCabello_{id_unico})"/>'
        if es_masc else
        f'<path d="M 152 95 C 146 54, 176 38, 204 40 C 232 40, 254 58, 248 95 C 238 70, 220 62, 200 64 C 178 64, 162 74, 152 95 Z" fill="url(#gradCabello_{id_unico})"/>'
    )
    cabello_espalda = (
        f'<path d="M 154 68 C 152 42, 248 42, 246 68 C 248 98, 240 125, 200 128 C 160 125, 152 98, 154 68 Z" fill="url(#gradCabello_{id_unico})"/>'
        if es_masc else
        f'<path d="M 146 78 C 146 42, 254 42, 254 78 C 262 128, 252 178, 232 186 Q 200 194 168 186 C 148 178, 138 128, 146 78 Z" fill="url(#gradCabello_{id_unico})"/>'
    )
    labios_svg = (
        f'<path d="M 189 125 Q 200 129 211 125" stroke="{piel_oscura}" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
        if es_masc else
        '<path d="M 188 124 Q 200 131 212 124 Q 200 134 188 124 Z" fill="#C96F69"/>'
    )

    # --- GEOMETRÍA SEGÚN DISEÑO DE PRENDA SUPERIOR ---
    torso_base = f"""
        M {cx - sh_w} 162 Q {cx} 152 {cx + sh_w} 162
        C {cx + sh_w + 4} 195, {cx + ch_w} 215, {cx + wa_w} 245
        C {cx + wa_w + 4} 265, {cx + hi_w} 275, {cx + hi_w} 294
        Q {cx} 304 {cx - hi_w} 294
        C {cx - hi_w} 275, {cx - wa_w - 4} 265, {cx - wa_w} 245
        C {cx - ch_w} 215, {cx - sh_w - 4} 195, {cx - sh_w} 162 Z
    """

    if "Suéter" in top_diseno:
        # Manga larga hasta las muñecas y cuello redondo alto tejido
        mangas_svg = f"""
            <path d="M {cx - sh_w + 2} 162 C {cx - sh_w - 20} 210, {cx - sh_w - 22} 255, {cx - sh_w - 16} 302 L {cx - sh_w - 1} 302 C {cx - sh_w - 4} 255, {cx - sh_w - 2} 215, {cx - ch_w + 4} 192 Z" fill="url(#gradTop_{id_unico})"/>
            <path d="M {cx + sh_w - 2} 162 C {cx + sh_w + 20} 210, {cx + sh_w + 22} 255, {cx + sh_w + 16} 302 L {cx + sh_w + 1} 302 C {cx + sh_w + 4} 255, {cx + sh_w + 2} 215, {cx + ch_w - 4} 192 Z" fill="url(#gradTop_{id_unico})"/>
        """
        detalles_top_frente = f"""
            <path d="M 178 156 Q 200 168 222 156 Q 200 162 178 156 Z" fill="{top_sombra}" stroke="{top_sombra}" stroke-width="4"/>
            <line x1="{cx - 25}" y1="175" x2="{cx - 25}" y2="290" stroke="{top_sombra}" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.45"/>
            <line x1="{cx}" y1="170" x2="{cx}" y2="295" stroke="{top_sombra}" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.45"/>
            <line x1="{cx + 25}" y1="175" x2="{cx + 25}" y2="290" stroke="{top_sombra}" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.45"/>
        """
    elif "Camisa" in top_diseno:
        # Manga media/larga con puño, cuello formal y hilera de botones
        mangas_svg = f"""
            <path d="M {cx - sh_w + 2} 162 C {cx - sh_w - 19} 200, {cx - sh_w - 21} 245, {cx - sh_w - 17} 275 L {cx - sh_w - 1} 275 L {cx - ch_w + 4} 192 Z" fill="url(#gradTop_{id_unico})"/>
            <path d="M {cx + sh_w - 2} 162 C {cx + sh_w + 19} 200, {cx + sh_w + 21} 245, {cx + sh_w + 17} 275 L {cx + sh_w + 1} 275 L {cx + ch_w - 4} 192 Z" fill="url(#gradTop_{id_unico})"/>
        """
        detalles_top_frente = f"""
            <path d="M 182 156 L 200 182 L 218 156 Z" fill="{piel_base}"/>
            <polygon points="175,154 198,178 184,186 168,164" fill="{top_luz}" stroke="{top_sombra}" stroke-width="1.5"/>
            <polygon points="225,154 202,178 216,186 232,164" fill="{top_luz}" stroke="{top_sombra}" stroke-width="1.5"/>
            <line x1="200" y1="180" x2="200" y2="296" stroke="{top_sombra}" stroke-width="3"/>
            <circle cx="200" cy="198" r="2.5" fill="{top_luz}" stroke="{top_sombra}" stroke-width="1"/>
            <circle cx="200" cy="222" r="2.5" fill="{top_luz}" stroke="{top_sombra}" stroke-width="1"/>
            <circle cx="200" cy="246" r="2.5" fill="{top_luz}" stroke="{top_sombra}" stroke-width="1"/>
            <circle cx="200" cy="270" r="2.5" fill="{top_luz}" stroke="{top_sombra}" stroke-width="1"/>
        """
    elif "Blazer" in top_diseno:
        # Casaca/Blazer abierto con camiseta blanca interior y solapas
        mangas_svg = f"""
            <path d="M {cx - sh_w + 2} 162 C {cx - sh_w - 20} 210, {cx - sh_w - 22} 255, {cx - sh_w - 16} 298 L {cx - sh_w - 1} 298 L {cx - ch_w + 4} 192 Z" fill="url(#gradTop_{id_unico})"/>
            <path d="M {cx + sh_w - 2} 162 C {cx + sh_w + 20} 210, {cx + sh_w + 22} 255, {cx + sh_w + 16} 298 L {cx + sh_w + 1} 298 L {cx + ch_w - 4} 192 Z" fill="url(#gradTop_{id_unico})"/>
        """
        detalles_top_frente = f"""
            <path d="M 184 160 L 216 160 L 214 294 L 186 294 Z" fill="#F7F5F0"/>
            <polygon points="176,156 188,245 198,245 186,160" fill="{top_sombra}"/>
            <polygon points="224,156 212,245 202,245 214,160" fill="{top_sombra}"/>
            <rect x="{cx - hi_w + 14}" y="258" width="22" height="5" rx="2" fill="{top_sombra}"/>
            <rect x="{cx + hi_w - 36}" y="258" width="22" height="5" rx="2" fill="{top_sombra}"/>
        """
    else:
        # Polo / Blusa manga corta
        mangas_svg = f"""
            <path d="M {cx - sh_w + 2} 162 C {cx - sh_w - 16} 185, {cx - sh_w - 18} 215, {cx - sh_w - 18} 228 L {cx - sh_w - 2} 232 L {cx - ch_w + 4} 195 Z" fill="url(#gradTop_{id_unico})"/>
            <path d="M {cx + sh_w - 2} 162 C {cx + sh_w + 16} 185, {cx + sh_w + 18} 215, {cx + sh_w + 18} 228 L {cx + sh_w + 2} 232 L {cx + ch_w - 4} 195 Z" fill="url(#gradTop_{id_unico})"/>
        """
        detalles_top_frente = f"""
            <path d="M 180 158 L 200 184 L 220 158" fill="{piel_base}" stroke="{top_sombra}" stroke-width="2.5"/>
        """

    # --- GEOMETRÍA SEGÚN DISEÑO DE PRENDA INFERIOR ---
    if "Ancho" in bot_diseno:
        p_izq = f"M {cx - hi_w} 288 L {cx + 2} 294 L {cx - 3} 345 L {cx - 8} 468 L {cx - 58} 468 C {cx - 58} 410, {cx - hi_w - 6} 350, {cx - hi_w} 288 Z"
        p_der = f"M {cx - 2} 294 L {cx + hi_w} 288 C {cx + hi_w + 6} 350, {cx + 58} 410, {cx + 58} 468 L {cx + 8} 468 L {cx + 3} 345 Z"
        piernas_piel_svg = ""
        detalles_bot_frente = f'<line x1="{cx - 32}" y1="305" x2="{cx - 35}" y2="465" stroke="{bot_sombra}" stroke-width="1.5" opacity="0.4"/><line x1="{cx + 32}" y1="305" x2="{cx + 35}" y2="465" stroke="{bot_sombra}" stroke-width="1.5" opacity="0.4"/>'
        detalles_bot_espalda = ""
    elif "Bermuda" in bot_diseno:
        p_izq = f"M {cx - hi_w} 288 L {cx + 2} 294 L {cx - 4} 382 L {cx - 48} 382 C {cx - 48} 345, {cx - hi_w - 2} 315, {cx - hi_w} 288 Z"
        p_der = f"M {cx - 2} 294 L {cx + hi_w} 288 C {cx + hi_w + 2} 315, {cx + 48} 345, {cx + 48} 382 L {cx + 4} 382 Z"
        piernas_piel_svg = f"""
            <rect x="{cx - 38}" y="378" width="22" height="92" rx="8" fill="url(#gradPielCilindro_{id_unico})"/>
            <rect x="{cx + 16}" y="378" width="22" height="92" rx="8" fill="url(#gradPielCilindro_{id_unico})"/>
        """
        detalles_bot_frente = f'<line x1="{cx - hi_w}" y1="378" x2="{cx + hi_w}" y2="378" stroke="{bot_luz}" stroke-width="2" opacity="0.5"/>'
        detalles_bot_espalda = ""
    elif "Jeans" in bot_diseno:
        p_izq = f"M {cx - hi_w} 288 L {cx + 2} 294 L {cx - 4} 345 C {cx - 6} 390, {cx - 14} 435, {cx - 18} 468 L {cx - 44} 468 C {cx - 46} 425, {cx - hi_w - 4} 355, {cx - hi_w} 288 Z"
        p_der = f"M {cx - 2} 294 L {cx + hi_w} 288 C {cx + hi_w + 4} 355, {cx + 46} 425, {cx + 44} 468 L {cx + 18} 468 C {cx + 14} 435, {cx + 6} 390, {cx + 4} 345 Z"
        piernas_piel_svg = ""
        detalles_bot_frente = f"""
            <path d="M {cx - hi_w + 4} 302 Q {cx - hi_w + 22} 318 {cx - hi_w + 26} 296" fill="none" stroke="#D4AF37" stroke-width="1.8" stroke-dasharray="2,2"/>
            <path d="M {cx + hi_w - 4} 302 Q {cx + hi_w - 22} 318 {cx + hi_w - 26} 296" fill="none" stroke="#D4AF37" stroke-width="1.8" stroke-dasharray="2,2"/>
            <line x1="{cx}" y1="294" x2="{cx}" y2="338" stroke="#D4AF37" stroke-width="2" stroke-dasharray="3,2"/>
            <circle cx="{cx}" cy="298" r="3" fill="#D4AF37"/>
        """
        detalles_bot_espalda = f"""
            <polygon points="{cx-38},308 {cx-14},308 {cx-14},330 {cx-26},338 {cx-38},330" fill="{bot_sombra}" stroke="#D4AF37" stroke-width="1.5" stroke-dasharray="2,2"/>
            <polygon points="{cx+14},308 {cx+38},308 {cx+38},330 {cx+26},338 {cx+14},330" fill="{bot_sombra}" stroke="#D4AF37" stroke-width="1.5" stroke-dasharray="2,2"/>
        """
    else:
        # Pantalón Sastre / Chino recto
        p_izq = f"M {cx - hi_w} 288 L {cx + 2} 294 L {cx - 4} 345 C {cx - 6} 390, {cx - 14} 435, {cx - 18} 468 L {cx - 44} 468 C {cx - 46} 425, {cx - hi_w - 4} 355, {cx - hi_w} 288 Z"
        p_der = f"M {cx - 2} 294 L {cx + hi_w} 288 C {cx + hi_w + 4} 355, {cx + 46} 425, {cx + 44} 468 L {cx + 18} 468 C {cx + 14} 435, {cx + 6} 390, {cx + 4} 345 Z"
        piernas_piel_svg = ""
        detalles_bot_frente = f"""
            <line x1="{cx - 30}" y1="305" x2="{cx - 31}" y2="465" stroke="{bot_luz}" stroke-width="2.5" opacity="0.45"/>
            <line x1="{cx + 30}" y1="305" x2="{cx + 31}" y2="465" stroke="{bot_luz}" stroke-width="2.5" opacity="0.45"/>
            <rect x="{cx - hi_w + 2}" y="288" width="{hi_w * 2 - 4}" height="8" rx="2" fill="{bot_sombra}"/>
        """
        detalles_bot_espalda = f"""
            <line x1="{cx - 36}" y1="312" x2="{cx - 16}" y2="312" stroke="{bot_sombra}" stroke-width="2.5"/>
            <line x1="{cx + 16}" y1="312" x2="{cx + 36}" y2="312" stroke="{bot_sombra}" stroke-width="2.5"/>
        """

    # --- GEOMETRÍA SEGÚN DISEÑO DE CALZADO ---
    if "Zapatillas" in sho_diseno:
        calzado_svg = f"""
            <path d="M {cx - 46} 464 C {cx - 54} 476, {cx - 52} 488, {cx - 32} 490 L {cx - 14} 490 C {cx - 12} 480, {cx - 14} 468, {cx - 18} 464 Z" fill="url(#gradZap_{id_unico})"/>
            <rect x="{cx - 52}" y="484" width="40" height="7" rx="3.5" fill="#FFFFFF" stroke="#CCCCCC" stroke-width="1"/>
            <line x1="{cx - 38}" y1="470" x2="{cx - 24}" y2="470" stroke="#FFFFFF" stroke-width="2"/>
            <line x1="{cx - 40}" y1="475" x2="{cx - 22}" y2="475" stroke="#FFFFFF" stroke-width="2"/>

            <path d="M {cx + 18} 464 C {cx + 14} 468, {cx + 12} 480, {cx + 14} 490 L {cx + 32} 490 C {cx + 52} 488, {cx + 54} 476, {cx + 46} 464 Z" fill="url(#gradZap_{id_unico})"/>
            <rect x="{cx + 12}" y="484" width="40" height="7" rx="3.5" fill="#FFFFFF" stroke="#CCCCCC" stroke-width="1"/>
            <line x1="{cx + 24}" y1="470" x2="{cx + 38}" y2="470" stroke="#FFFFFF" stroke-width="2"/>
            <line x1="{cx + 22}" y1="475" x2="{cx + 40}" y2="475" stroke="#FFFFFF" stroke-width="2"/>
        """
    elif "Botines" in sho_diseno:
        calzado_svg = f"""
            <path d="M {cx - 44} 446 L {cx - 18} 446 L {cx - 14} 488 L {cx - 50} 488 C {cx - 52} 475, {cx - 46} 462, {cx - 44} 446 Z" fill="url(#gradZap_{id_unico})"/>
            <rect x="{cx - 51}" y="485" width="38" height="6" rx="2" fill="#2B1B12"/>
            <path d="M {cx + 18} 446 L {cx + 44} 446 C {cx + 46} 462, {cx + 52} 475, {cx + 50} 488 L {cx + 14} 488 Z" fill="url(#gradZap_{id_unico})"/>
            <rect x="{cx + 13}" y="485" width="38" height="6" rx="2" fill="#2B1B12"/>
        """
    else:
        # Mocasines / Zapatos de vestir
        calzado_svg = f"""
            <path d="M {cx - 46} 465 C {cx - 52} 478, {cx - 50} 488, {cx - 32} 490 L {cx - 14} 490 C {cx - 12} 482, {cx - 14} 470, {cx - 18} 465 Z" fill="url(#gradZap_{id_unico})"/>
            <rect x="{cx - 40}" y="472" width="16" height="4" rx="1" fill="#D4AF37"/>
            <rect x="{cx - 50}" y="486" width="37" height="4" rx="2" fill="#2A1B12"/>

            <path d="M {cx + 18} 465 C {cx + 14} 470, {cx + 12} 482, {cx + 14} 490 L {cx + 32} 490 C {cx + 50} 488, {cx + 52} 478, {cx + 46} 465 Z" fill="url(#gradZap_{id_unico})"/>
            <rect x="{cx + 24}" y="472" width="16" height="4" rx="1" fill="#D4AF37"/>
            <rect x="{cx + 13}" y="486" width="37" height="4" rx="2" fill="#2A1B12"/>
        """

    # Posición del marcador en la regla de altura (140 cm a 200 cm)
    y_marcador_altura = int(460 - ((altura_cm - 140) / 60.0) * 380)
    y_marcador_altura = max(55, min(465, y_marcador_altura))

    html_3d = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0; padding: 0; background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex; flex-direction: column; align-items: center;
            user-select: none;
        }}
        .escena-3d {{
            width: 405px; height: 575px;
            background: radial-gradient(circle at 50% 35%, #FFFDF9 0%, #EFE6D5 65%, #DFCFB5 100%);
            border-radius: 22px;
            box-shadow: inset 0 0 35px rgba(90,60,35,0.14), 0 10px 24px rgba(0,0,0,0.09);
            border: 2px solid #D5C3AE;
            position: relative; overflow: hidden;
            cursor: grab;
        }}
        .escena-3d:active {{ cursor: grabbing; }}

        /* Separamos la animación de respiración del contenedor de rotación para que NUNCA bloquee el giro */
        .animacion-respirar {{
            width: 100%; height: 100%;
            animation: respirar 3.6s ease-in-out infinite;
        }}
        @keyframes respirar {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-4px); }}
        }}
        @keyframes parpadear {{
            0%, 94%, 98%, 100% {{ transform: scaleY(1); }}
            96% {{ transform: scaleY(0.1); }}
        }}
        .ojos {{
            transform-origin: 200px 101px;
            animation: parpadear 4.2s infinite;
        }}
        .etiqueta-sup {{
            position: absolute; top: 10px; left: 12px; right: 12px;
            display: flex; justify-content: space-between; align-items: center;
            pointer-events: none; z-index: 10;
        }}
        .badge {{
            background: rgba(60, 40, 25, 0.85); color: #FFF;
            padding: 5px 11px; border-radius: 14px; font-size: 11px; font-weight: 600;
        }}
        .controles-3d {{
            position: absolute; bottom: 10px; left: 12px; right: 12px;
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(5px);
            border-radius: 12px; padding: 8px 12px;
            display: flex; flex-direction: column; gap: 5px;
            font-size: 12px; color: #3B281E; font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            z-index: 10;
        }}
        .fila-ctrl {{
            display: flex; justify-content: space-between; align-items: center; gap: 8px;
        }}
        .btn-giro {{
            background: #8A5A36; color: white; border: none; border-radius: 6px;
            padding: 4px 10px; font-size: 11px; font-weight: 600; cursor: pointer;
        }}
        .btn-giro:hover {{ opacity: 0.9; }}
        input[type=range] {{ accent-color: #8A5A36; flex: 1; cursor: pointer; }}
    </style>
    </head>
    <body>
    <div class="escena-3d" id="escena_{id_unico}">
        <div class="etiqueta-sup">
            <span class="badge">🚻 {genero} | 📏 {altura_cm} cm</span>
            <span class="badge" id="badgeVista_{id_unico}">Vista: Frontal (0°)</span>
        </div>

        <div class="animacion-respirar">
            <svg viewBox="0 0 400 545" width="100%" height="100%">
                <defs>
                    <filter id="sombra_{id_unico}" x="-15%" y="-15%" width="130%" height="130%">
                        <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#2A1B12" flood-opacity="0.25"/>
                    </filter>
                    <radialGradient id="gradCara_{id_unico}" cx="42%" cy="35%" r="60%">
                        <stop offset="0%" stop-color="{piel_luz}"/>
                        <stop offset="55%" stop-color="{piel_base}"/>
                        <stop offset="100%" stop-color="{piel_sombra}"/>
                    </radialGradient>
                    <linearGradient id="gradPielCilindro_{id_unico}" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="{piel_sombra}"/>
                        <stop offset="35%" stop-color="{piel_luz}"/>
                        <stop offset="70%" stop-color="{piel_base}"/>
                        <stop offset="100%" stop-color="{piel_oscura}"/>
                    </linearGradient>
                    <linearGradient id="gradCabello_{id_unico}" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="{cabello_sombra}"/>
                        <stop offset="35%" stop-color="{cabello_hex}"/>
                        <stop offset="52%" stop-color="{cabello_luz}"/>
                        <stop offset="75%" stop-color="{cabello_hex}"/>
                        <stop offset="100%" stop-color="{cabello_sombra}"/>
                    </linearGradient>
                    <linearGradient id="gradTop_{id_unico}" x1="0%" y1="0%" x2="100%" y2="20%">
                        <stop offset="0%" stop-color="{top_sombra}"/>
                        <stop offset="30%" stop-color="{top_luz}"/>
                        <stop offset="65%" stop-color="{top_hex}"/>
                        <stop offset="100%" stop-color="{top_sombra}"/>
                    </linearGradient>
                    <linearGradient id="gradBot_{id_unico}" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="{bot_sombra}"/>
                        <stop offset="30%" stop-color="{bot_luz}"/>
                        <stop offset="65%" stop-color="{bot_hex}"/>
                        <stop offset="100%" stop-color="{bot_sombra}"/>
                    </linearGradient>
                    <radialGradient id="gradZap_{id_unico}" cx="38%" cy="30%" r="70%">
                        <stop offset="0%" stop-color="{sho_luz}"/>
                        <stop offset="55%" stop-color="{sho_hex}"/>
                        <stop offset="100%" stop-color="{sho_sombra}"/>
                    </radialGradient>
                </defs>

                <!-- Regla Medidora de Estatura 3D a la izquierda -->
                <g opacity="0.65">
                    <line x1="28" y1="60" x2="28" y2="480" stroke="#6E5036" stroke-width="2"/>
                    <line x1="22" y1="80" x2="34" y2="80" stroke="#6E5036" stroke-width="1.5"/>
                    <text x="38" y="84" font-size="9" fill="#5A3E28">200cm</text>
                    <line x1="22" y1="205" x2="34" y2="205" stroke="#6E5036" stroke-width="1.5"/>
                    <text x="38" y="209" font-size="9" fill="#5A3E28">180cm</text>
                    <line x1="22" y1="330" x2="34" y2="330" stroke="#6E5036" stroke-width="1.5"/>
                    <text x="38" y="334" font-size="9" fill="#5A3E28">160cm</text>
                    <line x1="22" y1="455" x2="34" y2="455" stroke="#6E5036" stroke-width="1.5"/>
                    <text x="38" y="459" font-size="9" fill="#5A3E28">140cm</text>
                    <!-- Indicador de la altura actual -->
                    <polygon points="18,{y_marcador_altura} 34,{y_marcador_altura-5} 34,{y_marcador_altura+5}" fill="#8A5A36"/>
                </g>

                <!-- Plataforma Circular 3D -->
                <ellipse cx="200" cy="485" rx="92" ry="18" fill="#C8B59E" opacity="0.65"/>
                <ellipse cx="200" cy="482" rx="72" ry="13" fill="#3D2B1F" opacity="0.26"/>

                <!-- GRUPO DEL AVATAR CON ESCALA DE ALTURA Y GIRO 360 -->
                <g id="grupoEscala_{id_unico}" transform="translate(200, 485) scale(1, {escala_altura}) translate(-200, -485)">
                    <g id="grupoGiro_{id_unico}">
                        <!-- Cabello Posterior -->
                        {cabello_trasero_frente}

                        <!-- Cuello -->
                        <path d="M {200 - ancho_cuello} 130 L {200 - ancho_cuello - 2} 168 L {200 + ancho_cuello + 2} 168 L {200 + ancho_cuello} 130 Z" fill="url(#gradPielCilindro_{id_unico})"/>

                        <!-- Brazos y Manos -->
                        <path d="M {cx - sh_w + 4} 166 C {cx - sh_w - 20} 215, {cx - sh_w - 22} 260, {cx - sh_w - 16} 305 L {cx - sh_w - 2} 305 C {cx - sh_w - 6} 260, {cx - sh_w - 4} 220, {cx - sh_w + 14} 178 Z" fill="url(#gradPielCilindro_{id_unico})"/>
                        <path d="M {cx + sh_w - 4} 166 C {cx + sh_w + 20} 215, {cx + sh_w + 22} 260, {cx + sh_w + 16} 305 L {cx + sh_w + 2} 305 C {cx + sh_w + 6} 260, {cx + sh_w + 4} 220, {cx + sh_w - 14} 178 Z" fill="url(#gradPielCilindro_{id_unico})"/>
                        <ellipse cx="{cx - sh_w - 9}" cy="312" rx="8" ry="11" fill="url(#gradCara_{id_unico})"/>
                        <ellipse cx="{cx + sh_w + 9}" cy="312" rx="8" ry="11" fill="url(#gradCara_{id_unico})"/>

                        <!-- Piernas visibles (si usa bermuda o falda) -->
                        {piernas_piel_svg}

                        <!-- PARTE INFERIOR (Pantalón / Jeans / Palazzo / Bermuda) -->
                        <g filter="url(#sombra_{id_unico})">
                            <path d="{p_izq}" fill="url(#gradBot_{id_unico})"/>
                            <path d="{p_der}" fill="url(#gradBot_{id_unico})"/>
                            <g id="detallesBotFrente_{id_unico}">{detalles_bot_frente}</g>
                            <g id="detallesBotEspalda_{id_unico}" style="display:none;">{detalles_bot_espalda}</g>
                        </g>

                        <!-- PARTE SUPERIOR (Camisa / Suéter / Polo / Blazer) -->
                        <g filter="url(#sombra_{id_unico})">
                            {mangas_svg}
                            <path d="{torso_base}" fill="url(#gradTop_{id_unico})"/>
                            <g id="detallesTopFrente_{id_unico}">{detalles_top_frente}</g>
                            <g id="detallesTopEspalda_{id_unico}" style="display:none;">
                                <line x1="200" y1="160" x2="200" y2="292" stroke="{top_sombra}" stroke-width="1.5" opacity="0.45"/>
                            </g>
                        </g>

                        <!-- CALZADO (Mocasines / Zapatillas / Botines) -->
                        <g filter="url(#sombra_{id_unico})">
                            {calzado_svg}
                        </g>

                        <!-- CABEZA (Rostro Frontal vs Cabello de Espalda) -->
                        <g id="cabezaParallax_{id_unico}" filter="url(#sombra_{id_unico})">
                            <ellipse cx="155" cy="104" rx="6" ry="10" fill="{piel_sombra}"/>
                            <ellipse cx="245" cy="104" rx="6" ry="10" fill="{piel_sombra}"/>
                            <path d="{rostro_path}" fill="url(#gradCara_{id_unico})"/>

                            <!-- Facciones del Rostro (Se ocultan cuando gira de espaldas) -->
                            <g id="rostroFrente_{id_unico}">
                                <g class="ojos">
                                    <ellipse cx="181" cy="101" rx="8" ry="5.5" fill="#FFF"/>
                                    <circle cx="181" cy="101" r="4.2" fill="#3E2723"/>
                                    <circle cx="182.5" cy="99.5" r="1.5" fill="#FFF"/>
                                    <path d="M 172 99 Q 181 93 190 100" stroke="#221510" stroke-width="{2.5 if not es_masc else 1.8}" fill="none"/>

                                    <ellipse cx="219" cy="101" rx="8" ry="5.5" fill="#FFF"/>
                                    <circle cx="219" cy="101" r="4.2" fill="#3E2723"/>
                                    <circle cx="220.5" cy="99.5" r="1.5" fill="#FFF"/>
                                    <path d="M 210 100 Q 219 93 228 99" stroke="#221510" stroke-width="{2.5 if not es_masc else 1.8}" fill="none"/>
                                </g>
                                <path d="M 171 90 Q 181 85 191 89" stroke="{cabello_sombra}" stroke-width="{3.4 if es_masc else 2.4}" stroke-linecap="round" fill="none"/>
                                <path d="M 209 89 Q 219 85 229 90" stroke="{cabello_sombra}" stroke-width="{3.4 if es_masc else 2.4}" stroke-linecap="round" fill="none"/>
                                <path d="M 199 97 L 197 112 Q 200 115 203 112" stroke="{piel_oscura}" stroke-width="1.8" fill="none"/>
                                {labios_svg}
                                {cabello_delantero}
                            </g>

                            <!-- Cabello de Espalda (Se muestra al girar más de 90°) -->
                            <g id="cabezaEspalda_{id_unico}" style="display:none;">
                                {cabello_espalda}
                            </g>
                        </g>
                    </g>
                </g>
            </svg>
        </div>

        <div class="controles-3d">
            <div class="fila-ctrl">
                <span>🔄 Giro 360°:</span>
                <input type="range" id="slider_{id_unico}" min="-180" max="180" value="0">
                <button class="btn-giro" id="btnAuto_{id_unico}">▶ Auto-Giro</button>
            </div>
            <div style="font-size:10.5px; color:#6E5036; text-align:center;">
                👕 {top_diseno.split('(')[0]} | 👖 {bot_diseno.split('(')[0]} | 👞 {sho_diseno.split('(')[0]}
            </div>
        </div>
    </div>

    <script>
        (function() {{
            const slider = document.getElementById('slider_{id_unico}');
            const btnAuto = document.getElementById('btnAuto_{id_unico}');
            const escena = document.getElementById('escena_{id_unico}');
            const badgeVista = document.getElementById('badgeVista_{id_unico}');

            const grupoGiro = document.getElementById('grupoGiro_{id_unico}');
            const rostroFrente = document.getElementById('rostroFrente_{id_unico}');
            const cabezaEspalda = document.getElementById('cabezaEspalda_{id_unico}');
            const detTopFrente = document.getElementById('detallesTopFrente_{id_unico}');
            const detTopEspalda = document.getElementById('detallesTopEspalda_{id_unico}');
            const detBotFrente = document.getElementById('detallesBotFrente_{id_unico}');
            const detBotEspalda = document.getElementById('detallesBotEspalda_{id_unico}');

            let anguloActual = 0;
            let autoGiroActivo = false;
            let animId = null;
            let arrastrando = false;
            let startX = 0;

            function aplicarRotacion(grados) {{
                anguloActual = ((grados + 180) % 360 + 360) % 360 - 180;
                slider.value = Math.round(anguloActual);

                const rad = anguloActual * Math.PI / 180;
                const cosVal = Math.cos(rad);
                const sinVal = Math.sin(rad);

                // Efecto 3D volumétrico con escala horizontal suave + desplazamiento de paralaje facial
                const signo = cosVal >= 0 ? 1 : -1;
                const escalaX = signo * Math.max(0.58, Math.abs(cosVal));
                const desplazamientoCara = sinVal * 12;

                grupoGiro.setAttribute(
                    'transform',
                    `translate(200, 0) scale(${{escalaX}}, 1) translate(-200, 0)`
                );
                rostroFrente.setAttribute('transform', `translate(${{desplazamientoCara}}, 0)`);

                const esEspalda = Math.abs(anguloActual) > 90;
                rostroFrente.style.display = esEspalda ? 'none' : 'block';
                cabezaEspalda.style.display = esEspalda ? 'block' : 'none';
                detTopFrente.style.display = esEspalda ? 'none' : 'block';
                detTopEspalda.style.display = esEspalda ? 'block' : 'none';
                detBotFrente.style.display = esEspalda ? 'none' : 'block';
                detBotEspalda.style.display = esEspalda ? 'block' : 'none';

                let nombreVista = "Frontal";
                if (esEspalda) nombreVista = "Espalda";
                else if (Math.abs(anguloActual) > 35) nombreVista = "Perfil 3/4";
                badgeVista.textContent = `Vista: ${{nombreVista}} (${{Math.round(anguloActual)}}°)`;
            }}

            slider.addEventListener('input', function() {{
                aplicarRotacion(parseFloat(this.value));
            }});

            // Arrastrar con el mouse directamente sobre el avatar
            escena.addEventListener('mousedown', function(e) {{
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'BUTTON') return;
                arrastrando = true;
                startX = e.clientX;
            }});
            window.addEventListener('mousemove', function(e) {{
                if (!arrastrando) return;
                const deltaX = e.clientX - startX;
                startX = e.clientX;
                aplicarRotacion(anguloActual + deltaX * 1.1);
            }});
            window.addEventListener('mouseup', function() {{
                arrastrando = false;
            }});

            // Botón de Auto-Giro 360°
            btnAuto.addEventListener('click', function() {{
                autoGiroActivo = !autoGiroActivo;
                btnAuto.textContent = autoGiroActivo ? "⏸ Pausar" : "▶ Auto-Giro";
                if (autoGiroActivo) {{
                    function loop() {{
                        if (!autoGiroActivo) return;
                        aplicarRotacion(anguloActual + 1.4);
                        animId = requestAnimationFrame(loop);
                    }}
                    loop();
                }} else if (animId) {{
                    cancelAnimationFrame(animId);
                }}
            }});
        }})();
    </script>
    </body>
    </html>
    """
    components.html(html_3d, height=altura_px)

# 6. ENCABEZADO Y NAVEGACIÓN PRINCIPAL
st.title("🧥 EcoArmario 3D")
st.write("Tu clóset digital con rotación 360°, adaptación de género, altura, silueta y diseños reales de prendas.")

tabs = st.tabs([
    "👗 Mi Armario",
    "➕ Agregar Prenda (Color y Diseño)",
    "📸 Escáner IA",
    "🧍 Mi Perfil, Género y Altura",
    "✨ Recomendador 3D y Agenda",
    "🤖 Asistente IA",
    "🌍 Impacto Ambiental"
])

# --- TAB 1: MI ARMARIO ---
with tabs[0]:
    st.header("Tus Prendas Registradas")
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
                <p>📁 <b>Categoría:</b> {p.get('categoria', 'Ropa')}</p>
                <p>✂️ <b>Diseño:</b> {p.get('diseno', 'Clásico')}</p>
                <p>🎨 <b>Color:</b> {etiqueta}</p>
                <p>🔄 <b>Usos:</b> {p.get('usos', 1)} puestas</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Registrar uso hoy ➕", key=f"btn_u_{p.get('id', idx)}"):
                p['usos'] = p.get('usos', 0) + 1
                st.rerun()

# --- TAB 2: AGREGAR PRENDA CON DISEÑO Y COLOR ---
with tabs[1]:
    st.header("➕ Añadir Nueva Prenda (Con Diseño y Color)")
    c1, c2 = st.columns(2)
    with c1:
        nom_in = st.text_input("Nombre de la prenda:", placeholder="Ej: Casaca de mezclilla o Camisa beige")
        cat_in = st.selectbox("Categoría:", ["Parte Superior", "Parte Inferior", "Calzado"])
        diseno_in = st.selectbox("Diseño visual en el Avatar 3D:", DISENOS_POR_CATEGORIA[cat_in])
        mat_in = st.selectbox("Material:", ["Algodón", "Lino", "Lana", "Denim", "Poliéster", "Cuero", "Lona"])
        usos_in = st.number_input("Veces que ya la has usado:", min_value=1, value=3)

    with c2:
        modo_c = st.radio("Selección de color:", ["Catálogo de 40+ Tonos", "Selector Libre de Color (Cualquier tono)"])
        if modo_c == "Catálogo de 40+ Tonos":
            nom_c = st.selectbox("Elige el color:", list(CATALOGO_COLORES.keys()))
            hex_c = CATALOGO_COLORES[nom_c]
        else:
            hex_c = st.color_picker("Selecciona cualquier color exacto:", "#8A5A36")
            nom_c = st.text_input("Nombre de este color:", value="Color Personalizado")
        st.markdown(f"Vista previa del color: <span class='muestra-color' style='background:{hex_c};width:26px;height:26px;'></span> `{hex_c}`", unsafe_allow_html=True)

    if st.button("Guardar Prenda en EcoArmario 🌿"):
        if not nom_in.strip():
            st.error("Por favor, escribe el nombre de la prenda.")
        else:
            huellas = {"Parte Superior": (2700, 5.5), "Parte Inferior": (7500, 15.0), "Calzado": (6000, 12.0)}
            ag, co = huellas[cat_in]
            st.session_state.armario.append({
                "id": len(st.session_state.armario) + 1,
                "nombre": nom_in,
                "categoria": cat_in,
                "diseno": diseno_in,
                "color": nom_c,
                "hex": hex_c,
                "material": mat_in,
                "usos": int(usos_in),
                "agua_l": ag,
                "co2_kg": co
            })
            st.success(f"¡'{nom_in}' ({diseno_in}) guardada! Ya puedes probártela en el recomendador 3D.")

# --- TAB 3: ESCÁNER IA ---
with tabs[2]:
    st.header("📸 Escáner Inteligente de Ropa")
    c_sub, c_res = st.columns(2)
    with c_sub:
        tipo_cam = st.radio("Método:", ["Subir foto", "Usar cámara"])
        foto = st.file_uploader("Sube la foto de tu prenda", type=["jpg", "png", "jpeg"]) if tipo_cam == "Subir foto" else st.camera_input("Captura tu prenda")

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

            st.success("¡Color y corte analizados!")
            nom_scan = st.text_input("Nombre detectado:", value="Prenda Escaneada")
            cat_scan = st.selectbox("Categoría:", ["Parte Superior", "Parte Inferior", "Calzado"], key="sc_cat")
            dis_scan = st.selectbox("Diseño detectado:", DISENOS_POR_CATEGORIA[cat_scan], key="sc_dis")
            hex_scan = st.color_picker("Color detectado:", color_auto_hex)

            if st.button("Guardar Prenda Escaneada"):
                st.session_state.armario.append({
                    "id": len(st.session_state.armario) + 1,
                    "nombre": nom_scan,
                    "categoria": cat_scan,
                    "diseno": dis_scan,
                    "color": "Tono Escaneado",
                    "hex": hex_scan,
                    "material": "Algodón mixto",
                    "usos": 1,
                    "agua_l": 3200,
                    "co2_kg": 7.0
                })
                st.success(f"¡'{nom_scan}' añadida con su diseño y color!")

# --- TAB 4: PERFIL, GÉNERO, ALTURA Y AVATAR 3D ---
with tabs[3]:
    st.header("🧍 Configura tu Género, Estatura, Silueta y Piel")
    st.write("Modifica cualquier opción y **gira el avatar 3D** con el deslizador o arrastrando con el mouse.")

    col_p, col_av = st.columns([1.15, 1])
    with col_p:
        c_gen, c_alt = st.columns(2)
        with c_gen:
            opciones_genero = ["Femenino", "Masculino"]
            gen_actual = st.session_state.perfil.get("genero", "Femenino")
            idx_gen = opciones_genero.index(gen_actual) if gen_actual in opciones_genero else 0
            genero_sel = st.radio("1. Género del Avatar:", opciones_genero, index=idx_gen, horizontal=True)

        with c_alt:
            altura_actual = int(st.session_state.perfil.get("altura_cm", 165))
            altura_sel = st.slider("2. Tu Estatura (cm):", min_value=140, max_value=200, value=altura_actual, step=1)

        opciones_cuerpo = [
            "Reloj de arena / Equilibrado",
            "Pera / Triángulo",
            "Triángulo Invertido",
            "Rectángulo",
            "Ovalado / Manzana"
        ]
        cuerpo_actual = st.session_state.perfil.get("cuerpo", opciones_cuerpo[0])
        idx_cuerpo = opciones_cuerpo.index(cuerpo_actual) if cuerpo_actual in opciones_cuerpo else 0
        cuerpo_sel = st.selectbox("3. Tipo de cuerpo / silueta:", opciones_cuerpo, index=idx_cuerpo)

        opciones_tono = list(TONOS_PIEL.keys())
        tono_actual = st.session_state.perfil.get("tono_nombre", opciones_tono[2])
        idx_tono = opciones_tono.index(tono_actual) if tono_actual in opciones_tono else 2
        tono_sel = st.selectbox("4. Tono de piel:", opciones_tono, index=idx_tono)

        c_col1, c_col2 = st.columns(2)
        with c_col1:
            piel_sel = st.color_picker("Ajuste exacto de piel:", TONOS_PIEL[tono_sel])
        with c_col2:
            cabello_sel = st.color_picker("Color de cabello:", st.session_state.perfil.get("cabello_hex", "#3B2618"))

        opciones_subtono = ["Cálido (Dorado / Melocotón)", "Frío (Rosado / Azulado)", "Neutro (Equilibrado)"]
        subtono_actual = st.session_state.perfil.get("subtono", opciones_subtono[0])
        idx_subtono = opciones_subtono.index(subtono_actual) if subtono_actual in opciones_subtono else 0
        subtono_sel = st.selectbox("5. Subtono de piel:", opciones_subtono, index=idx_subtono)

        st.session_state.perfil = {
            "genero": genero_sel,
            "altura_cm": altura_sel,
            "cuerpo": cuerpo_sel,
            "tono_nombre": tono_sel,
            "piel_hex": piel_sel,
            "subtono": subtono_sel,
            "cabello_hex": cabello_sel
        }

        consejo_estatura = obtener_consejo_altura(altura_sel, genero_sel)
        st.markdown(f"""
        <div class="tarjeta-ropa">
            <h4>💡 Recomendación según tu Altura y Perfil</h4>
            <p>{consejo_estatura}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_av:
        tops_d = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Superior']
        bots_d = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Inferior']
        shos_d = [p for p in st.session_state.armario if p.get('categoria') == 'Calzado']
        p_top = tops_d[0] if tops_d else {"nombre": "Camisa", "hex": "#C19A6B", "diseno": "Camisa (Cuello y Botones)"}
        p_bot = bots_d[0] if bots_d else {"nombre": "Pantalón", "hex": "#6F4E37", "diseno": "Pantalón Sastre / Chino (Recto)"}
        p_sho = shos_d[0] if shos_d else {"nombre": "Calzado", "hex": "#4B3020", "diseno": "Mocasines / Zapatos de Vestir"}
        renderizar_avatar_3d(p_top, p_bot, p_sho, st.session_state.perfil, id_unico="perfil3d")

# --- TAB 5: RECOMENDADOR 3D Y AGENDA ---
with tabs[4]:
    st.header("✨ Recomendador 3D (Cambia Color, Diseño y Proporción)")
    tops = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Superior']
    bottoms = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Inferior']
    shoes = [p for p in st.session_state.armario if p.get('categoria') == 'Calzado']

    if not tops or not bottoms or not shoes:
        st.info("Agrega al menos una prenda de cada categoría para ver combinaciones.")
    else:
        col_rec, col_3d_rec = st.columns([1.15, 1])
        with col_rec:
            modo_armado = st.radio(
                "¿Cómo quieres elegir el outfit?",
                ["Recomendación Inteligente (Según tu altura y color)", "Elegir Prendas Manualmente para Probar en el Avatar"],
                horizontal=True
            )

            ocasion = st.selectbox("Ocasión:", ["Casual / Diario", "Oficina / Estudio", "Reunión Elegante", "Fin de Semana"])

            if modo_armado.startswith("Recomendación"):
                if st.button("Generar Nueva Combinación 🎲") or 'outfit_3d' not in st.session_state:
                    st.session_state.outfit_3d = {
                        "top": random.choice(tops),
                        "bottom": random.choice(bottoms),
                        "shoes": random.choice(shoes)
                    }
            else:
                t_sel = st.selectbox("Elige Parte Superior:", tops, format_func=lambda x: f"{x['nombre']} — {x.get('diseno','')} ({x['color']})")
                b_sel = st.selectbox("Elige Parte Inferior:", bottoms, format_func=lambda x: f"{x['nombre']} — {x.get('diseno','')} ({x['color']})")
                s_sel = st.selectbox("Elige Calzado:", shoes, format_func=lambda x: f"{x['nombre']} — {x.get('diseno','')} ({x['color']})")
                st.session_state.outfit_3d = {"top": t_sel, "bottom": b_sel, "shoes": s_sel}

            out = st.session_state.outfit_3d
            arm_top_bot = calcular_armonia_colores(out['top'].get('hex', '#FFF'), out['bottom'].get('hex', '#333'))
            consejo_alt = obtener_consejo_altura(st.session_state.perfil.get("altura_cm", 165), st.session_state.perfil.get("genero", "Femenino"))

            st.markdown(f"""
            <div class="tarjeta-ropa">
                <h4>Outfit para: {ocasion}</h4>
                <p>👕 <b>Superior:</b> <span class="muestra-color" style="background:{out['top'].get('hex')};"></span> <b>{out['top']['nombre']}</b><br>
                <small>✂️ Diseño: {out['top'].get('diseno')} | 🎨 Color: {out['top'].get('color')}</small></p>
                <p>👖 <b>Inferior:</b> <span class="muestra-color" style="background:{out['bottom'].get('hex')};"></span> <b>{out['bottom']['nombre']}</b><br>
                <small>✂️ Diseño: {out['bottom'].get('diseno')} | 🎨 Color: {out['bottom'].get('color')}</small></p>
                <p>👞 <b>Calzado:</b> <span class="muestra-color" style="background:{out['shoes'].get('hex')};"></span> <b>{out['shoes']['nombre']}</b><br>
                <small>✂️ Diseño: {out['shoes'].get('diseno')} | 🎨 Color: {out['shoes'].get('color')}</small></p>
                <hr>
                <p>🎨 <b>Armonía de Color:</b> {arm_top_bot}</p>
                <p>{consejo_alt}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_3d_rec:
            renderizar_avatar_3d(out['top'], out['bottom'], out['shoes'], st.session_state.perfil, id_unico="rec3d")

        st.divider()
        st.subheader("📅 Agenda Semanal de Outfits")
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        agenda = []
        for d in dias:
            t = random.choice(tops)
            b = random.choice(bottoms)
            s = random.choice(shoes)
            agenda.append({
                "Día": d,
                "Parte Superior (Diseño y Color)": f"{t['nombre']} [{t.get('diseno','').split('(')[0].strip()}] ({t['color']})",
                "Parte Inferior (Diseño y Color)": f"{b['nombre']} [{b.get('diseno','').split('(')[0].strip()}] ({b['color']})",
                "Calzado": f"{s['nombre']} ({s['color']})",
                "Compatibilidad": calcular_armonia_colores(t.get('hex', '#FFF'), b.get('hex', '#000'))
            })
        st.dataframe(pd.DataFrame(agenda), use_container_width=True, hide_index=True)

# --- TAB 6: ASISTENTE IA ---
with tabs[5]:
    st.header("🤖 Asistente de Estilo IA (Adaptado a tu Altura y Género)")
    for m in st.session_state.mensajes_ia:
        with st.chat_message(m["rol"]):
            st.write(m["texto"])

    pregunta = st.chat_input("Ej: ¿Qué me pongo hoy según mi altura para verme más estilizado?")
    if pregunta:
        st.session_state.mensajes_ia.append({"rol": "user", "texto": pregunta})
        with st.chat_message("user"):
            st.write(pregunta)

        sug_top = random.choice(tops) if tops else {"nombre": "Camisa", "color": "Blanco", "diseno": "Camisa"}
        sug_bot = random.choice(bottoms) if bottoms else {"nombre": "Pantalón", "color": "Marrón", "diseno": "Recto"}
        sug_sho = random.choice(shoes) if shoes else {"nombre": "Calzado", "color": "Chocolate"}
        alt_u = st.session_state.perfil.get("altura_cm", 165)
        gen_u = st.session_state.perfil.get("genero", "Femenino")

        resp = (
            f"Considerando tu perfil **{gen_u}**, tu estatura de **{alt_u} cm** y tu silueta **{st.session_state.perfil.get('cuerpo')}**, "
            f"te sugiero combinar tu **{sug_top['nombre']}** (diseño *{sug_top.get('diseno')}* en color *{sug_top.get('color')}*) "
            f"con tu **{sug_bot['nombre']}** (diseño *{sug_bot.get('diseno')}* en *{sug_bot.get('color')}*) y tus **{sug_sho['nombre']}**. "
            f"{obtener_consejo_altura(alt_u, gen_u)}"
        )
        st.session_state.mensajes_ia.append({"rol": "assistant", "texto": resp})
        with st.chat_message("assistant"):
            st.write(resp)

# --- TAB 7: IMPACTO AMBIENTAL ---
with tabs[6]:
    st.header("🌍 Tu Impacto Ambiental Positivo")
    tot_agua = sum(p.get('agua_l', 0) for p in st.session_state.armario)
    tot_co2 = sum(p.get('co2_kg', 0) for p in st.session_state.armario)
    tot_usos = sum(p.get('usos', 0) for p in st.session_state.armario)

    c1, c2, c3 = st.columns(3)
    c1.metric("💧 Agua Amortizada", f"{tot_agua:,} Litros", "Reutilizando tu clóset")
    c2.metric("☁️ CO2 Evitado", f"{tot_co2:.1f} kg CO2", "Consumo responsable")
    c3.metric("🔄 Puestas Totales", f"{tot_usos} usos", "Vida útil activa")

    st.divider()
    df_arm = pd.DataFrame(st.session_state.armario)
    st.bar_chart(df_arm.set_index("nombre")["usos"])
