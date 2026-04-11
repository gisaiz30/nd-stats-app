import streamlit as st
import requests

# 1. CONFIGURACIÓN ÚNICA
st.set_page_config(page_title="ND Hub", page_icon="🍀", layout="wide", initial_sidebar_state="expanded")

# --- DICCIONARIO DE TRADUCCIONES ---
idiomas = {
    "Español": {
        "titulo": "🍀 Panel de Control Notre Dame",
        "tab1": "Estadísticas", "tab2": "Jugadores", "tab3": "Compromisos",
        "boton": "🔄 Actualizar ahora",
        "resumen": "Resumen de Temporada",
        "pase": "Yardas Pase", "tierra": "Yardas Tierra", "puntos": "Puntos Totales",
        "desglose": "Desglose Completo"
        # Añade esto dentro de cada idioma en tu diccionario
"tab4": "Show Prep", 
"fuentes": "Fuentes Externas",
"trending": "Tendencias en X (Recruiting)"
    },
    "English": {
        "titulo": "🍀 Notre Dame Command Center",
        "tab1": "Stats", "tab2": "Roster", "tab3": "Commitments",
        "boton": "🔄 Refresh Now",
        "resumen": "Season Summary",
        "pase": "Passing Yards", "tierra": "Rushing Yards", "puntos": "Total Points",
        "desglose": "Full Breakdown"
        # Añade esto dentro de cada idioma en tu diccionario
"tab4": "Show Prep", 
"fuentes": "Fuentes Externas",
"trending": "Tendencias en X (Recruiting)"
    },
    "Français": {
        "titulo": "🍀 Centre de Contrôle Notre Dame",
        "tab1": "Statistiques", "tab2": "Effectif", "tab3": "Recrutement",
        "boton": "🔄 Actualiser maintenant",
        "resumen": "Résumé de la Saison",
        "pase": "Yards de Passe", "tierra": "Yards de Course", "puntos": "Points Totaux",
        "desglose": "Répartition Complète"
        # Añade esto dentro de cada idioma en tu diccionario
"tab4": "Show Prep", 
"fuentes": "Fuentes Externas",
"trending": "Tendencias en X (Recruiting)"
    }
}

# 2. SELECTOR DE IDIOMA
st.sidebar.title("Configuración")
seleccion = st.sidebar.selectbox("Idioma / Language", list(idiomas.keys()))
t = idiomas[seleccion]

st.title(t["titulo"])

# Botón de actualizar
if st.button(t["boton"]):
    st.cache_data.clear()
    st.rerun()

# 3. PESTAÑAS
tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

@st.cache_data(ttl=600)
def obtener_datos(url):
    try:
        return requests.get(url).json()
    except:
        return None

# --- TAB 1: ESTADÍSTICAS (La versión de 3,061 yardas) ---
with tab1:
    datos = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
    if datos:
        categorias = datos.get('results', {}).get('stats', {}).get('categories', [])
        st.subheader(t["resumen"])
        
        col1, col2, col3 = st.columns(3)
        
        for cat in categorias:
            # Buscamos por nombre técnico para evitar el error de las 217 yardas
            if cat['name'] == 'passing':
                for s in cat['stats']:
                    if s['name'] == 'netPassingYards':
                        col1.metric(t["pase"], s['displayValue'])
            
            if cat['name'] == 'rushing':
                for s in cat['stats']:
                    if s['name'] == 'rushingYards':
                        col2.metric(t["tierra"], s['displayValue'])
            
            if cat['name'] == 'scoring':
                for s in cat['stats']:
                    if s['name'] == 'totalPoints':
                        col3.metric(t["puntos"], s['displayValue'])

        st.divider()
        st.write(f"### {t['desglose']}")
        for cat in categorias:
            with st.expander(f"📊 {cat['displayName']}"):
                for s in cat['stats']:
                    st.write(f"**{s['displayName']}:** {s['displayValue']}")

# --- TAB 2: JUGADORES ---
with tab2:
    roster = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/roster")
    if roster:
        for group in roster.get('athletes', []):
            st.write(f"### {group['position']}")
            for p in group['items']:
                c1, c2 = st.columns([1, 5])
                with c1: st.image(p.get('headshot', {}).get('href', 'https://via.placeholder.com/50'), width=60)
                with c2: st.write(f"**{p['fullName']}** | #{p.get('jersey', '0')}")

# --- TAB 3: COMPROMISOS ---
with tab3:
    st.subheader("Class 2026 Commitments")
    commits = [
        {"name": "Noah Grubbs", "pos": "QB", "stars": "⭐⭐⭐⭐"},
        {"name": "Jameson Knight", "pos": "WR", "stars": "⭐⭐⭐⭐⭐"}
    ]
    for c in commits:
        st.success(f"✅ {c['name']} ({c['pos']}) - {c['stars']}")
