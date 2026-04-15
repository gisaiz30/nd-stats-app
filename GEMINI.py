import streamlit as st
import requests
from datetime import datetime
from groq import Groq

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="ND Hub - Dream Assistant", 
    page_icon="🍀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CONFIGURACIÓN DE IA (GROQ) ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    st.success("🍀 Dream Assistant (Groq) Conectado")
else:
    st.error("⚠️ No se encontró la clave GROQ_API_KEY en los Secrets.")
    client = None

# --- DICCIONARIO DE IDIOMAS ---
idiomas = {
    "Español": {
        "titulo": "🍀 Panel de Control Notre Dame",
        "tab1": "Estadísticas", "tab2": "Jugadores", "tab3": "Compromisos", "tab4": "Morning Note 🎙️",
        "boton": "🔄 Actualizar ahora", "resumen": "Resumen de Temporada",
        "pase": "Yardas Pase", "tierra": "Yardas Tierra", "puntos": "Puntos Totales",
        "desglose": "Desglose Completo", "fuentes": "Fuentes Externas",
        "prep_header": "🌅 Morning Note: Guion del Show",
        "prep_desc": "Generación automática de puntos clave para el show.",
        "boton_guion": "🚀 Generar Guion con IA",
    },
    "English": {
        "titulo": "🍀 Notre Dame Command Center",
        "tab1": "Stats", "tab2": "Roster", "tab3": "Commitments", "tab4": "Morning Note 🎙️",
        "boton": "🔄 Refresh Now", "resumen": "Season Summary",
        "pase": "Passing Yards", "tierra": "Rushing Yards", "puntos": "Total Points",
        "desglose": "Full Breakdown", "fuentes": "External Sources",
        "prep_header": "🌅 Morning Note: Show Script",
        "prep_desc": "Automatic generation of show key points.",
        "boton_guion": "🚀 Generate AI Script",
    }
}

# 3. SELECTOR DE IDIOMA
st.sidebar.title("Configuración")
seleccion = st.sidebar.selectbox("Idioma / Language", list(idiomas.keys()))
t = idiomas[seleccion]

# 4. LÓGICA DE DATOS
@st.cache_data(ttl=300) # Reducido a 5 min para mayor frescura
def obtener_datos(url):
    try:
        r = requests.get(url)
        return r.json()
    except: return None

# 5. FUNCIÓN DE INTELIGENCIA (PROMPT DE HIERRO 2026)
def analizar_con_ia(datos_crudos, pregunta_usuario):
    if client:
        # Forzamos la fecha y el contexto en el mensaje
        fecha_actual = datetime.now().strftime('%d/%m/%Y')
        contexto = f"FECHA DEL SISTEMA: {fecha_actual}\nDATOS EN TIEMPO REAL: {str(datos_crudos)[:7000]}"
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system", 
                        "content": f"""Eres el analista oficial de Notre Dame. 
                        REGLA CRÍTICA: Ignora tu base de datos de entrenamiento (2023). 
                        SOLO usa los 'DATOS EN TIEMPO REAL' proporcionados. Estamos en el año 2026.
                        Si los datos no mencionan algo, di que no está en el reporte de ESPN.
                        Responde siempre en {seleccion} con tono profesional y apasionado."""
                    },
                    {"role": "user", "content": f"{contexto}\n\nPREGUNTA: {pregunta_usuario}"}
                ],
                temperature=0.1 # Muy bajo para evitar alucinaciones
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error al procesar con Groq: {e}"
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

# --- TAB 4: MORNING NOTE (MULTIFUENTE) ---
with tab4:
    st.header(t["prep_header"])
    if st.button(t["boton_guion"], type="primary"):
        with st.spinner('Analizando estadísticas y noticias para el show...'):
            s_datos = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
            n_datos = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/news")
            
            guion = analizar_con_ia(
                {"stats": s_datos, "news": n_datos}, 
                "Genera un guion de 3 puntos clave para mi show de radio. Incluye un análisis de los números actuales y menciona las noticias más recientes."
            )
            st.markdown(f"### 📄 Show Script IA - {datetime.now().strftime('%d/%m/%Y')}")
            st.info(guion)

# --- SECCIÓN: CHAT INTERACTIVO (MULTIFUENTE) ---
st.divider()
st.subheader("🤖 Pregunta al Dream Assistant")
user_question = st.chat_input("Ejemplo: ¿Qué dicen las últimas noticias sobre los jugadores?")

if user_question:
    with st.chat_message("user"):
        st.write(user_question)
        
    with st.spinner('Consultando ESPN Stats + News...'):
        espn_stats = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
        espn_news = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/news")
        
        mega_contexto = {
            "estadisticas": espn_stats,
            "noticias": espn_news,
            "fecha_hoy": datetime.now().strftime('%d/%m/%Y')
        }
        
        respuesta = analizar_con_ia(mega_contexto, user_question)
        
        with st.chat_message("assistant", avatar="🍀"):
            st.write(respuesta)
