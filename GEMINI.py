import streamlit as st
import requests
from datetime import datetime
import google.generativeai as genai  # <--- 1. AÑADIMOS LA LIBRERÍA DE GOOGLE

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="ND Hub - Dream Assistant", 
    page_icon="🍀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CONFIGURACIÓN DE GEMINI ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Intentamos primero con la versión más compatible de todas
    try:
        # 'gemini-1.5-flash' es el estándar actual
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        # Si da error 404, usamos el modelo Pro que es infalible
        model = genai.GenerativeModel('gemini-pro')
        
    st.success("✅ Conexión con IA establecida")
else:
    st.error("⚠️ Falta la configuración de 'GEMINI_API_KEY' en los Secrets de Streamlit.")
    model = None
# --- DICCIONARIO DE IDIOMAS ---
idiomas = {
    "Español": {
        "titulo": "🍀 Panel de Control Notre Dame",
        "tab1": "Estadísticas", "tab2": "Jugadores", "tab3": "Compromisos", "tab4": "Morning Note 🎙️",
        "boton": "🔄 Actualizar ahora", "resumen": "Resumen de Temporada",
        "pase": "Yardas Pase", "tierra": "Yardas Tierra", "puntos": "Puntos Totales",
        "desglose": "Desglose Completo", "fuentes": "Fuentes Externas", "trending": "Tendencias en X",
        "prep_header": "🌅 Morning Note: Guion del Show",
        "prep_desc": "Generación automática de puntos clave para el show de las 8:00 AM.",
        "boton_guion": "🚀 Generar Guion con IA", # <--- Cambiamos el nombre
        "ideas_header": "💡 Ideas para 'Buy / Sell / Hold'",
        "link_team": "TeamRankings", "link_cfb": "CFBStats", "link_x": "Noticias X",
        "analisis_pred": "🧠 Análisis de Gemini IA", # <--- Cambiamos el nombre
        "idea1": "¿Es la defensa de ND la mejor de la era Freeman?",
        "idea2": "Proyección: Impacto de los nuevos compromisos.",
        "idea3": "Análisis: Rendimiento en terceras oportunidades."
    },
    "English": {
        "titulo": "🍀 Notre Dame Command Center",
        "tab1": "Stats", "tab2": "Roster", "tab3": "Commitments", "tab4": "Morning Note 🎙️",
        "boton": "🔄 Refresh Now", "resumen": "Season Summary",
        "pase": "Passing Yards", "tierra": "Rushing Yards", "puntos": "Total Points",
        "desglose": "Full Breakdown", "fuentes": "External Sources", "trending": "X Trends",
        "prep_header": "🌅 Morning Note: Show Script",
        "prep_desc": "Automatic generation of key points for the 8:00 AM show.",
        "boton_guion": "🚀 Generate AI Script",
        "ideas_header": "💡 'Buy / Sell / Hold' Ideas",
        "link_team": "TeamRankings", "link_cfb": "CFBStats", "link_x": "X News",
        "analisis_pred": "🧠 Gemini AI Analysis",
        "idea1": "Is ND's defense the best of the Freeman era?",
        "idea2": "Projection: Impact of new commitments.",
        "idea3": "Analysis: Third-down performance."
    }
}

# 3. SELECTOR DE IDIOMA
st.sidebar.title("Configuración")
seleccion = st.sidebar.selectbox("Idioma / Language", list(idiomas.keys()))
t = idiomas[seleccion]

st.sidebar.divider()
st.sidebar.subheader(t["fuentes"])
st.sidebar.link_button(f"📊 {t['link_team']}", "https://www.teamrankings.com/ncf/team/notre-dame-fighting-irish/stats")
st.sidebar.link_button(f"📈 {t['link_cfb']}", "http://www.cfbstats.com/2025/team/513/index.html")

# 4. LÓGICA DE DATOS
@st.cache_data(ttl=600)
def obtener_datos(url):
    try:
        r = requests.get(url)
        return r.json()
    except: return None

# 5. FUNCIÓN PARA QUE GEMINI ANALICE LOS DATOS
def analizar_con_ia(datos_crudos, pregunta_usuario):
    if model:
        # Simplificamos los datos para que Gemini no se confunda
        contexto = str(datos_crudos)[:5000] 
        prompt = f"Eres un experto analista de fútbol de Notre Dame. Basándote en estos datos de ESPN: {contexto}. {pregunta_usuario}"
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error de IA: {e}"
    return "IA no configurada."

# 6. CUERPO PRINCIPAL
st.title(t["titulo"])

if st.button(t["boton"]):
    st.cache_data.clear()
    st.rerun()

tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# --- TAB 1: ESTADÍSTICAS ---
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
        st.write(f"### {t['desglose']}")
        for cat in categorias:
            with st.expander(f"📊 {cat['displayName']}"):
                for s in cat['stats']: st.write(f"**{s['displayName']}:** {s['displayValue']}")

# --- TAB 2: JUGADORES ---
with tab2:
    roster = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/roster")
    if roster:
        for group in roster.get('athletes', []):
            st.write(f"### {group['position']}")
            for p in group['items']:
                c1, c2 = st.columns([1, 5])
                with c1: st.image(p.get('headshot', {}).get('href', 'https://via.placeholder.com/50'), width=60)
                with c2: st.write(f"**{p['fullName']}** | #{p.get('jersey', 'N/A')}")

# --- TAB 3: RECRUITING ---
with tab3:
    st.subheader("Class 2026 Commitments")
    commits = [{"name": "Noah Grubbs", "pos": "QB", "stars": "⭐⭐⭐⭐"}, {"name": "Jameson Knight", "pos": "WR", "stars": "⭐⭐⭐⭐⭐"}]
    for c in commits: st.success(f"✅ {c['name']} ({c['pos']}) - {c['stars']}")

# --- TAB 4: MORNING NOTE (AQUÍ ESTÁ LA IA) ---
with tab4:
    st.header(t["prep_header"])
    st.write(t["prep_desc"])
    
    if st.button(t["boton_guion"], type="primary"):
        with st.spinner('Gemini IA está analizando las estadísticas de ESPN...'):
            # Traemos datos frescos para la IA
            datos_m = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
            
            if datos_m:
                # LLAMADA A GEMINI: Le pedimos que cree el guion basado en datos reales
                pregunta = "Genera un guion para mi show de radio de hoy. Incluye un análisis de los puntos por partido y una predicción breve basada en las yardas de pase y tierra actuales."
                guion_ia = analizar_con_ia(datos_m, pregunta)
                
                st.markdown(f"### 📄 Show Script IA - {datetime.now().strftime('%d/%m/%Y')}")
                st.info(guion_ia) # Mostramos lo que dice Gemini
            else:
                st.error("No se pudieron obtener datos para el análisis.")

    st.divider()
    st.subheader(t["ideas_header"])
    st.checkbox(t["idea1"])
    st.checkbox(t["idea2"])
    st.checkbox(t["idea3"])

# --- SECCIÓN EXTRA: CHAT ABIERTO CON LA IA ---
st.divider()
st.subheader("🤖 Pregunta lo que quieras al Dream Assistant")
user_question = st.text_input("Ejemplo: ¿Quién es el mejor jugador del equipo según sus stats?")
if user_question:
    with st.spinner('Consultando a Gemini...'):
        datos_chat = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
        respuesta = analizar_con_ia(datos_chat, user_question)
        st.write(respuesta)
