import streamlit as st
import requests

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="ND Hub - Dream Assistant", 
    page_icon="🍀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- DICCIONARIO DE IDIOMAS ---
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
        "link_x": "Ver noticias de reclutas en X (Tiempo Real)",
        "boton_atras": "⬅️ Volver a Estadísticas"
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
        "link_x": "View recruit news on X (Real Time)",
        "boton_atras": "⬅️ Back to Stats"
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
        "link_x": "Voir les nouvelles des recrues sur X",
        "boton_atras": "⬅️ Retour aux Statistiques"
    }
}

# --- CONTROL DE NAVEGACIÓN ---
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0

# 2. SELECTOR DE IDIOMA
st.sidebar.title("Configuración")
seleccion = st.sidebar.selectbox("Idioma / Language", list(idiomas.keys()))
t = idiomas[seleccion]

# Barra lateral
st.sidebar.divider()
st.sidebar.subheader(t["fuentes"])
st.sidebar.link_button(f"📊 {t['link_team']}", "https://www.teamrankings.com/ncf/team/notre-dame-fighting-irish/stats")
st.sidebar.link_button(f"📈 {t['link_cfb']}", "http://www.cfbstats.com/2025/team/513/index.html")

# 3. CUERPO PRINCIPAL
st.title(t["titulo"])

# Pestañas controladas por session_state
tabs = [t["tab1"], t["tab2"], t["tab3"], t["tab4"]]
active_tab = st.tabs(tabs)

@st.cache_data(ttl=600)
def obtener_datos(url):
    try:
        r = requests.get(url)
        return r.json()
    except:
        return None

# --- TAB 1: ESTADÍSTICAS ---
with active_tab[0]:
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
        for cat in categorias:
            with st.expander(f"📊 {cat['displayName']}"):
                for s in cat['stats']: st.write(f"**{s['displayName']}:** {s['displayValue']}")

# --- TAB 2: ROSTER ---
with active_tab[1]:
    roster = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/roster")
    if roster:
        for group in roster.get('athletes', []):
            st.write(f"### {group['position']}")
            for p in group['items']:
                c1, c2 = st.columns([1, 5])
                with c1: st.image(p.get('headshot', {}).get('href', 'https://via.placeholder.com/50'), width=60)
                with c2: st.write(f"**{p['fullName']}** | #{p.get('jersey', 'N/A')}")

# --- TAB 3: RECRUITING ---
with active_tab[2]:
    st.subheader("Class 2026 Commitments")
    commits = [{"name": "Noah Grubbs", "pos": "QB", "stars": "⭐⭐⭐⭐"}, {"name": "Jameson Knight", "pos": "WR", "stars": "⭐⭐⭐⭐⭐"}]
    for c in commits: st.success(f"✅ {c['name']} ({c['pos']}) - {c['stars']}")

# --- TAB 4: SHOW PREP (CON BOTÓN ATRÁS) ---
with active_tab[3]:
    # BOTÓN PARA VOLVER A LA TAB 0 (Estadísticas)
    if st.button(t["boton_atras"]):
        # Nota: En Streamlit las pestañas son visuales. Para "volver", 
        # simplemente reiniciamos la app o usamos un aviso.
        st.info("Para volver, haz clic en la pestaña de 'Estadísticas' arriba.")
        st.rerun()

    st.header(t["prep_header"])
    st.write(t["prep_desc"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader(t["quick_analysis"])
        st.info(f"[{t['link_team']}](https://www.teamrankings.com/ncf/stats/)")
        st.info(f"[{t['link_cfb']}](http://www.cfbstats.com/)")
    with col_b:
        st.subheader(f"🐦 {t['trending']}")
        st.markdown(f"[{t['link_x']}](https://twitter.com/search?q=Notre%20Dame%20Recruiting&src=typed_query&f=live)")
    
    st.divider()
    st.subheader(t["ideas_header"])
    st.checkbox(t["idea1"])
    st.checkbox(t["idea2"])
    st.checkbox(t["idea3"])
