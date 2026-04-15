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

# Inyección de CSS personalizado para mejorar la visualización (Cartas, Colores)
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
""", unsafe_allow_stdio=True)

# ==========================================
# 2. CONEXIÓN SEGURA CON IA (GROQ 2026)
# ==========================================
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    # No mostramos éxito para limpiar la interfaz
else:
    st.error("⚠️ Crítico: Falta GROQ_API_KEY en los Secrets de Streamlit.")
    client = None

# ==========================================
# 3. LÓGICA DE DATOS Y CACHÉ (FRESCURA)
# ==========================================
@st.cache_data(ttl=300) # Datos frescos cada 5 minutos
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
    
    # Preparamos un contexto estructurado y limpio para la IA
    # Esto soluciona el error de "no sé el nombre del equipo"
    contexto_estructurado = f"""
    SISTEMA DE DATOS EN TIEMPO REAL (RAG)
    -------------------------------------
    EQUIPO: Notre Dame Fighting Irish (NCAAF College Football)
    FECHA DE HOY: {fecha_actual}
    FUENTE PRIMARIA: ESPN API
    
    REPORTES TÉCNICOS PROPORCIONADOS:
    {str(datos_contexto)[:8000]}  # Limitamos tokens
    -------------------------------------
    """
    
    # Instrucciones de comportamiento para Llama 3.1 Sonnet (Abril 2026)
    system_prompt = f"""
    Eres el 'Dream Assistant' de Notre Dame, una IA experta y apasionada en NCAAF.
    
    TUS REGLAS DE ORO:
    1. Responde SIEMPRE en {idioma}.
    2. Usa EXCLUSIVAMENTE los 'DATOS EN TIEMPO REAL' proporcionados arriba.
    3. Tu conocimiento previo (entrenamiento) está obsoleto. Estamos en ABRIL DE 2026.
    4. El equipo analizado es Notre Dame. Si ves IDs (ej. 87), asume que son de los Irish.
    5. Si los datos no contienen la respuesta, di: 'No tengo ese dato específico en los reportes actuales de ESPN'. No inventes.
    6. Sé profesional, preciso con los números y mantén el espíritu de 'Go Irish!'.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", # Modelo ultra rápido de 2026
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{contexto_estructurado}\n\nPREGUNTA DEL ANALISTA: {pregunta_usuario}"}
            ],
            temperature=0.1, # Muy bajo para máxima precisión
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error de conexión con el cerebro de IA: {e}"

# ==========================================
# 5. DICCIONARIO DE IDIOMAS Y TEXTOS
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
        "boton_guion": "🚀 Generar Guion con Llama 3.1",
        "guion_desc": "Generación de puntos clave basada en números y noticias de hoy.",
        "chat_header": "🤖 Pregunta al Dream Assistant (Notre Dame Expert)",
        "chat_placeholder": "Ej: ¿Quién es el líder en touchdowns?",
        "consultando": "Consultando fuentes en tiempo real..."
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
        "guion_desc": "Generation of key points based on numbers and news.",
        "chat_header": "🤖 Ask the Dream Assistant (Notre Dame Expert)",
        "chat_placeholder": "Ex: Who is leading in touchdowns?",
        "consultando": "Consulting real-time sources..."
    }
}

# ==========================================
# 6. BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/Notre_Dame_Fighting_Irish_logo.svg/1200px-Notre_Dame_Fighting_Irish_logo.svg.png", width=100)
    st.title(textos["Español"]["sidebar_config"]) # Usamos español por defecto aquí
    
    # Selector de Idioma
    idioma_sel = st.selectbox(textos["Español"]["idioma"], list(textos.keys()))
    t = textos[idioma_sel]
    
    st.divider()
    
    # Botón de Actualización
    if st.button(t["update_btn"], use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.divider()
    
    # Enlaces Útiles
    st.subheader(t["fuentes"])
    st.link_button("📊 TeamRankings", "https://www.teamrankings.com/ncf/team/notre-dame-fighting-irish/stats", use_container_width=True)
    st.link_button("📈 CFBStats", "http://www.cfbstats.com/2025/team/513/index.html", use_container_width=True)
    st.link_button("🗞️ ESPN News", "https://www.espn.com/college-football/team/_/id/87/notre-dame-fighting-irish", use_container_width=True)

# ==========================================
# 7. INTERFAZ PRINCIPAL (MAIN BODY)
# ==========================================
st.title(t["main_title"])
st.write(f"📅 **{datetime.now().strftime('%d/%m/%Y | %H:%M')}**")

tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# URLS de API ESPN
URL_STATS = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics"
URL_ROSTER = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/roster"
URL_NEWS = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/news"

# --- TAB 1: ESTADÍSTICAS (VISUAL) ---
with tab1:
    with st.spinner(t["consultando"]):
        datos_stats = obtener_datos_api(URL_STATS)
        
    if datos_stats:
        st.subheader(t["resumen"])
        
        # Procesamiento de métricas clave (Big Numbers)
        categorias = datos_stats.get('results', {}).get('stats', {}).get('categories', [])
        net_passing = "N/A"; net_rushing = "N/A"; total_points = "N/A"
        
        for cat in categorias:
            for s in cat.get('stats', []):
                if s['name'] == 'netPassingYards': net_passing = s['displayValue']
                if s['name'] == 'rushingYards': net_rushing = s['displayValue']
                if s['name'] == 'totalPoints': total_points = s['displayValue']
        
        # Diseño de Columnas para Métricas Visuales
        col1, col2, col3 = st.columns(3)
        with col1: st.metric(label=t["pase"], value=net_passing)
        with col2: st.metric(label=t["tierra"], value=net_rushing)
        with col3: st.metric(label=t["puntos"], value=total_points)
        
        st.divider()
        
        # Desglose Técnico detallado (Expander)
        with st.expander(f"📊 {t['desglose']}"):
            for cat in categorias:
                st.markdown(f"### {cat['displayName']}")
                cols = st.columns(2)
                for i, s in enumerate(cat.get('stats', [])):
                    cols[i%2].markdown(f"**{s['displayName']}:** {s['displayValue']}")

# --- TAB 2: ROSTER (DISEÑO DE CARTAS) ---
with tab2:
    with st.spinner(t["consultando"]):
        roster = obtener_datos_api(URL_ROSTER)
        
    if roster:
        # Mostramos los grupos de posiciones
        for group in roster.get('athletes', []):
            st.markdown(f"## 🏈 {group['position']}")
            
            # Grilla de 2 columnas para jugadores
            cols = st.columns(2)
            for i, p in enumerate(group.get('items', [])):
                with cols[i % 2]:
                    # Contenedor visual tipo "nd-card"
                    st.markdown(f"""
                    <div class="nd-card">
                        <img src="{p.get('headshot', {}).get('href', 'https://via.placeholder.com/60')}" width="60" style="border-radius:50%; float:left; margin-right:15px;">
                        <h3>{p['fullName']} | #{p.get('jersey', 'N/A')}</h3>
                        <p><b>Pos:</b> {p.get('position', {}).get('abbreviation', 'N/A')}</p>
                        <p><b>HT/WT:</b> {p.get('displayHeight', 'N/A')} / {p.get('displayWeight', 'N/A')} lbs</p>
                        <p><b>Class:</b> {p.get('experience', {}).get('displayValue', 'N/A')}</p>
                        <div style="clear:both;"></div>
                    </div>
                    """, unsafe_allow_stdio=True)

# --- TAB 3: NOTICIAS (FORMATO LIMPIO) ---
with tab3:
    with st.spinner(t["consultando"]):
        noticias = obtener_datos_api(URL_NEWS)
        
    if noticias:
        articles = noticias.get('articles', [])
        for art in articles:
            # Diseño de tarjeta para noticia
            st.markdown(f"""
            <div class="nd-card">
                <img src="{art.get('images', [{}])[0].get('url', 'https://via.placeholder.com/150')}" width="150" style="border-radius:8px; float:right; margin-left:15px; margin-bottom:10px;">
                <h3><a href="{art.get('links', {}).get('web', {}).get('href', '#')}" target="_blank" style="text-decoration:none; color:#0C2340;">{art['headline']}</a></h3>
                <p style="color:#888; font-size:0.9rem;">🕒 {art.get('published', 'N/A')[:10]}</p>
                <p>{art.get('description', '')}</p>
                <div style="clear:both;"></div>
            </div>
            """, unsafe_allow_stdio=True)

# --- TAB 4: MORNING NOTE (GENERACIÓN IA MULTIFUENTE) ---
with tab4:
    st.header(t["prep_header"])
    st.write(t["guion_desc"])
    
    if st.button(t["boton_guion"], type="primary"):
        with st.spinner('Dream Assistant analizando datos y noticias actuales...'):
            # Obtenemos ambas fuentes de datos para un análisis completo
            s_datos = obtener_datos_api(URL_STATS)
            n_datos = obtener_datos_api(URL_NEWS)
            
            # Empaquetamos el contexto para la IA
            contexto_m = {"estadisticas": s_datos, "noticias": n_datos}
            
            # Generación del guion con Groq Llama 3.1
            pregunta_guion = "Genera un guion de 3 puntos clave para mi show de radio de hoy. Haz un análisis profundo de los números actuales de la temporada 2025 y comenta las noticias más recientes relevantes para el equipo."
            guion = preguntar_al_assistant(contexto_m, pregunta_guion, idioma_sel)
            
            # Visualización del Guion
            st.markdown(f"### 📄 Show Script IA - {datetime.now().strftime('%d/%m/%Y')}")
            st.info(guion)

# ==========================================
# 8. SECCIÓN: CHAT INTERACTIVO (PIE DE PÁGINA)
# ==========================================
st.divider()
st.subheader(f"💬 {t['chat_header']}")

# Componente chat_input moderno
user_question = st.chat_input(t["chat_placeholder"])

if user_question:
    # Mostramos pregunta del usuario
    with st.chat_message("user"):
        st.write(user_question)
        
    # La IA responde con contexto multifuente fresco
    with st.spinner(t["consultando"]):
        # Obtenemos datos frescos justo antes de responder
        stats_c = obtener_datos_api(URL_STATS)
        news_c = obtener_datos_api(URL_NEWS)
        mega_contexto = {"stats": stats_c, "news": news_c}
        
        # Llamada a Groq Llama 3.1 (Abril 2026 Blindado)
        respuesta = preguntar_al_assistant(mega_contexto, user_question, idioma_sel)
        
        with st.chat_message("assistant", avatar="🍀"):
            st.write(respuesta)
