import streamlit as st
import google.generativeai as genai
import requests
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser lo primero de Streamlit)
st.set_page_config(
    page_title="ND Hub - Dream Assistant", 
    page_icon="🍀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CONFIGURACIÓN DE GEMINI (Global)
# Buscamos la clave en los Secrets de la web de Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Error: No se encontró 'GEMINI_API_KEY' en los Secrets de Streamlit.")
    st.stop() # Detiene la app si no hay clave

# 3. DICCIONARIO DE IDIOMAS
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
        "prep_desc": "Automatic generation of key points for the 8:00 AM show.",
        "boton_guion": "🚀 Generate AI Script",
        "analisis_pred": "🧠 Gemini Analysis",
        "ideas_header": "💡 'Buy / Sell / Hold' Ideas",
        "idea1": "Is ND's defense the best of the Freeman era?",
        "idea2": "Projection: Impact of new commitments.",
        "idea3": "Analysis: Third-down performance.",
        "link_team": "TeamRankings", "link_cfb": "CFBStats"
    }
}

# SELECTOR DE IDIOMA (Barra lateral)
st.sidebar.title("Configuración")
seleccion = st.sidebar.selectbox("Idioma / Language", list(idiomas.keys()))
t = idiomas[seleccion]

# 4. FUNCIONES DE AYUDA (Helper Functions)
@st.cache_data(ttl=600)
def obtener_datos(url):
    try:
        r = requests.get(url)
        return r.json()
    except:
        return None

def chat_con_ia(consulta_usuario, datos_contexto):
    # Acortamos los datos para no pasarnos del límite de Gemini
    contexto_texto = str(datos_contexto)[:5000]
    
    instrucciones = f"""
    Eres el 'Dream Assistant', un experto analista del equipo de fútbol americano de Notre Dame.
    Tu objetivo es ayudar al equipo de producción de 'Irish Breakdown'.
    Datos actuales de ESPN: {contexto_texto}
    
    Responde a la siguiente solicitud en el idioma {seleccion}:
    {consulta_usuario}
    """
    
    try:
        response = model.generate_content(instrucciones)
        return response.text
    except Exception as e:
        return f"Error al conectar con Gemini: {str(e)}"

# 5. INTERFAZ PRINCIPAL
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
    roster = obtener_datos("
