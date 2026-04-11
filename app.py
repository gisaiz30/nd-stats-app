import streamlit as st
import requests
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="ND Hub - Dream Assistant", 
    page_icon="🍀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- DICCIONARIO DE IDIOMAS ACTUALIZADO ---
idiomas = {
    "Español": {
        "titulo": "🍀 Panel de Control Notre Dame",
        "tab1": "Estadísticas", "tab2": "Jugadores", "tab3": "Compromisos", "tab4": "Morning Note 🎙️",
        "boton": "🔄 Actualizar ahora", "resumen": "Resumen de Temporada",
        "pase": "Yardas Pase", "tierra": "Yardas Tierra", "puntos": "Puntos Totales",
        "desglose": "Desglose Completo", "fuentes": "Fuentes Externas", "trending": "Tendencias en X",
        "prep_header": "🌅 Morning Note: Guion del Show",
        "prep_desc": "Generación automática de puntos clave para Bryan Driskell.",
        "boton_guion": "🚀 Generar Guion e Ideas",
        "ideas_header": "⚖️ Segmento: Buy / Sell / Hold",
        "ideas_desc": "Temas sugeridos por la IA para el debate de hoy:",
        "link_team": "TeamRankings", "link_cfb": "CFBStats", "link_x": "Noticias X",
        "analisis_pred": "🧠 Análisis Predictivo e Inteligencia"
    },
    "English": {
        "titulo": "🍀 Notre Dame Command Center",
        "tab1": "Stats", "tab2": "Roster", "tab3": "Commitments", "tab4": "Morning Note 🎙️",
        "boton": "🔄 Refresh Now", "resumen": "Season Summary",
        "pase": "Passing Yards", "tierra": "Rushing Yards", "puntos": "Total Points",
        "desglose": "Full Breakdown", "fuentes": "External Sources", "trending": "X Trends",
        "prep_header": "🌅 Morning Note: Show Script",
        "prep_desc": "Automatic generation of key points for Bryan Driskell.",
        "boton_guion": "🚀 Generate Script & Ideas",
        "ideas_header": "⚖️ Segment: Buy / Sell / Hold",
        "ideas_desc": "AI-suggested topics for today's debate:",
        "link_team": "TeamRankings", "link_cfb": "CFBStats", "link_x": "X News",
        "analisis_pred": "🧠 Predictive Analysis & Intelligence"
    }
}

# 2. SELECTOR DE IDIOMA
st.sidebar.title("Configuración")
seleccion = st.sidebar.selectbox("Idioma / Language", list(idiomas.keys()))
t = idiomas[seleccion]

# Barra lateral
st.sidebar.divider()
st.sidebar.subheader(t["fuentes"])
st.sidebar.link_button(f"📊 {t['link_team']}", "https://www.teamrankings.com/ncf/team/notre-dame-fighting-irish/stats")
st.sidebar.link_button(f"📈 {t['link_cfb']}", "http://www.cfbstats.com/2025/team/513/index.html")

# 3. LÓGICA DE DATOS
@st.cache_data(ttl=600)
def obtener_datos(url):
    try:
        r = requests.get(url)
        return r.json()
    except: return None

# 4. CUERPO PRINCIPAL
st.title(t["titulo"])

# Definición de las 4 pestañas
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# --- TAB 1, 2 y 3 (Se mantienen con tu lógica de APIs anterior) ---
with tab1:
    datos_stats = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
    if datos_stats:
        st.subheader(t["resumen"])
        # (Aquí iría tu lógica de métricas de la Tab 1)

# --- TAB 4: MORNING NOTE & BUY/SELL/HOLD ---
with tab4:
    st.header(t["prep_header"])
    st.write(t["prep_desc"])
    
    if st.button(t["boton_guion"], type="primary"):
        with st.spinner('Analizando tendencias y estadísticas...'):
            datos_m = obtener_datos("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics")
            
            # Simulamos el análisis para generar los temas "picantes"
            st.markdown(f"### 📄 Show Script - {datetime.now().strftime('%d/%m/%Y')}")
            
            # --- SECCIÓN BUY / SELL / HOLD ---
            st.divider()
            st.subheader(t["ideas_header"])
            st.info(t["ideas_desc"])
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown("### 🟢 **BUY**")
                st.write("**Tema:** Noah Grubbs como titular inmediato en 2026.")
                st.caption("Basado en: Tendencias de reclutamiento y eficiencia actual de QBs.")
            
            with col_b:
                st.markdown("### 🔴 **SELL**")
                st.write("**Tema:** La defensa de ND permitirá menos de 10 puntos este sábado.")
                st.caption("Basado en: El próximo rival promedia 24.5 puntos por partido.")
                
            with col_c:
                st.markdown("### 🟡 **HOLD**")
                st.write("**Tema:** Mantener el esquema de rotación en la línea ofensiva.")
                st.caption("Basado en: Estadísticas de capturas permitidas en los últimos 2 juegos.")

            st.divider()
            st.subheader(t["analisis_pred"])
            st.warning("Punto de debate sugerido: ¿Es la ofensiva terrestre actual superior a la de la temporada pasada según las yardas por acarreo?")

    st.divider()
    # Enlaces rápidos para Bryan
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(t["fuentes"])
        st.write(f"- [{t['link_team']}](https://www.teamrankings.com/ncf/stats/)")
        st.write(f"- [{t['link_cfb']}](http://www.cfbstats.com/)")
    with c2:
        st.subheader(t["trending"])
        st.write(f"- [{t['link_x']}](https://twitter.com/search?q=Notre%20Dame%20Recruiting)")
