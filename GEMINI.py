import streamlit as st
import requests
from datetime import datetime
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="ND Hub - Dream Assistant", 
    page_icon="🍀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CONFIGURACIÓN DE GEMINI (ELIMINAR ERROR 404) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Usamos 'gemini-pro' a secas, sin números de versión. 
    # Es el nombre más estable y compatible con la API v1.
    try:
        model = genai.GenerativeModel('gemini-pro')
        # Hacemos una mini prueba silenciosa
        model.generate_content("ok")
        st.success("🍀 Dream Assistant Conectado")
    except Exception as e:
        # Si 'gemini-pro' falla, intentamos la versión flash más básica
        try:
            model = genai.GenerativeModel('gemini-1.5-flash-8b')
            st.success("🍀 Dream Assistant Conectado (Modo Lite)")
        except:
            st.error(f"⚠️ Error crítico de API: {e}")
            model = None
else:
    st.error("⚠️ No se encontró la clave en Secrets.")
    model = None
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
        "analisis_pred": "🧠 Análisis de Gemini IA",
        "ideas_header": "💡 Ideas para 'Buy / Sell / Hold'",
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
        "analisis_pred": "🧠 Gemini AI Analysis",
        "ideas_header": "💡 'Buy / Sell / Hold' Ideas",
        "link_team": "TeamRankings", "link_cfb": "CFBStats"
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

# 5. FUNCIÓN DE INTELIGENCIA (EL CORAZÓN DE LA IA)
def analizar_con_ia(datos_crudos, pregunta_usuario):
    if model:
        # Convertimos los datos JSON a texto plano para la IA
        contexto = str(datos_crudos)[:7000] # Limitamos para no saturar a la IA
        
        # Le damos instrucciones MUY claras para que no invente
        prompt_final = f"""
        Actúa como un experto analista deportivo de los Notre Dame Fighting Irish.
        DATOS REALES DE ESPN: {contexto}
        
        PREGUNTA DEL USUARIO: {pregunta_usuario}
        
        REGLAS:
        1. Responde en {seleccion}.
        2. Si la respuesta está en los datos, sé preciso (nombres, números, posiciones).
        3. Si no encuentras la información, di: 'No tengo ese dato específico en los registros actuales de ESPN'.
        4. Sé profesional y apasionado por Notre Dame.
        """
        try:
            response = model.generate_content(prompt_final)
            return response.text
        except Exception as e:
            return f"Error al procesar con IA: {e}"
    return "IA no configurada correctamente en Streamlit."

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
        # Lógica de extracción de métricas clave
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
        with st.expander(t["desglose"]):
            for cat in categorias:
                st.write(f"**{cat['displayName']}**")
                for s in cat['stats']: st.write(f"- {s['displayName']}: {s['displayValue']}")

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

# --- TAB 4: MORNING NOTE (IA GENERATIVA) ---
with tab4:
    st.header(t["prep_header"])
    if st.button(t["boton_guion"], type="primary"):
        with st.spinner('Gemini IA está redactando el guion...'):
            datos_m = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
            if datos_m:
                guion_ia = analizar_con_ia(datos_m, "Genera un guion de 3 puntos clave para mi show de radio. Analiza los puntos por partido y yardas totales.")
                st.markdown(f"### 📄 Show Script IA - {datetime.now().strftime('%d/%m/%Y')}")
                st.info(guion_ia)
            else:
                st.error("No hay datos de ESPN disponibles.")

# --- SECCIÓN: CHAT INTERACTIVO (LA MEJORA) ---
st.divider()
st.subheader("🤖 Pregunta al Dream Assistant")
# Usamos chat_input que es más moderno y bonito
user_question = st.chat_input("Ejemplo: ¿Quién es el líder en touchdowns?")

if user_question:
    # Mostramos lo que tú preguntaste
    with st.chat_message("user"):
        st.write(user_question)
        
    # La IA responde
    with st.spinner('Consultando con los servidores de ESPN...'):
        # Le enviamos las estadísticas completas para que tenga contexto
        datos_completos = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
        respuesta = analizar_con_ia(datos_completos, user_question)
        
        with st.chat_message("assistant", avatar="🍀"):
            st.write(respuesta)
