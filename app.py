import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import colorsys
import json
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

PRESETS_SILUETA = {
    "Reloj de arena / Equilibrado": {"hombros": 1.05, "pecho": 1.05, "cintura": 0.78, "cadera": 1.06, "complexion": 1.0},
    "Pera / Triángulo": {"hombros": 0.88, "pecho": 0.90, "cintura": 0.85, "cadera": 1.22, "complexion": 1.0},
    "Triángulo Invertido": {"hombros": 1.25, "pecho": 1.15, "cintura": 0.88, "cadera": 0.88, "complexion": 1.0},
    "Rectángulo": {"hombros": 1.00, "pecho": 0.96, "cintura": 0.96, "cadera": 0.98, "complexion": 0.98},
    "Ovalado / Manzana": {"hombros": 1.02, "pecho": 1.16, "cintura": 1.20, "cadera": 1.05, "complexion": 1.12}
}

# Funciones auxiliares
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
        return "Armonía Monocromática — Estiliza tu figura (96% Compatible)"
    elif diff_hue < 58:
        return "Armonía Análoga Suave (93% Compatible)"
    elif 150 <= diff_hue <= 210:
        return "Contraste Complementario (91% Compatible)"
    return "Combinación Creativa Equilibrada (88% Compatible)"

def obtener_consejo_altura(altura_cm, genero):
    if altura_cm < 162:
        return (
            f"📏 **Estatura Baja ({altura_cm} cm):** Te favorecen las **combinaciones monocromáticas** o de tonos similares "
            "para alargar visualmente tu silueta. Prioriza **Pantalones Sastre o Jeans de tiro alto** y evita prendas demasiado anchas."
        )
    elif altura_cm <= 175:
        return (
            f"📏 **Estatura Media ({altura_cm} cm):** Tu proporción te permite combinar libremente tanto **Camisas y Blazers** "
            "como **Pantalones Rectos o Anchos**, jugando con bloques de color equilibrados."
        )
    else:
        return (
            f"📏 **Estatura Alta ({altura_cm} cm):** Te lucen excelente los **contrastes de color marcados** entre el top y el pantalón, "
            "así como **Blazers con solapa**, **Suéteres tejidos** y **Pantalones Anchos o Jeans**."
        )

# 3. AUTORREPARACIÓN DE SESIÓN (Evita KeyError)
PERFIL_PREDETERMINADO = {
    "genero": "Femenino",
    "altura_cm": 165,
    "cuerpo": "Reloj de arena / Equilibrado",
    "tono_nombre": "Trigueño Claro",
    "piel_hex": "#E8B993",
    "subtono": "Cálido (Dorado / Melocotón)",
    "cabello_hex": "#3B2618",
    "molde_complexion": 1.0,
    "molde_hombros": 1.05,
    "molde_pecho": 1.05,
    "molde_cintura": 0.78,
    "molde_cadera": 1.06
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
        {"id": 7, "nombre": "Pantalón Palazzo Arena", "categoria": "Parte Inferior", "diseno": "Pantalón Ancho / Palazzo", "color": "Beige Arena", "hex": "#E1D4BC", "material": "Lino", "usos": 11, "agua_l": 5000, "co2_kg": 10.5},
        {"id": 8, "nombre": "Bermuda / Falda Terracota", "categoria": "Parte Inferior", "diseno": "Bermuda / Falda Corta", "color": "Terracota", "hex": "#B4553C", "material": "Algodón", "usos": 9, "agua_l": 3500, "co2_kg": 7.0},
        {"id": 9, "nombre": "Mocasines de Cuero", "categoria": "Calzado", "diseno": "Mocasines / Zapatos de Vestir", "color": "Marrón Chocolate", "hex": "#4B3020", "material": "Cuero", "usos": 30, "agua_l": 7000, "co2_kg": 14.0},
        {"id": 10, "nombre": "Zapatillas de Lona", "categoria": "Calzado", "diseno": "Zapatillas Urbanas (Con Pasadores)", "color": "Crema", "hex": "#F5EEDC", "material": "Lona", "usos": 18, "agua_l": 2800, "co2_kg": 6.0},
        {"id": 11, "nombre": "Botines de Cuero Negro", "categoria": "Calzado", "diseno": "Botines / Botas", "color": "Negro Ónix", "hex": "#222222", "material": "Cuero Vegano", "usos": 14, "agua_l": 4500, "co2_kg": 9.5},
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
        {"rol": "assistant", "texto": "¡Hola! Soy tu estilista 3D de EcoArmario. Ahora el maniquí tiene volumen 3D real al rotar, cuerpo moldeable y cambia el diseño y color de cada prenda según la recomendación. ¿Para qué ocasión quieres vestir hoy?"}
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

# 5. MOTOR DE AVATAR 3D REAL (THREE.JS WEBGL) CON VOLUMEN 360°, ROPA DINÁMICA Y TAMAÑO MOLDEABLE
def renderizar_avatar_3d(top_prenda, bottom_prenda, shoes_prenda, perfil, id_unico="av3d", altura_px=620):
    genero = perfil.get("genero", "Femenino")
    altura_cm = int(perfil.get("altura_cm", 165))
    cuerpo = perfil.get("cuerpo", "Reloj de arena / Equilibrado")
    tono_nombre = perfil.get("tono_nombre", "Trigueño Claro")
    piel_hex = perfil.get("piel_hex", "#E8B993")
    subtono = perfil.get("subtono", "Cálido (Dorado / Melocotón)")
    cabello_hex = perfil.get("cabello_hex", "#3B2618")

    # Matiz de piel según subtono
    r_p, g_p, b_p = hex_a_rgb(piel_hex)
    if "Cálido" in subtono:
        piel_final = rgb_a_hex((r_p + 6, g_p + 2, b_p - 5))
    elif "Frío" in subtono:
        piel_final = rgb_a_hex((r_p + 3, g_p - 2, b_p + 6))
    else:
        piel_final = piel_hex

    datos_escena = {
        "genero": genero,
        "altura_cm": altura_cm,
        "cuerpo": cuerpo,
        "tono_nombre": tono_nombre,
        "piel_hex": piel_final,
        "cabello_hex": cabello_hex,
        "molde_complexion": float(perfil.get("molde_complexion", 1.0)),
        "molde_hombros": float(perfil.get("molde_hombros", 1.05)),
        "molde_pecho": float(perfil.get("molde_pecho", 1.05)),
        "molde_cintura": float(perfil.get("molde_cintura", 0.78)),
        "molde_cadera": float(perfil.get("molde_cadera", 1.06)),
        "top_hex": top_prenda.get("hex", "#C19A6B"),
        "top_diseno": top_prenda.get("diseno", inferir_diseno(top_prenda.get("nombre", ""), "Parte Superior")),
        "top_nombre": top_prenda.get("nombre", "Prenda Superior"),
        "bot_hex": bottom_prenda.get("hex", "#6F4E37"),
        "bot_diseno": bottom_prenda.get("diseno", inferir_diseno(bottom_prenda.get("nombre", ""), "Parte Inferior")),
        "bot_nombre": bottom_prenda.get("nombre", "Prenda Inferior"),
        "sho_hex": shoes_prenda.get("hex", "#4B3020"),
        "sho_diseno": shoes_prenda.get("diseno", inferir_diseno(shoes_prenda.get("nombre", ""), "Calzado")),
        "sho_nombre": shoes_prenda.get("nombre", "Calzado")
    }
    config_json = json.dumps(datos_escena)

    html_3d = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body {{
            margin: 0; padding: 0; background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex; flex-direction: column; align-items: center;
            user-select: none;
        }}
        .escena-wrapper {{
            width: 420px; height: 600px;
            background: radial-gradient(circle at 50% 32%, #FFFDF9 0%, #EFE5D4 65%, #DCCAB0 100%);
            border-radius: 22px;
            box-shadow: inset 0 0 35px rgba(90,60,35,0.14), 0 10px 25px rgba(0,0,0,0.10);
            border: 2px solid #D5C3AE;
            position: relative; overflow: hidden;
        }}
        #canvas_{id_unico} {{
            width: 100%; height: 100%;
            cursor: grab;
        }}
        #canvas_{id_unico}:active {{ cursor: grabbing; }}
        .hud-top {{
            position: absolute; top: 10px; left: 12px; right: 12px;
            display: flex; justify-content: space-between; align-items: center;
            pointer-events: none; z-index: 10;
        }}
        .badge {{
            background: rgba(60, 40, 25, 0.86); color: #FFF;
            padding: 5px 11px; border-radius: 14px; font-size: 11px; font-weight: 600;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }}
        .regla-3d {{
            position: absolute; left: 12px; top: 55px; bottom: 95px;
            width: 44px; pointer-events: none; z-index: 8;
            display: flex; flex-direction: column; justify-content: space-between;
            border-left: 2px solid rgba(110, 80, 54, 0.55);
            padding-left: 5px; font-size: 10px; color: #5A3E28; font-weight: 600;
        }}
        .hud-bottom {{
            position: absolute; bottom: 10px; left: 12px; right: 12px;
            background: rgba(255, 255, 255, 0.93);
            backdrop-filter: blur(6px);
            border-radius: 12px; padding: 8px 12px;
            display: flex; flex-direction: column; gap: 6px;
            font-size: 12px; color: #3B281E; font-weight: 600;
            box-shadow: 0 4px 14px rgba(0,0,0,0.09);
            z-index: 10;
        }}
        .fila-ctrl {{
            display: flex; justify-content: space-between; align-items: center; gap: 8px;
        }}
        .btn-3d {{
            background: #8A5A36; color: white; border: none; border-radius: 6px;
            padding: 5px 10px; font-size: 11px; font-weight: 600; cursor: pointer;
        }}
        .btn-3d:hover {{ opacity: 0.9; }}
        input[type=range] {{ accent-color: #8A5A36; flex: 1; cursor: pointer; }}
    </style>
    </head>
    <body>
    <div class="escena-wrapper">
        <div class="hud-top">
            <span class="badge">🚻 {genero} | 📏 {altura_cm} cm</span>
            <span class="badge" id="anguloTxt_{id_unico}">Giro 3D: 0° (Frente)</span>
        </div>

        <div class="regla-3d">
            <span>200cm</span>
            <span>185cm</span>
            <span>170cm</span>
            <span>155cm</span>
            <span>140cm</span>
        </div>

        <div id="canvas_{id_unico}"></div>

        <div class="hud-bottom">
            <div class="fila-ctrl">
                <span>🔄 Rotar 3D:</span>
                <input type="range" id="slider_{id_unico}" min="-180" max="180" value="0">
                <button class="btn-3d" id="btnAuto_{id_unico}">▶ Giro 360°</button>
            </div>
            <div style="font-size:10.5px; color:#5A3E28; text-align:center; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                👕 {datos_escena['top_nombre']} | 👖 {datos_escena['bot_nombre']} | 👞 {datos_escena['sho_nombre']}
            </div>
        </div>
    </div>

    <script>
    (function() {{
        const cfg = {config_json};
        const container = document.getElementById('canvas_{id_unico}');
        const slider = document.getElementById('slider_{id_unico}');
        const btnAuto = document.getElementById('btnAuto_{id_unico}');
        const anguloTxt = document.getElementById('anguloTxt_{id_unico}');

        const width = 420, height = 600;
        const scene = new THREE.Scene();

        const camera = new THREE.PerspectiveCamera(34, width / height, 0.1, 100);
        camera.position.set(0, 1.05, 6.2);
        camera.lookAt(0, 0.95, 0);

        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        // Iluminación de estudio 3D (Luz principal, relleno lateral y contraluz para resaltar el volumen al girar)
        const ambientLight = new THREE.AmbientLight(0xfff8f0, 0.68);
        scene.add(ambientLight);

        const keyLight = new THREE.DirectionalLight(0xffffff, 0.78);
        keyLight.position.set(3.5, 5.5, 4.5);
        scene.add(keyLight);

        const fillLight = new THREE.DirectionalLight(0xf5e6d3, 0.42);
        fillLight.position.set(-4.0, 3.0, 2.0);
        scene.add(fillLight);

        const backLight = new THREE.DirectionalLight(0xffe8cc, 0.48);
        backLight.position.set(0, 4.0, -4.5);
        scene.add(backLight);

        // Materiales 3D
        const skinMat = new THREE.MeshStandardMaterial({{ color: cfg.piel_hex, roughness: 0.55, metalness: 0.05 }});
        const hairMat = new THREE.MeshStandardMaterial({{ color: cfg.cabello_hex, roughness: 0.45, metalness: 0.12 }});
        const topMat = new THREE.MeshStandardMaterial({{ color: cfg.top_hex, roughness: 0.68, metalness: 0.05, side: THREE.DoubleSide }});
        const botMat = new THREE.MeshStandardMaterial({{ color: cfg.bot_hex, roughness: 0.72, metalness: 0.06, side: THREE.DoubleSide }});
        const shoMat = new THREE.MeshStandardMaterial({{ color: cfg.sho_hex, roughness: 0.38, metalness: 0.18 }});
        const whiteMat = new THREE.MeshStandardMaterial({{ color: 0xf8f8f5, roughness: 0.5 }});
        const darkMat = new THREE.MeshStandardMaterial({{ color: 0x241811, roughness: 0.4 }});
        const goldMat = new THREE.MeshStandardMaterial({{ color: 0xd4af37, roughness: 0.25, metalness: 0.8 }});
        const lipMat = new THREE.MeshStandardMaterial({{ color: cfg.genero === "Masculino" ? cfg.piel_hex : 0xc96f69, roughness: 0.4 }});

        // Pedestal / Base 3D
        const pedestalGeo = new THREE.CylinderGeometry(0.95, 1.08, 0.12, 48);
        const pedestalMat = new THREE.MeshStandardMaterial({{ color: 0xc8b299, roughness: 0.6, metalness: 0.1 }});
        const pedestal = new THREE.Mesh(pedestalGeo, pedestalMat);
        pedestal.position.y = -0.78;
        scene.add(pedestal);

        const ringGeo = new THREE.TorusGeometry(0.96, 0.02, 16, 64);
        const ringMesh = new THREE.Mesh(ringGeo, goldMat);
        ringMesh.rotation.x = Math.PI / 2;
        ringMesh.position.y = -0.72;
        scene.add(ringMesh);

        // Grupo principal del Avatar 3D
        const avatarGroup = new THREE.Group();
        scene.add(avatarGroup);

        // Factores de moldeado anatómico (Hombros, Pecho, Cintura, Cadera, Complexión, Género)
        const esMasc = (cfg.genero === "Masculino");
        const comp = cfg.molde_complexion;
        const wSh = (esMasc ? 0.46 : 0.39) * cfg.molde_hombros * comp;
        const wCh = (esMasc ? 0.39 : 0.35) * cfg.molde_pecho * comp;
        const wWa = (esMasc ? 0.33 : 0.26) * cfg.molde_cintura * comp;
        const wHi = (esMasc ? 0.36 : 0.41) * cfg.molde_cadera * comp;

        // Profundidades 3D reales en el eje Z (para que al rotar de perfil se vea 100% tridimensional)
        const dCh = (esMasc ? 0.25 : 0.26) * cfg.molde_pecho * comp;
        const dWa = (esMasc ? 0.22 : 0.19) * cfg.molde_cintura * comp;
        const dHi = (esMasc ? 0.25 : 0.29) * cfg.molde_cadera * comp;

        // Función constructora de segmentos elípticos 3D suaves (Conecta dos anillos con X y Z independientes)
        function crearSegmento3D(rxTop, rzTop, rxBot, rzBot, altura, mat, segs=36) {{
            const geo = new THREE.CylinderGeometry(1, 1, altura, segs, 12, false);
            const pos = geo.attributes.position;
            for (let i = 0; i < pos.count; i++) {{
                const y = pos.getY(i);
                const t = (y + altura / 2) / altura; // 0 abajo, 1 arriba
                // Interpolación suave cosenoidal para curvas orgánicas
                const st = (1 - Math.cos(t * Math.PI)) / 2;
                const rx = rxBot + (rxTop - rxBot) * st;
                const rz = rzBot + (rzTop - rzBot) * st;
                pos.setX(i, pos.getX(i) * rx);
                pos.setZ(i, pos.getZ(i) * rz);
            }}
            geo.computeVertexNormals();
            return new THREE.Mesh(geo, mat);
        }}

        // 1. CABEZA Y ROSTRO 3D ESCULPIDO
        const headGroup = new THREE.Group();
        headGroup.position.set(0, 1.98, 0);
        avatarGroup.add(headGroup);

        // Cráneo/Rostro con volumen 3D
        const headGeo = new THREE.SphereGeometry(0.24, 36, 36);
        const headMesh = new THREE.Mesh(headGeo, skinMat);
        headMesh.scale.set(esMasc ? 0.96 : 0.90, 1.15, 1.02);
        headGroup.add(headMesh);

        // Mandíbula más marcada si es masculino
        if (esMasc) {{
            const jawGeo = new THREE.CylinderGeometry(0.18, 0.13, 0.18, 24);
            const jawMesh = new THREE.Mesh(jawGeo, skinMat);
            jawMesh.position.set(0, -0.10, 0.02);
            jawMesh.scale.set(1.0, 1.0, 0.92);
            headGroup.add(jawMesh);
        }}

        // Orejas 3D
        [-1, 1].forEach(side => {{
            const earGeo = new THREE.SphereGeometry(0.048, 16, 16);
            const ear = new THREE.Mesh(earGeo, skinMat);
            ear.scale.set(0.45, 1.1, 0.7);
            ear.position.set(side * (esMasc ? 0.225 : 0.21), -0.01, -0.01);
            headGroup.add(ear);
        }});

        // Nariz 3D que sobresale en el perfil (Eje Z)
        const noseGeo = new THREE.ConeGeometry(0.032, 0.10, 16);
        const nose = new THREE.Mesh(noseGeo, skinMat);
        nose.position.set(0, -0.01, 0.245);
        nose.rotation.x = 0.22;
        headGroup.add(nose);

        // Ojos 3D con Pupilas y Cejas
        [-1, 1].forEach(side => {{
            const eyeWhite = new THREE.Mesh(new THREE.SphereGeometry(0.034, 16, 16), whiteMat);
            eyeWhite.scale.set(1.2, 0.85, 0.6);
            eyeWhite.position.set(side * 0.082, 0.035, 0.215);
            headGroup.add(eyeWhite);

            const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.019, 16, 16), darkMat);
            pupil.scale.set(1.0, 1.0, 0.5);
            pupil.position.set(side * 0.082, 0.035, 0.233);
            headGroup.add(pupil);

            // Cejas 3D
            const browGeo = new THREE.BoxGeometry(0.075, esMasc ? 0.022 : 0.014, 0.02);
            const brow = new THREE.Mesh(browGeo, hairMat);
            brow.position.set(side * 0.082, 0.082, 0.225);
            brow.rotation.z = side * -0.08;
            headGroup.add(brow);
        }});

        // Labios 3D
        const lipsGeo = new THREE.TorusGeometry(0.038, 0.014, 12, 24);
        const lips = new THREE.Mesh(lipsGeo, lipMat);
        lips.scale.set(1.35, 0.55, 0.7);
        lips.position.set(0, -0.105, 0.218);
        headGroup.add(lips);

        // Cabello 3D Volumétrico (según Género)
        const hairCapGeo = new THREE.SphereGeometry(0.256, 32, 32, 0, Math.PI * 2, 0, Math.PI * 0.62);
        const hairCap = new THREE.Mesh(hairCapGeo, hairMat);
        hairCap.scale.set(esMasc ? 0.99 : 0.95, 1.12, 1.08);
        hairCap.position.set(0, 0.03, -0.015);
        hairCap.rotation.x = -0.18;
        headGroup.add(hairCap);

        // Flequillo / Volumen superior 3D
        const topHairGeo = new THREE.SphereGeometry(0.16, 24, 24);
        const topHair = new THREE.Mesh(topHairGeo, hairMat);
        topHair.scale.set(1.35, 0.65, 1.15);
        topHair.position.set(0, 0.23, 0.06);
        headGroup.add(topHair);

        if (!esMasc) {{
            // Cabello largo 3D con volumen en la espalda y laterales
            const backHairGeo = new THREE.CylinderGeometry(0.21, 0.26, 0.58, 28);
            const backHair = new THREE.Mesh(backHairGeo, hairMat);
            backHair.scale.set(1.0, 1.0, 0.65);
            backHair.position.set(0, -0.18, -0.11);
            headGroup.add(backHair);

            [-1, 1].forEach(side => {{
                const sideLock = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.04, 0.42, 16), hairMat);
                sideLock.position.set(side * 0.20, -0.14, 0.03);
                sideLock.rotation.z = side * 0.12;
                headGroup.add(sideLock);
            }});
        }} else {{
            // Nuca masculina 3D
            const napeHair = new THREE.Mesh(new THREE.CylinderGeometry(0.21, 0.17, 0.22, 24), hairMat);
            napeHair.scale.set(0.95, 1.0, 0.75);
            napeHair.position.set(0, -0.02, -0.07);
            headGroup.add(napeHair);
        }}

        // Cuello 3D
        const neckMesh = new THREE.Mesh(
            new THREE.CylinderGeometry(esMasc ? 0.115 : 0.095, esMasc ? 0.135 : 0.11, 0.24, 24),
            skinMat
        );
        neckMesh.position.set(0, 1.66, 0);
        avatarGroup.add(neckMesh);

        // 2. TORSO Y PRENDA SUPERIOR 3D (Cambia su geometría según el diseño recomendado)
        const topDesign = cfg.top_diseno;
        const scaleCloth = topDesign.includes("Suéter") ? 1.06 : topDesign.includes("Blazer") ? 1.04 : 1.02;

        // Parte alta del torso (Hombros a Pecho)
        const upperTorso = crearSegmento3D(
            wSh * scaleCloth, dCh * 0.88 * scaleCloth,
            wCh * scaleCloth, dCh * scaleCloth,
            0.34, topMat
        );
        upperTorso.position.set(0, 1.43, 0);
        avatarGroup.add(upperTorso);

        // Volumen pectoral / busto 3D en el eje Z (Hace que el perfil 3D sea realista)
        [-1, 1].forEach(side => {{
            const chestVolGeo = new THREE.SphereGeometry(esMasc ? 0.135 : 0.145, 24, 24);
            const chestVol = new THREE.Mesh(chestVolGeo, topMat);
            chestVol.scale.set(
                1.1 * cfg.molde_pecho,
                esMasc ? 0.85 : 0.95,
                (esMasc ? 0.65 : 0.92) * cfg.molde_pecho
            );
            chestVol.position.set(side * 0.115 * cfg.molde_pecho, 1.34, dCh * 0.58);
            avatarGroup.add(chestVol);
        }});

        // Parte media del torso (Pecho a Cintura)
        const midTorso = crearSegmento3D(
            wCh * scaleCloth, dCh * scaleCloth,
            wWa * scaleCloth, dWa * scaleCloth,
            0.34, topMat
        );
        midTorso.position.set(0, 1.10, 0);
        avatarGroup.add(midTorso);

        // Parte baja del top (Cintura a Cadera Alta)
        const lowTorso = crearSegmento3D(
            wWa * scaleCloth, dWa * scaleCloth,
            wHi * 0.97 * scaleCloth, dHi * 0.95 * scaleCloth,
            0.22, topMat
        );
        lowTorso.position.set(0, 0.83, 0);
        avatarGroup.add(lowTorso);

        // DETALLES 3D ESPECÍFICOS DEL DISEÑO DE PRENDA SUPERIOR
        if (topDesign.includes("Camisa")) {{
            // Cuello de camisa 3D elevado + abertura en V + tapeta y botones 3D
            const collarGeo = new THREE.CylinderGeometry(0.135, 0.15, 0.09, 28, 1, true, 0.4, Math.PI * 1.75);
            const collarMesh = new THREE.Mesh(collarGeo, topMat);
            collarMesh.position.set(0, 1.62, 0);
            collarMesh.rotation.y = Math.PI * 0.62;
            avatarGroup.add(collarMesh);

            // Hilera de botones en 3D
            for (let b = 0; b < 5; b++) {{
                const btn = new THREE.Mesh(new THREE.SphereGeometry(0.016, 12, 12), whiteMat);
                const zOffset = (b < 2) ? dCh * 0.98 : dWa * 0.98;
                btn.position.set(0, 1.44 - b * 0.14, zOffset + 0.015);
                avatarGroup.add(btn);
            }}
        }} else if (topDesign.includes("Suéter")) {{
            // Cuello redondo grueso tejido en 3D + pretina inferior
            const neckRib = new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.032, 16, 32), topMat);
            neckRib.rotation.x = Math.PI / 2;
            neckRib.position.set(0, 1.60, 0.01);
            avatarGroup.add(neckRib);

            const waistRib = crearSegmento3D(wHi * 0.99, dHi * 0.97, wHi * 0.97, dHi * 0.95, 0.07, topMat);
            waistRib.position.set(0, 0.73, 0);
            avatarGroup.add(waistRib);
        }} else if (topDesign.includes("Blazer")) {{
            // Camiseta interior blanca 3D + Solapas estructuradas en relieve
            const innerFront = crearSegmento3D(wCh * 0.55, dCh * 1.03, wWa * 0.55, dWa * 1.04, 0.82, whiteMat);
            innerFront.position.set(0, 1.15, 0.015);
            avatarGroup.add(innerFront);

            [-1, 1].forEach(side => {{
                const lapelGeo = new THREE.BoxGeometry(0.08, 0.48, 0.035);
                const lapel = new THREE.Mesh(lapelGeo, topMat);
                lapel.position.set(side * 0.095, 1.32, dCh * 0.96);
                lapel.rotation.z = side * -0.18;
                avatarGroup.add(lapel);
            }});
        }} else {{
            // Polo / Blusa Manga Corta: Escote de piel visible
            const vNeck = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.04, 0.14, 24), skinMat);
            vNeck.scale.set(1.0, 1.0, 0.85);
            vNeck.position.set(0, 1.56, dCh * 0.45);
            avatarGroup.add(vNeck);
        }}

        // 3. BRAZOS Y MANGAS 3D (Manga corta vs Manga larga según diseño)
        const esMangaCorta = topDesign.includes("Polo");
        [-1, 1].forEach(side => {{
            const armGroup = new THREE.Group();
            armGroup.position.set(side * (wSh + 0.04), 1.52, 0);
            armGroup.rotation.z = side * -0.09;
            avatarGroup.add(armGroup);

            // Hombro 3D redondeado
            const shoulderSphere = new THREE.Mesh(new THREE.SphereGeometry(0.095 * comp, 20, 20), topMat);
            armGroup.add(shoulderSphere);

            // Brazo superior (Cubierto por manga)
            const upperArm = new THREE.Mesh(
                new THREE.CylinderGeometry(0.088 * comp, 0.076 * comp, 0.34, 20),
                topMat
            );
            upperArm.position.set(0, -0.18, 0);
            armGroup.add(upperArm);

            // Antebrazo (Piel si es manga corta, Tela si es manga larga)
            const foreArmMat = esMangaCorta ? skinMat : topMat;
            const foreArm = new THREE.Mesh(
                new THREE.CylinderGeometry(0.074 * comp, 0.058 * comp, 0.34, 20),
                foreArmMat
            );
            foreArm.position.set(0, -0.50, 0.02);
            foreArm.rotation.x = -0.08;
            armGroup.add(foreArm);

            // Puño de camisa si corresponde
            if (topDesign.includes("Camisa")) {{
                const cuff = new THREE.Mesh(new THREE.CylinderGeometry(0.064 * comp, 0.064 * comp, 0.06, 20), whiteMat);
                cuff.position.set(0, -0.65, 0.03);
                armGroup.add(cuff);
            }}

            // Mano 3D esculpida
            const hand = new THREE.Mesh(new THREE.SphereGeometry(0.062 * comp, 16, 16), skinMat);
            hand.scale.set(0.85, 1.25, 0.65);
            hand.position.set(0, -0.73, 0.035);
            armGroup.add(hand);
        }});

        // 4. CADERA, PIERNAS Y PRENDA INFERIOR 3D (Cambia según diseño recomendado)
        const botDesign = cfg.bot_diseno;

        // Pelvis / Cadera 3D
        const pelvisMesh = crearSegmento3D(wHi * 0.98, dHi * 0.96, wHi * 1.02, dHi * 1.02, 0.24, botMat);
        pelvisMesh.position.set(0, 0.62, -0.01);
        avatarGroup.add(pelvisMesh);

        // Volumen glúteo 3D en la parte posterior (Eje -Z)
        [-1, 1].forEach(side => {{
            const glute = new THREE.Mesh(new THREE.SphereGeometry(0.145 * comp, 20, 20), botMat);
            glute.scale.set(1.05 * cfg.molde_cadera, 1.0, 0.85 * cfg.molde_cadera);
            glute.position.set(side * 0.11 * cfg.molde_cadera, 0.56, -dHi * 0.65);
            avatarGroup.add(glute);

            // Si son Jeans, añade bolsillos traseros en relieve 3D
            if (botDesign.includes("Jeans")) {{
                const pocket = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.12, 0.02), goldMat);
                pocket.position.set(side * 0.11 * cfg.molde_cadera, 0.57, -dHi * 1.02);
                avatarGroup.add(pocket);
            }}
        }});

        // Cinturón 3D en Pantalón Sastre o Jeans
        if (botDesign.includes("Sastre") || botDesign.includes("Jeans")) {{
            const belt = crearSegmento3D(wHi * 1.00, dHi * 0.98, wHi * 1.00, dHi * 0.98, 0.045, darkMat);
            belt.position.set(0, 0.73, -0.005);
            avatarGroup.add(belt);

            const buckle = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.055, 0.03), goldMat);
            buckle.position.set(0, 0.73, dHi * 0.98);
            avatarGroup.add(buckle);
        }}

        const legSep = Math.max(0.135, wHi * 0.44);

        if (botDesign.includes("Bermuda") && !esMasc) {{
            // Falda 3D acampanada + piernas de piel en 3D
            const skirt = crearSegmento3D(wHi * 1.01, dHi * 1.01, wHi * 1.28, dHi * 1.22, 0.48, botMat);
            skirt.position.set(0, 0.32, -0.01);
            avatarGroup.add(skirt);

            [-1, 1].forEach(side => {{
                const lowerLeg = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.105 * comp, 0.068 * comp, 0.72, 24),
                    skinMat
                );
                lowerLeg.position.set(side * legSep, -0.22, 0);
                avatarGroup.add(lowerLeg);
            }});
        }} else {{
            // Piernas de Pantalón (Recto, Jeans, Palazzo Ancho o Bermuda)
            const esPalazzo = botDesign.includes("Ancho");
            const esBermuda = botDesign.includes("Bermuda");

            [-1, 1].forEach(side => {{
                // Muslo 3D
                const thighTopR = 0.155 * comp * (cfg.molde_cadera * 0.92);
                const thighBotR = esPalazzo ? thighTopR * 1.12 : 0.118 * comp;
                const thigh = new THREE.Mesh(
                    new THREE.CylinderGeometry(thighTopR, thighBotR, 0.52, 24),
                    botMat
                );
                thigh.position.set(side * legSep, 0.26, 0);
                avatarGroup.add(thigh);

                // Pantorrilla (De tela o de piel si es bermuda)
                const calfTopR = thighBotR;
                const calfBotR = esPalazzo ? thighTopR * 1.22 : (esBermuda ? 0.072 * comp : 0.088 * comp);
                const calfMat = esBermuda ? skinMat : botMat;
                const calf = new THREE.Mesh(
                    new THREE.CylinderGeometry(calfTopR, calfBotR, 0.56, 24),
                    calfMat
                );
                calf.position.set(side * legSep, -0.28, 0);
                avatarGroup.add(calf);
            }});
        }}

        // 5. CALZADO 3D VOLUMÉTRICO (Mocasines, Zapatillas con pasadores, Botines)
        const shoDesign = cfg.sho_diseno;
        [-1, 1].forEach(side => {{
            const shoeGroup = new THREE.Group();
            shoeGroup.position.set(side * legSep, -0.62, 0.05);
            avatarGroup.add(shoeGroup);

            // Si son Botines, caña alta 3D que sube por el tobillo
            if (shoDesign.includes("Botines")) {{
                const bootShaft = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.095 * comp, 0.088 * comp, 0.22, 20),
                    shoMat
                );
                bootShaft.position.set(0, 0.12, -0.04);
                shoeGroup.add(bootShaft);
            }}

            // Cuerpo principal del zapato (Proyectado hacia adelante en Z)
            const footGeo = new THREE.SphereGeometry(0.095, 24, 24);
            const footMesh = new THREE.Mesh(footGeo, shoMat);
            footMesh.scale.set(0.95, 0.65, 1.75);
            footMesh.position.set(0, -0.02, 0.04);
            shoeGroup.add(footMesh);

            // Suela 3D (Blanca gruesa en zapatillas, oscura con tacón en mocasines/botines)
            const soleMat = shoDesign.includes("Zapatillas") ? whiteMat : darkMat;
            const soleGeo = new THREE.BoxGeometry(0.17, shoDesign.includes("Zapatillas") ? 0.045 : 0.028, 0.32);
            const sole = new THREE.Mesh(soleGeo, soleMat);
            sole.position.set(0, -0.075, 0.035);
            shoeGroup.add(sole);

            if (shoDesign.includes("Zapatillas")) {{
                // Pasadores blancos 3D sobre el empeine
                for (let l = 0; l < 3; l++) {{
                    const lace = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.012, 0.016), whiteMat);
                    lace.position.set(0, 0.025 - l * 0.012, 0.03 + l * 0.035);
                    shoeGroup.add(lace);
                }}
            }} else if (shoDesign.includes("Mocasines")) {{
                // Hebilla dorada clásica en el empeine
                const bit = new THREE.Mesh(new THREE.BoxGeometry(0.095, 0.015, 0.02), goldMat);
                bit.position.set(0, 0.028, 0.06);
                shoeGroup.add(bit);
            }}
        }});

        // Escala vertical según la estatura en cm (140 cm a 200 cm) manteniendo los pies sobre el pedestal
        const factorAltura = 0.84 + ((cfg.altura_cm - 140) / 60.0) * 0.24;
        avatarGroup.scale.set(1.0, factorAltura, 1.0);
        avatarGroup.position.y = -0.72 + 0.72 * factorAltura - 0.72 * (factorAltura - 1.0) * 0.9;

        // CONTROLES DE ROTACIÓN 3D REAL (360° COMPLETOS SIN APLANARSE)
        let rotY = 0;
        let autoGiro = false;
        let isDragging = false;
        let prevX = 0;

        function actualizarAnguloUI(deg) {{
            let norm = ((deg + 180) % 360 + 360) % 360 - 180;
            slider.value = Math.round(norm);
            let vista = "Frente";
            const absD = Math.abs(norm);
            if (absD > 135) vista = "Espalda";
            else if (absD > 45) vista = "Perfil 3D";
            anguloTxt.textContent = `Giro 3D: ${{Math.round(norm)}}° (${{vista}})`;
        }}

        slider.addEventListener('input', function() {{
            const deg = parseFloat(this.value);
            rotY = deg * Math.PI / 180;
            avatarGroup.rotation.y = rotY;
            actualizarAnguloUI(deg);
        }});

        container.addEventListener('mousedown', (e) => {{
            isDragging = true;
            prevX = e.clientX;
        }});
        window.addEventListener('mousemove', (e) => {{
            if (!isDragging) return;
            const dx = e.clientX - prevX;
            prevX = e.clientX;
            rotY += dx * 0.015;
            avatarGroup.rotation.y = rotY;
            actualizarAnguloUI(rotY * 180 / Math.PI);
        }});
        window.addEventListener('mouseup', () => {{ isDragging = false; }});

        // Soporte táctil para celulares/tablets
        container.addEventListener('touchstart', (e) => {{
            if (e.touches.length === 1) {{
                isDragging = true;
                prevX = e.touches[0].clientX;
            }}
        }});
        window.addEventListener('touchmove', (e) => {{
            if (!isDragging || e.touches.length !== 1) return;
            const dx = e.touches[0].clientX - prevX;
            prevX = e.touches[0].clientX;
            rotY += dx * 0.015;
            avatarGroup.rotation.y = rotY;
            actualizarAnguloUI(rotY * 180 / Math.PI);
        }});
        window.addEventListener('touchend', () => {{ isDragging = false; }});

        btnAuto.addEventListener('click', () => {{
            autoGiro = !autoGiro;
            btnAuto.textContent = autoGiro ? "⏸ Pausar" : "▶ Giro 360°";
        }});

        // Bucle de animación 3D (Respiración orgánica + Giro 360°)
        let clock = new THREE.Clock();
        function animate() {{
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();

            // Respiración suave del torso 3D
            headGroup.position.y = 1.98 + Math.sin(t * 2.2) * 0.008;

            if (autoGiro && !isDragging) {{
                rotY += 0.018;
                avatarGroup.rotation.y = rotY;
                actualizarAnguloUI(rotY * 180 / Math.PI);
            }}

            renderer.render(scene, camera);
        }}
        animate();
    }})();
    </script>
    </body>
    </html>
    """
    components.html(html_3d, height=altura_px)

# 6. ENCABEZADO Y NAVEGACIÓN PRINCIPAL
st.title("🧥 EcoArmario 3D")
st.write("Tu clóset digital con maniquí 3D volumétrico real, tamaño moldeable y cambio automático de diseño y color.")

tabs = st.tabs([
    "👗 Mi Armario",
    "➕ Agregar Prenda (Color y Diseño)",
    "📸 Escáner IA",
    "🧍 Cuerpo Moldeable 3D, Género y Altura",
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
                <p>✂️ <b>Diseño 3D:</b> {p.get('diseno', 'Clásico')}</p>
                <p>🎨 <b>Color:</b> {etiqueta}</p>
                <p>🔄 <b>Usos:</b> {p.get('usos', 1)} puestas</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Registrar uso hoy ➕", key=f"btn_u_{p.get('id', idx)}"):
                p['usos'] = p.get('usos', 0) + 1
                st.rerun()

# --- TAB 2: AGREGAR PRENDA CON DISEÑO Y COLOR ---
with tabs[1]:
    st.header("➕ Añadir Nueva Prenda a tu Armario")
    c1, c2 = st.columns(2)
    with c1:
        nom_in = st.text_input("Nombre de la prenda:", placeholder="Ej: Blazer Azul o Suéter Tejido")
        cat_in = st.selectbox("Categoría:", ["Parte Superior", "Parte Inferior", "Calzado"])
        diseno_in = st.selectbox("Diseño 3D que vestirá el Avatar:", DISENOS_POR_CATEGORIA[cat_in])
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
            nueva = {
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
            }
            st.session_state.armario.append(nueva)
            st.success(f"¡'{nom_in}' ({diseno_in}) guardada! Ya puedes verla en el Recomendador 3D.")

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

            st.success("¡Color y diseño detectados!")
            nom_scan = st.text_input("Nombre detectado:", value="Prenda Escaneada")
            cat_scan = st.selectbox("Categoría:", ["Parte Superior", "Parte Inferior", "Calzado"], key="sc_cat")
            dis_scan = st.selectbox("Diseño 3D detectado:", DISENOS_POR_CATEGORIA[cat_scan], key="sc_dis")
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
                st.success(f"¡'{nom_scan}' añadida con su diseño 3D y color!")

# --- TAB 4: PERFIL, GÉNERO, ALTURA Y CUERPO MOLDEABLE EN 3D ---
with tabs[3]:
    st.header("🧍 Moldea tu Cuerpo 3D, Género, Estatura y Tono de Piel")
    st.write("Ajusta tus medidas con los deslizadores y **rota el avatar 3D** con el mouse o el botón de giro 360° para ver su volumen real desde cualquier ángulo.")

    col_p, col_av = st.columns([1.18, 1])
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

        opciones_cuerpo = list(PRESETS_SILUETA.keys())
        cuerpo_actual = st.session_state.perfil.get("cuerpo", opciones_cuerpo[0])
        idx_cuerpo = opciones_cuerpo.index(cuerpo_actual) if cuerpo_actual in opciones_cuerpo else 0
        cuerpo_sel = st.selectbox("3. Silueta base (Carga proporciones iniciales):", opciones_cuerpo, index=idx_cuerpo)

        # Si el usuario cambia de preset de silueta, actualiza los valores base moldeables
        if cuerpo_sel != st.session_state.perfil.get("cuerpo"):
            preset = PRESETS_SILUETA[cuerpo_sel]
            st.session_state.perfil["molde_complexion"] = preset["complexion"]
            st.session_state.perfil["molde_hombros"] = preset["hombros"]
            st.session_state.perfil["molde_pecho"] = preset["pecho"]
            st.session_state.perfil["molde_cintura"] = preset["cintura"]
            st.session_state.perfil["molde_cadera"] = preset["cadera"]

        st.markdown("##### 📐 Moldea el Tamaño Exacto de tu Cuerpo en 3D")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            molde_comp = st.slider("Complexión / Volumen General:", 0.75, 1.35, float(st.session_state.perfil.get("molde_complexion", 1.0)), 0.02)
            molde_hom = st.slider("Ancho de Hombros:", 0.75, 1.35, float(st.session_state.perfil.get("molde_hombros", 1.05)), 0.02)
            molde_pec = st.slider("Volumen de Pecho / Torso:", 0.75, 1.35, float(st.session_state.perfil.get("molde_pecho", 1.05)), 0.02)
        with m_col2:
            molde_cin = st.slider("Contorno de Cintura:", 0.65, 1.35, float(st.session_state.perfil.get("molde_cintura", 0.78)), 0.02)
            molde_cad = st.slider("Ancho y Volumen de Cadera:", 0.75, 1.40, float(st.session_state.perfil.get("molde_cadera", 1.06)), 0.02)

        st.markdown("##### 🎨 Tono de Piel y Cabello")
        opciones_tono = list(TONOS_PIEL.keys())
        tono_actual = st.session_state.perfil.get("tono_nombre", opciones_tono[2])
        idx_tono = opciones_tono.index(tono_actual) if tono_actual in opciones_tono else 2
        tono_sel = st.selectbox("Tono de piel:", opciones_tono, index=idx_tono)

        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1:
            piel_sel = st.color_picker("Ajustar piel:", TONOS_PIEL[tono_sel])
        with c_col2:
            cabello_sel = st.color_picker("Color cabello:", st.session_state.perfil.get("cabello_hex", "#3B2618"))
        with c_col3:
            opciones_subtono = ["Cálido (Dorado / Melocotón)", "Frío (Rosado / Azulado)", "Neutro (Equilibrado)"]
            subtono_sel = st.selectbox("Subtono:", opciones_subtono)

        st.session_state.perfil = {
            "genero": genero_sel,
            "altura_cm": altura_sel,
            "cuerpo": cuerpo_sel,
            "tono_nombre": tono_sel,
            "piel_hex": piel_sel,
            "subtono": subtono_sel,
            "cabello_hex": cabello_sel,
            "molde_complexion": molde_comp,
            "molde_hombros": molde_hom,
            "molde_pecho": molde_pec,
            "molde_cintura": molde_cin,
            "molde_cadera": molde_cad
        }

        st.markdown(f"""
        <div class="tarjeta-ropa">
            <h4>💡 Recomendación según tu Altura y Silueta</h4>
            <p>{obtener_consejo_altura(altura_sel, genero_sel)}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_av:
        # Usa el outfit recomendado actual para mostrar cómo queda en el cuerpo moldeado
        tops_d = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Superior']
        bots_d = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Inferior']
        shos_d = [p for p in st.session_state.armario if p.get('categoria') == 'Calzado']
        if 'outfit_3d' in st.session_state:
            p_top = st.session_state.outfit_3d['top']
            p_bot = st.session_state.outfit_3d['bottom']
            p_sho = st.session_state.outfit_3d['shoes']
        else:
            p_top = tops_d[0]
            p_bot = bots_d[0]
            p_sho = shos_d[0]
        renderizar_avatar_3d(p_top, p_bot, p_sho, st.session_state.perfil, id_unico="perfil3d")

# --- TAB 5: RECOMENDADOR 3D Y AGENDA ---
with tabs[4]:
    st.header("✨ Recomendador 3D en Vivo (Cambia Diseño y Color en el Avatar)")
    tops = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Superior']
    bottoms = [p for p in st.session_state.armario if p.get('categoria') == 'Parte Inferior']
    shoes = [p for p in st.session_state.armario if p.get('categoria') == 'Calzado']

    if not tops or not bottoms or not shoes:
        st.info("Agrega al menos una prenda de cada categoría para ver combinaciones.")
    else:
        # Inicializa la agenda semanal y el outfit actual si no existen
        if 'agenda_semanal' not in st.session_state or st.button("🔄 Generar Nuevas Recomendaciones para Hoy y la Semana 🎲"):
            st.session_state.outfit_3d = {
                "top": random.choice(tops),
                "bottom": random.choice(bottoms),
                "shoes": random.choice(shoes)
            }
            dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            st.session_state.agenda_semanal = {}
            for d in dias:
                st.session_state.agenda_semanal[d] = {
                    "top": random.choice(tops),
                    "bottom": random.choice(bottoms),
                    "shoes": random.choice(shoes)
                }

        col_rec, col_3d_rec = st.columns([1.15, 1])
        with col_rec:
            modo_armado = st.radio(
                "¿Qué outfit quieres visualizar en el Avatar 3D?",
                [
                    "Recomendación Inteligente del Día",
                    "Ver un Día de mi Agenda Semanal en el Avatar",
                    "Personalizar Prendas, Diseños y Colores Manualmente"
                ]
            )

            ocasion = st.selectbox("Ocasión:", ["Casual / Diario", "Oficina / Estudio", "Reunión Elegante", "Fin de Semana"])

            if modo_armado == "Recomendación Inteligente del Día":
                out = st.session_state.outfit_3d
            elif modo_armado == "Ver un Día de mi Agenda Semanal en el Avatar":
                dia_elegido = st.selectbox("Selecciona el día de la semana para probártelo en 3D:", list(st.session_state.agenda_semanal.keys()))
                out = st.session_state.agenda_semanal[dia_elegido]
                st.session_state.outfit_3d = out
            else:
                t_sel = st.selectbox("Elige Parte Superior:", tops, format_func=lambda x: f"{x['nombre']} — {x.get('diseno','')} ({x['color']})")
                b_sel = st.selectbox("Elige Parte Inferior:", bottoms, format_func=lambda x: f"{x['nombre']} — {x.get('diseno','')} ({x['color']})")
                s_sel = st.selectbox("Elige Calzado:", shoes, format_func=lambda x: f"{x['nombre']} — {x.get('diseno','')} ({x['color']})")

                # Permite probar al instante otro diseño o color sobre la prenda seleccionada
                st.markdown("###### 🎨 Ajustar Diseño o Color en Vivo sobre el Avatar:")
                c_mod1, c_mod2, c_mod3 = st.columns(3)
                with c_mod1:
                    dis_t_vivo = st.selectbox("Diseño Top:", DISENOS_POR_CATEGORIA["Parte Superior"], index=DISENOS_POR_CATEGORIA["Parte Superior"].index(t_sel.get("diseno", DISENOS_POR_CATEGORIA["Parte Superior"][0])))
                    col_t_vivo = st.color_picker("Color Top:", t_sel.get("hex", "#C19A6B"))
                with c_mod2:
                    dis_b_vivo = st.selectbox("Diseño Inferior:", DISENOS_POR_CATEGORIA["Parte Inferior"], index=DISENOS_POR_CATEGORIA["Parte Inferior"].index(b_sel.get("diseno", DISENOS_POR_CATEGORIA["Parte Inferior"][0])))
                    col_b_vivo = st.color_picker("Color Inferior:", b_sel.get("hex", "#6F4E37"))
                with c_mod3:
                    dis_s_vivo = st.selectbox("Diseño Calzado:", DISENOS_POR_CATEGORIA["Calzado"], index=DISENOS_POR_CATEGORIA["Calzado"].index(s_sel.get("diseno", DISENOS_POR_CATEGORIA["Calzado"][0])))
                    col_s_vivo = st.color_picker("Color Calzado:", s_sel.get("hex", "#4B3020"))

                out = {
                    "top": {**t_sel, "diseno": dis_t_vivo, "hex": col_t_vivo},
                    "bottom": {**b_sel, "diseno": dis_b_vivo, "hex": col_b_vivo},
                    "shoes": {**s_sel, "diseno": dis_s_vivo, "hex": col_s_vivo}
                }
                st.session_state.outfit_3d = out

            arm_top_bot = calcular_armonia_colores(out['top'].get('hex', '#FFF'), out['bottom'].get('hex', '#333'))
            consejo_alt = obtener_consejo_altura(st.session_state.perfil.get("altura_cm", 165), st.session_state.perfil.get("genero", "Femenino"))

            st.markdown(f"""
            <div class="tarjeta-ropa">
                <h4>Outfit Activo en el Maniquí 3D ({ocasion})</h4>
                <p>👕 <b>Superior:</b> <span class="muestra-color" style="background:{out['top'].get('hex')};"></span> <b>{out['top']['nombre']}</b><br>
                <small>✂️ Diseño 3D: <b>{out['top'].get('diseno')}</b> | 🎨 Código: {out['top'].get('hex')}</small></p>
                <p>👖 <b>Inferior:</b> <span class="muestra-color" style="background:{out['bottom'].get('hex')};"></span> <b>{out['bottom']['nombre']}</b><br>
                <small>✂️ Diseño 3D: <b>{out['bottom'].get('diseno')}</b> | 🎨 Código: {out['bottom'].get('hex')}</small></p>
                <p>👞 <b>Calzado:</b> <span class="muestra-color" style="background:{out['shoes'].get('hex')};"></span> <b>{out['shoes']['nombre']}</b><br>
                <small>✂️ Diseño 3D: <b>{out['shoes'].get('diseno')}</b> | 🎨 Código: {out['shoes'].get('hex')}</small></p>
                <hr>
                <p>🎨 <b>Armonía de Color:</b> {arm_top_bot}</p>
                <p>{consejo_alt}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_3d_rec:
            renderizar_avatar_3d(out['top'], out['bottom'], out['shoes'], st.session_state.perfil, id_unico="rec3d")

        st.divider()
        st.subheader("📅 Agenda Semanal de Outfits")
        filas_agenda = []
        for d, conj in st.session_state.agenda_semanal.items():
            t = conj["top"]
            b = conj["bottom"]
            s = conj["shoes"]
            filas_agenda.append({
                "Día": d,
                "Parte Superior (Diseño y Color)": f"{t['nombre']} — {t.get('diseno','')} ({t['color']})",
                "Parte Inferior (Diseño y Color)": f"{b['nombre']} — {b.get('diseno','')} ({b['color']})",
                "Calzado": f"{s['nombre']} — {s.get('diseno','')} ({s['color']})",
                "Compatibilidad": calcular_armonia_colores(t.get('hex', '#FFF'), b.get('hex', '#000'))
            })
        st.dataframe(pd.DataFrame(filas_agenda), use_container_width=True, hide_index=True)

# --- TAB 6: ASISTENTE IA ---
with tabs[5]:
    st.header("🤖 Asistente de Estilo IA (Conectado a tu Avatar 3D)")
    for m in st.session_state.mensajes_ia:
        with st.chat_message(m["rol"]):
            st.write(m["texto"])

    pregunta = st.chat_input("Ej: Recomiéndame un outfit formal y vístelo en el avatar 3D...")
    if pregunta:
        st.session_state.mensajes_ia.append({"rol": "user", "texto": pregunta})
        with st.chat_message("user"):
            st.write(pregunta)

        sug_top = random.choice(tops)
        sug_bot = random.choice(bottoms)
        sug_sho = random.choice(shoes)
        # Actualiza automáticamente el avatar 3D con lo que recomendó la IA
        st.session_state.outfit_3d = {"top": sug_top, "bottom": sug_bot, "shoes": sug_sho}

        alt_u = st.session_state.perfil.get("altura_cm", 165)
        gen_u = st.session_state.perfil.get("genero", "Femenino")

        resp = (
            f"¡Listo! He actualizado tu **Avatar 3D** con esta recomendación para tu perfil **{gen_u}** ({alt_u} cm, silueta **{st.session_state.perfil.get('cuerpo')}**):\n\n"
            f"- 👕 **Superior:** {sug_top['nombre']} (*{sug_top.get('diseno')}*, color *{sug_top.get('color')}*)\n"
            f"- 👖 **Inferior:** {sug_bot['nombre']} (*{sug_bot.get('diseno')}*, color *{sug_bot.get('color')}*)\n"
            f"- 👞 **Calzado:** {sug_sho['nombre']} (*{sug_sho.get('diseno')}*)\n\n"
            f"Ve a la pestaña **Recomendador 3D** para girarlo 360° y ver cómo te queda."
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
