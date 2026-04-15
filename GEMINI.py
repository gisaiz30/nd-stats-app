import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from groq import Groq

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="ND Hub | Dream Assistant",
    page_icon="🍀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de CSS corregida (parámetro unsafe_allow_html=True)
st.markdown("""
<style>
    /* Colores Principales ND: Azul Marino (#0C2340) y Oro (#C99700) */
    .stApp { background-color: #f4f6f9; }
    
    /* Estilo para las tarjetas de métricas */
    [data-testid="stMetricValue"] { font-size: 2.5rem !important; color: #0C2340; font-weight: 700; }
    [data-testid="stMetricLabel"] { font-size: 1.1rem !important; color: #666; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Tarjetas personalizadas para jugadores y noticias */
    .nd-card {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; border-left: 5px solid #C99700;
    }
    .nd-card h3 { color: #0C2340; margin-top: 0; }
    .nd-card p { color: #555; margin-bottom: 5px; }
    
    /* Títulos de Tabs y Secciones */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem; font-weight: 600; color: #0C2340;
    }
    h1, h2, h3 { color: #0C2340; font-family: 'Inter', sans-serif; }
    
    /* Botón Principal */
    .stButton>button {
        background-color: #0C2340; color: white; border-radius: 8px;
        border: none; padding: 10px 20px; font-weight: 600;
    }
    .stButton>button:hover { background-color: #1a3a61; color: #C99700; border: 1px solid #C99700; }
    
    /* Avatar del Chat */
    [data-testid="chatAvatarIcon-user"] { background-color: #0C2340; }
    [data-testid="chatAvatarIcon-assistant"] { background-color: #C99700; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CONEXIÓN SEGURA CON IA (GROQ 2026)
# ==========================================
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Crítico: Falta GROQ_API_KEY en los Secrets de Streamlit.")
    client = None

# ==========================================
# 3. LÓGICA DE DATOS Y CACHÉ
# ==========================================
@st.cache_data(ttl=300)
def obtener_datos_api(url):
    try:
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else None
    except: return None

# ==========================================
# 4. FUNCIÓN MAESTRA DE IA (RAG INTELIGENTE)
# ==========================================
def preguntar_al_assistant(datos_contexto, pregunta_usuario, idioma):
    if not client: return "IA no configurada."
    
    fecha_actual = datetime.now().strftime('%d/%m/%Y')
    
    contexto_estructurado = f"""
    SISTEMA DE DATOS EN TIEMPO REAL (RAG)
    -------------------------------------
    EQUIPO: Notre Dame Fighting Irish (NCAAF College Football)
    FECHA DE HOY: {fecha_actual}
    FUENTE PRIMARIA: ESPN API
    REPORTES TÉCNICOS: {str(datos_contexto)[:8000]}
    -------------------------------------
    """
    
    system_prompt = f"""
    Eres el 'Dream Assistant' de Notre Dame. 
    REGLAS:
    1. Responde SIEMPRE en {idioma}.
    2. Usa SOLO los datos proporcionados. Estamos en ABRIL DE 2026.
    3. El equipo analizado es Notre Dame. Los IDs de ESPN (como 87) son de los Irish.
    4. Si no sabes algo, dilo, no inventes.
    5. Sé profesional y usa tono de analista deportivo.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{contexto_estructurado}\n\nPREGUNTA: {pregunta_usuario}"}
            ],
            temperature=0.1,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# ==========================================
# 5. DICCIONARIO DE IDIOMAS
# ==========================================
textos = {
    "Español": {
        "sidebar_config": "⚙️ Configuración", "idioma": "Idioma / Language",
        "fuentes": "📊 Fuentes Externas", "update_btn": "🔄 Actualizar Datos",
        "main_title": "Notre Dame Football | 🍀 Panel Central",
        "tab1": "📊 Estadísticas", "tab2": "🏈 Roster", "tab3": "🗞️ Noticias", "tab4": "🎙️ Morning Note",
        "resumen": "Resumen de Temporada 2025-2026",
        "pase": "Yardas Pase", "tierra": "Yardas Tierra", "puntos": "Puntos Totales",
        "desglose": "Estadísticas Detalladas",
        "prep_header": "🌅 Guion Automático para el Show",
        "boton_guion": "🚀 Generar Guion con IA",
        "guion_desc": "Generación de puntos clave basada en números y noticias de hoy.",
        "chat_header": "🤖 Pregunta al Dream Assistant",
        "chat_placeholder": "Ej: ¿Quién lidera el equipo en yardas?",
        "consultando": "Consultando fuentes..."
    },
    "English": {
        "sidebar_config": "⚙️ Configuration", "idioma": "Language / Idioma",
        "fuentes": "📊 External Sources", "update_btn": "🔄 Refresh Data",
        "main_title": "Notre Dame Football | 🍀 Command Center",
        "tab1": "📊 Stats", "tab2": "🏈 Roster", "tab3": "🗞️ News", "tab4": "🎙️ Morning Note",
        "resumen": "2025-2026 Season Summary",
        "pase": "Passing Yards", "tierra": "Rushing Yards", "puntos": "Total Points",
        "desglose": "Detailed Breakdown",
        "prep_header": "🌅 Automatic Show Script",
        "boton_guion": "🚀 Generate AI Script",
        "guion_desc": "Key points generation based on today's data.",
        "chat_header": "🤖 Ask the Dream Assistant",
        "chat_placeholder": "Ex: Who is the passing leader?",
        "consultando": "Consulting real-time sources..."
    }
}

# ==========================================
# 6. BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/Notre_Dame_Fighting_Irish_logo.svg/1200px-Notre_Dame_Fighting_Irish_logo.svg.png", width=100)
    idioma_sel = st.selectbox("Idioma", list(textos.keys()))
    t = textos[idioma_sel]
    
    if st.button(t["update_btn"], use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.divider()
    st.subheader(t["fuentes"])
    st.link_button("📊 TeamRankings", "https://www.teamrankings.com/ncf/team/notre-dame-fighting-irish/stats", use_container_width=True)
    st.link_button("🗞️ ESPN News", "https://www.espn.com/college-football/team/_/id/87/notre-dame-fighting-irish", use_container_width=True)

# ==========================================
# 7. INTERFAZ PRINCIPAL
# ==========================================
st.title(t["main_title"])
st.write(f"📅 **{datetime.now().strftime('%d/%m/%Y')}**")

tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

URL_STATS = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics"
URL_ROSTER = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/roster"
URL_NEWS = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/news"

# --- TAB 1: ESTADÍSTICAS ---
with tab1:
    datos_stats = obtener_datos_api(URL_STATS)
    if datos_stats:
        st.subheader(t["resumen"])
        categorias = datos_stats.get('results', {}).get('stats', {}).get('categories', [])
        net_p = "N/A"; net_r = "N/A"; pts = "N/A"
        for cat in categorias:
            for s in cat.get('stats', []):
                if s['name'] == 'netPassingYards': net_p = s['displayValue']
                if s['name'] == 'rushingYards': net_r = s['displayValue']
                if s['name'] == 'totalPoints': pts = s['displayValue']
        
        c1, c2, c3 = st.columns(3)
        c1.metric(t["pase"], net_p)
        c2.metric(t["tierra"], net_r)
        c3.metric(t["puntos"], pts)
        
        with st.expander(t["desglose"]):
            for cat in categorias:
                st.markdown(f"**{cat['displayName']}**")
                for s in cat.get('stats', []):
                    st.write(f"- {s['displayName']}: {s['displayValue']}")

# --- TAB 2: ROSTER ---
with tab2:
    roster = obtener_datos_api(URL_ROSTER)
    if roster:
        for group in roster.get('athletes', []):
            st.markdown(f"### {group['position']}")
            cols = st.columns(2)
            for i, p in enumerate(group.get('items', [])):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="nd-card">
                        <img src="{p.get('headshot', {}).get('href', 'https://via.placeholder.com/60')}" width="60" style="border-radius:50%; float:left; margin-right:15px;">
                        <h3>{p['fullName']} | #{p.get('jersey', 'N/A')}</h3>
                        <p><b>HT/WT:</b> {p.get('displayHeight', 'N/A')} / {p.get('displayWeight', 'N/A')} lbs</p>
                        <div style="clear:both;"></div>
                    </div>
                    """, unsafe_allow_html=True)

# --- TAB 3: NOTICIAS ---
with tab3:
    noticias = obtener_datos_api(URL_NEWS)
    if noticias:
        for art in noticias.get('articles', []):
            st.markdown(f"""
            <div class="nd-card">
                <h3>{art['headline']}</h3>
                <p>{art.get('description', '')}</p>
                <a href="{art.get('links', {}).get('web', {}).get('href', '#')}" target="_blank">Leer más</a>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 4: MORNING NOTE ---
with tab4:
    st.header(t["prep_header"])
    if st.button(t["boton_guion"], type="primary"):
        with st.spinner('Redactando guion...'):
            s = obtener_datos_api(URL_STATS)
            n = obtener_datos_api(URL_NEWS)
            res = preguntar_al_assistant({"stats": s, "news": n}, "Genera un guion de 3 puntos para radio.", idioma_sel)
            st.info(res)

# --- CHAT ---
st.divider()
st.subheader(t["chat_header"])
user_input = st.chat_input(t["chat_placeholder"])
if user_input:
    with st.chat_message("user"): st.write(user_input)
    with st.spinner(t["consultando"]):
        s_c = obtener_datos_api(URL_STATS)
        n_c = obtener_datos_api(URL_NEWS)
        ans = preguntar_al_assistant({"stats": s_c, "news": n_c}, user_input, idioma_sel)
        with st.chat_message("assistant", avatar="🍀"): st.write(ans)
