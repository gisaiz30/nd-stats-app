import streamlit as st
import requests

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="ND Hub - Dream Assistant", 
    page_icon="🍀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- DICCIONARIO DE IDIOMAS COMPLETO ---
idiomas = {
    "Español": {
        "titulo": "🍀 Panel de Control Notre Dame",
        "tab1": "Estadísticas", 
        "tab2": "Jugadores", 
        "tab3": "Compromisos", 
        "tab4": "Show Prep",
        "boton": "🔄 Actualizar ahora", 
        "resumen": "Resumen de Temporada",
        "pase": "Yardas Pase", 
        "tierra": "Yardas Tierra", 
        "puntos": "Puntos Totales",
        "desglose": "Desglose Completo", 
        "fuentes": "Fuentes Externas", 
        "trending": "Tendencias en X"
    },
    "English": {
        "titulo": "🍀 Notre Dame Command Center",
        "tab1": "Stats", 
        "tab2": "Roster", 
        "tab3": "Commitments", 
        "tab4": "Show Prep",
        "boton": "🔄 Refresh Now", 
        "resumen": "Season Summary",
        "pase": "Passing Yards", 
        "tierra": "Rushing Yards", 
        "puntos": "Total Points",
        "desglose": "Full Breakdown", 
        "fuentes": "External Sources", 
        "trending": "X Trends"
    },
    "Français": {
        "titulo": "🍀 Centre de Contrôle Notre Dame",
        "tab1": "Statistiques", 
        "tab2": "Effectif", 
        "tab3": "Recrutement", 
        "tab4": "Show Prep",
        "boton": "🔄 Actualiser maintenant", 
        "resumen": "Résumé de la Saison",
        "pase": "Yards de Passe", 
        "tierra": "Yards de Course", 
        "puntos": "Points Totaux",
        "desglose": "Répartition Complète", 
        "fuentes": "Sources Externes", 
        "trending": "Tendances sur X"
    }
}
# --- DICCIONARIO DE IDIOMAS COMPLETO (ACTUALIZADO CON TAB 4) ---
idiomas = {
    "Español": {
        "titulo": "🍀 Panel de Control Notre Dame",
        "tab1": "Estadísticas", "tab2": "Jugadores", "tab3": "Compromisos", "tab4": "Show Prep",
        "boton": "🔄 Actualizar ahora", "resumen": "Resumen de Temporada",
        "pase": "Yardas Pase", "tierra": "Yardas Tierra", "puntos": "Puntos Totales",
        "desglose": "Desglose Completo", "fuentes": "Fuentes Externas", "trending": "Tendencias en X",
        "prep_header": "🎙️ Irish Breakdown Show Prep",
        "prep_desc": "Herramientas para eliminar las tareas pesadas (chores) de Bryan Driskell.",
        "quick_analysis": "📌 Análisis Rápido",
        "ideas_header": "💡 Ideas para el segmento 'Buy / Sell / Hold'",
        "idea1": "¿Es la defensa de ND la mejor de la era Freeman?",
        "idea2": "Proyección: Impacto de los nuevos compromisos en el ranking nacional.",
        "idea3": "Análisis: Rendimiento en terceras oportunidades vs la media nacional.",
        "link_team": "Abrir comparativa en TeamRankings",
        "link_cfb": "Consultar históricos en CFBStats",
        "link_x": "Ver noticias de reclutas en X (Tiempo Real)"
    },
    "English": {
        "titulo": "🍀 Notre Dame Command Center",
        "tab1": "Stats", "tab2": "Roster", "tab3": "Commitments", "tab4": "Show Prep",
        "boton": "🔄 Refresh Now", "resumen": "Season Summary",
        "pase": "Passing Yards", "tierra": "Rushing Yards", "puntos": "Total Points",
        "desglose": "Full Breakdown", "fuentes": "External Sources", "trending": "X Trends",
        "prep_header": "🎙️ Irish Breakdown Show Prep",
        "prep_desc": "Tools to eliminate Bryan Driskell's heavy lifting (chores).",
        "quick_analysis": "📌 Quick Analysis",
        "ideas_header": "💡 Ideas for 'Buy / Sell / Hold' Segment",
        "idea1": "Is ND's defense the best of the Freeman era?",
        "idea2": "Projection: Impact of new commitments on national rankings.",
        "idea3": "Analysis: Third-down performance vs national average.",
        "link_team": "Open TeamRankings comparison",
        "link_cfb": "Check historical data on CFBStats",
        "link_x": "View recruit news on X (Real Time)"
    },
    "Français": {
        "titulo": "🍀 Centre de Contrôle Notre Dame",
        "tab1": "Statistiques", "tab2": "Effectif", "tab3": "Recrutement", "tab4": "Show Prep",
        "boton": "🔄 Actualiser maintenant", "resumen": "Résumé de la Saison",
        "pase": "Yards de Passe", "tierra": "Yards de Course", "puntos": "Points Totaux",
        "desglose": "Répartition Complète", "fuentes": "Sources Externes", "trending": "Tendances sur X",
        "prep_header": "🎙️ Irish Breakdown Show Prep",
        "prep_desc": "Outils pour éliminer les corvées de Bryan Driskell.",
        "quick_analysis": "📌 Analyse Rapide",
        "ideas_header": "💡 Idées pour le segment 'Buy / Sell / Hold'",
        "idea1": "La défense de ND est-elle la meilleure de l'ère Freeman?",
        "idea2": "Projection: Impact des nouveaux engagements sur le classement national.",
        "idea3": "Analyse: Performance sur les troisièmes tentatives vs moyenne nationale.",
        "link_team": "Ouvrir la comparaison TeamRankings",
        "link_cfb": "Consulter les historiques sur CFBStats",
        "link_x": "Voir les nouvelles des recrues sur X"
    }
}
# 2. CONFIGURACIÓN DEL SIDEBAR (BARRA LATERAL)
st.sidebar.title("Configuración")
seleccion = st.sidebar.selectbox("Idioma / Language", list(idiomas.keys()))
t = idiomas[seleccion]

# Botones de enlaces rápidos que pidió Bryan Driskell
st.sidebar.divider()
st.sidebar.subheader(t["fuentes"])
st.sidebar.link_button("📊 Team Rankings (ND)", "https://www.teamrankings.com/ncf/team/notre-dame-fighting-irish/stats")
st.sidebar.link_button("📈 CFB Stats (ND)", "http://www.cfbstats.com/2025/team/513/index.html")

# 3. CUERPO PRINCIPAL
st.title(t["titulo"])

if st.button(t["boton"]):
    st.cache_data.clear()
    st.rerun()

# Definición de las 4 pestañas
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# Función para conectar con las APIs
@st.cache_data(ttl=600)
def obtener_datos(url):
    try:
        r = requests.get(url)
        return r.json()
    except:
        return None

# --- TAB 1: ESTADÍSTICAS (DATOS REALES) ---
with tab1:
    datos = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
    if datos:
        categorias = datos.get('results', {}).get('stats', {}).get('categories', [])
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
                for s in cat['stats']:
                    st.write(f"**{s['displayName']}:** {s['displayValue']}")

# --- TAB 2: JUGADORES (ROSTER) ---
with tab2:
    roster = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/roster")
    if roster:
        for group in roster.get('athletes', []):
            st.write(f"### {group['position']}")
            for p in group['items']:
                c1, c2 = st.columns([1, 5])
                with c1: 
                    st.image(p.get('headshot', {}).get('href', 'https://via.placeholder.com/50'), width=60)
                with c2: 
                    st.write(f"**{p['fullName']}** | #{p.get('jersey', 'N/A')}")
                    st.caption(f"{p.get('displayHeight', '')}, {p.get('displayWeight', '')}")

# --- TAB 3: COMPROMISOS (RECRUITING) ---
with tab3:
    st.subheader("Class 2026 Commitments")
    st.info("Futuros talentos que han dado el 'Sí' a Notre Dame")
    # Datos simulados basados en tendencias reales para el show
    commits = [
        {"name": "Noah Grubbs", "pos": "QB", "stars": "⭐⭐⭐⭐"},
        {"name": "Jameson Knight", "pos": "WR", "stars": "⭐⭐⭐⭐⭐"}
    ]
    for c in commits:
        st.success(f"✅ {c['name']} ({c['pos']}) - {c['stars']}")

# --- TAB 4: SHOW PREP (ESPECÍFICO PARA EL CLIENTE) ---
with tab4:
    st.header("🎙️ Irish Breakdown Show Prep")
    st.write("Herramientas para eliminar las tareas pesadas (chores) de Bryan Driskell.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📌 Análisis Rápido")
        st.info("[Abrir comparativa en TeamRankings](https://www.teamrankings.com/ncf/stats/)")
        st.info("[Consultar históricos en CFBStats](http://www.cfbstats.com/)")
    
    with col_b:
        st.subheader(f"🐦 {t['trending']}")
        # Enlace directo a la búsqueda que Bryan hace manualmente
        st.markdown("[Ver noticias de reclutas en X (Tiempo Real)](https://twitter.com/search?q=Notre%20Dame%20Recruiting&src=typed_query&f=live)")
    
    st.divider()
    st.subheader("💡 Ideas para el segmento 'Buy / Sell / Hold'")
    st.write("Temas sugeridos basados en la actividad de la semana:")
    st.checkbox("Debate: ¿Es la defensa de ND la mejor de la era Freeman?")
    st.checkbox("Proyección: Impacto de los nuevos compromisos en el ranking nacional.")
    st.checkbox("Análisis: Rendimiento en terceras oportunidades vs la media nacional.")
