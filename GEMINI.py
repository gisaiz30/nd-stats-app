import streamlit as st
import google.generativeai as genai
import requests
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera instrucción de Streamlit)
st.set_page_config(
    page_title="ND Hub - Dream Assistant", 
    page_icon="🍀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CONFIGURACIÓN GLOBAL DE GEMINI
if "AIzaSyAf6hgvJbjs1asVU127PXy3X2z3O2NpuiA" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # USAMOS EL NOMBRE COMPLETO DEL MODELO AQUÍ:
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
else:
    st.error("⚠️ Error: No se encontró 'GEMINI_API_KEY' en los Secrets.")
    st.stop()

# --- DICCIONARIO DE IDIOMAS ---
idiomas = {
    "Español": {
        "titulo": "🍀 Panel de Control Notre Dame",
        "tab1": "Estadísticas", "tab2": "Jugadores", "tab3": "Compromisos", "tab4": "Morning Note 🎙️",
        "boton": "🔄 Actualizar ahora", "resumen": "Resumen de Temporada",
        "pase": "Yardas Pase", "tierra": "Yardas Tierra", "puntos": "Puntos Totales",
        "desglose": "Desglose Completo", "fuentes": "Fuentes Externas",
        "prep_header": "🌅 Morning Note: Guion del Show",
        "prep_desc": "Generación automática de puntos clave para el show de las 8:00 AM.",
        "boton_guion": "🚀 Generar Guion con IA",
        "analisis_pred": "🧠 Análisis de Gemini",
        "ideas_header": "💡 Ideas para 'Buy / Sell / Hold'",
        "idea1": "¿Es la defensa de ND la mejor de la era Freeman?",
        "idea2": "Proyección: Impacto de nuevos compromisos.",
        "idea3": "Análisis: Rendimiento en terceras oportunidades.",
        "link_team": "TeamRankings", "link_cfb": "CFBStats"
    },
    "English": {
        "titulo": "🍀 Notre Dame Command Center",
        "tab1": "Stats", "tab2": "Roster", "tab3": "Commitments", "tab4": "Morning Note 🎙️",
        "boton": "🔄 Refresh Now", "resumen": "Season Summary",
        "pase": "Passing Yards", "tierra": "Rushing Yards", "puntos": "Total Points",
        "desglose": "Full Breakdown", "fuentes": "External Sources",
        "prep_header": "🌅 Morning Note: Show Script",
        "prep_desc": "Automatic generation of key points for the show.",
        "boton_guion": "🚀 Generate AI Script",
        "analisis_pred": "🧠 Gemini Analysis",
        "ideas_header": "💡 'Buy / Sell / Hold' Ideas",
        "idea1": "Is ND's defense the best of the Freeman era?",
        "idea2": "National ranking projection.",
        "idea3": "Third-down performance analysis.",
        "link_team": "TeamRankings", "link_cfb": "CFBStats"
    }
}

# SELECTOR DE IDIOMA (Barra lateral)
st.sidebar.title("Configuración")
seleccion = st.sidebar.selectbox("Idioma / Language", list(idiomas.keys()))
t = idiomas[seleccion]

# 3. FUNCIONES DE LÓGICA
@st.cache_data(ttl=600)
def obtener_datos(url):
    try:
        r = requests.get(url)
        return r.json()
    except:
        return None

def chat_con_ia(consulta_usuario, datos_contexto):
    # Acortamos los datos para no saturar a la IA
    resumen = str(datos_contexto)[:5000]
    
    instrucciones = f"""
    Eres el 'Dream Assistant', analista experto de Notre Dame Football para 'Irish Breakdown'.
    Datos de ESPN: {resumen}
    Responde en {seleccion} de forma concisa y profesional.
    """
    
    try:
        response = model.generate_content(f"{instrucciones}\n\nPregunta: {consulta_usuario}")
        return response.text
    except Exception as e:
        return f"Error en la conexión con la IA: {e}"

# 4. CUERPO PRINCIPAL
st.title(t["titulo"])

if st.button(t["boton"]):
    st.cache_data.clear()
    st.rerun()

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

with tab1:
    datos_stats = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
    if datos_stats:
        categorias = datos_stats.get('results', {}).get('stats', {}).get('categories', [])
        st.subheader(t["resumen"])
        col1, col2, col3 = st.columns(3)
        for cat in categorias:
            if cat['name'] == 'passing':
                for s in cat['stats']:
                    if s['name'] == 'netPassingYards': col1.metric(t["pase"], s['displayValue'])
            if cat['name'] == 'rushing':
                for s in cat['stats']:
                    if s['name'] == 'rushingYards': col2.metric(t["tierra"], s['displayValue'])
            if cat['name'] == 'scoring':
                for s in cat['stats']:
                    if s['name'] == 'totalPoints': col3.metric(t["puntos"], s['displayValue'])
        st.divider()
        for cat in categorias:
            with st.expander(f"📊 {cat['displayName']}"):
                for s in cat['stats']: st.write(f"**{s['displayName']}:** {s['displayValue']}")

with tab2:
    roster = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/roster")
    if roster:
        for group in roster.get('athletes', []):
            st.write(f"### {group['position']}")
            for p in group['items']:
                c1, c2 = st.columns([1, 5])
                with c1: st.image(p.get('headshot', {}).get('href', 'https://via.placeholder.com/50'), width=60)
                with c2: st.write(f"**{p['fullName']}** | #{p.get('jersey', 'N/A')}")

with tab3:
    st.subheader("Class 2026 Commitments")
    commits = [
        {"name": "Noah Grubbs", "pos": "QB", "stars": "⭐⭐⭐⭐"}, 
        {"name": "Jameson Knight", "pos": "WR", "stars": "⭐⭐⭐⭐⭐"}
    ]
    for c in commits: st.success(f"✅ {c['name']} ({c['pos']}) - {c['stars']}")

with tab4:
    st.header(t["prep_header"])
    if st.button(t["boton_guion"], type="primary"):
        with st.spinner('Gemini analizando estadísticas...'):
            datos_m = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
            guion = chat_con_ia("Genera un guion de 3 puntos clave para el show de radio.", datos_m)
            st.info(guion)
    
    st.divider()
    st.subheader(t["ideas_header"])
    st.checkbox(t["idea1"])
    st.checkbox(t["idea2"])
    st.checkbox(t["idea3"])

# --- CAJA DE CHAT INTERACTIVA ---
st.divider()
st.header("🤖 Pregunta al Dream Assistant")
input_usuario = st.chat_input("Ej: ¿Cómo va el promedio de puntos de ND?")

if input_usuario:
    with st.chat_message("user"):
        st.write(input_usuario)
    
    with st.spinner("Pensando..."):
        # Contexto fresco para el chat
        contexto_chat = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
        respuesta = chat_con_ia(input_usuario, contexto_chat)
        
        with st.chat_message("assistant", avatar="🍀"):
            st.write(respuesta)
