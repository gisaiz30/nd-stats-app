import streamlit as st
import requests
# 1. Configuración de la página
st.set_page_config(page_title="ND Stats Multi-Language", page_icon="🍀")

# 1. Configuración de la página (La barra se queda abierta por defecto)
st.set_page_config(page_title="ND Stats", page_icon="🍀", initial_sidebar_state="expanded")

# --- DICCIONARIO DE TRADUCCIONES ---
idiomas = {
    "Español": {
        "titulo": "🍀 Estadísticas Notre Dame",
        "boton": "🔄 Actualizar ahora",
        "resumen": "Resumen de Temporada",
        "pase": "Yardas Pase",
        "tierra": "Yardas Tierra",
        "puntos": "Puntos Totales",
        "desglose": "Desglose Completo"
    },
    "English": {
        "titulo": "🍀 Notre Dame Statistics",
        "boton": "🔄 Refresh Now",
        "resumen": "Season Summary",
        "pase": "Passing Yards",
        "tierra": "Rushing Yards",
        "puntos": "Total Points",
        "desglose": "Full Breakdown"
    },
    "Français": {
        "titulo": "🍀 Statistiques de Notre Dame",
        "boton": "🔄 Actualiser maintenant",
        "resumen": "Résumé de la Saison",
        "pase": "Yards de Passe",
        "tierra": "Yards de Course",
        "puntos": "Points Totaux",
        "desglose": "Répartition Complète"
    }
}

# 2. Selector en la barra lateral
st.sidebar.title("Configuración")
seleccion = st.sidebar.selectbox("Idioma / Language", list(idiomas.keys()))
t = idiomas[seleccion]  # Esta 't' es la que hace la magia

# --- APLICAR TRADUCCIONES A LA APP ---

st.title(t["titulo"]) # <--- Aquí usamos t["titulo"] en lugar de texto fijo

if st.button(t["boton"]):
    st.cache_data.clear()
    st.rerun()

@st.cache_data(ttl=600)
def obtener_datos():
    url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics"
    return requests.get(url).json()

datos = obtener_datos()

if datos:
    categorias = datos.get('results', {}).get('stats', {}).get('categories', [])
    st.subheader(t["resumen"]) # <--- Traducción aplicada
    
    col1, col2, col3 = st.columns(3)
    
    for cat in categorias:
        if cat['name'] == 'passing':
            val = cat['stats'][1]['displayValue'] # yardas pase
            col1.metric(t["pase"], val) # <--- Traducción aplicada
            
        if cat['name'] == 'rushing':
            val = cat['stats'][1]['displayValue'] # yardas tierra
            col2.metric(t["tierra"], val) # <--- Traducción aplicada
            
        if cat['name'] == 'scoring':
            val = cat['stats'][0]['displayValue'] # puntos
            col3.metric(t["puntos"], val) # <--- Traducción aplicada

    st.divider()
    st.write(f"### {t['desglose']}") # <--- Traducción aplicada
    
    for cat in categorias:
        with st.expander(f"📊 {cat['displayName']}"):
            for s in cat['stats']:
                st.write(f"**{s['displayName']}:** {s['displayValue']}")
# 1. Configuración de la página
st.set_page_config(page_title="ND Stats - ESPN", page_icon="🍀")
st.title("🍀 Estadísticas Notre Dame (ESPN)")
# --- AQUÍ VA EL BOTÓN ---
if st.button('🔄 Actualizar Estadísticas ahora'):
    st.cache_data.clear() # Esto borra la memoria vieja
    st.rerun()           # Esto reinicia la app para buscar datos nuevos
# ------------------------
# --- TAB 2: JUGADORES (ROSTER) ---
with tab2:
    # Usamos la API de ESPN para el roster actual
    roster_data = fetch_data("https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/roster")
    if roster_data:
        for group in roster_data.get('athletes', []):
            st.write(f"### {group['position']}")
            for player in group['items']:
                col_p1, col_p2 = st.columns([1, 4])
                with col_p1:
                    st.image(player.get('headshot', {}).get('href', 'https://via.placeholder.com/50'), width=70)
                with col_p2:
                    st.write(f"**{player['fullName']}** (#{player.get('jersey', 'N/A')})")
                    st.caption(f"{player.get('experience', {}).get('displayValue', '')} | {player.get('displayHeight', '')}, {player.get('displayWeight', '')}")

# --- TAB 3: COMPROMISOS (RECRUITING) ---
with tab3:
    st.write("### Reclutamiento Clase 2026")
    # Para recruiting usamos CollegeFootballData (necesitarías tu API KEY si fuera esa, 
    # pero aquí simulamos la visualización para que veas cómo queda)
    st.info("Aquí aparecerán los nuevos talentos que han firmado con Notre Dame.")
    
    # Ejemplo de cómo se vería una lista de reclutas
    reclutas_ejemplo = [
        {"nombre": "Noah Grubbs", "pos": "QB", "estrellas": "⭐⭐⭐⭐", "ciudad": "Lake Mary, FL"},
        {"nombre": "Deuce Knight", "pos": "QB", "estrellas": "⭐⭐⭐⭐⭐", "ciudad": "Lucedale, MS"}
    ]
    
    for r in reclutas_ejemplo:
        st.success(f"📌 {r['nombre']} - {r['pos']} | {t['estrellas']}: {r['estrellas']}")
        st.write(f"📍 {r['ciudad']}")
        st.divider()
# 2. Función para traer datos de la API de ESPN
@st.cache_data(ttl=600)
def obtener_datos_espn():
    # Usamos la URL de estadísticas de la temporada actual
    url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

datos = obtener_datos_espn()

# 3. Procesar y mostrar los datos
if datos and 'results' in datos:
    # ESPN guarda las estadísticas dentro de 'results' -> 'stats' -> 'categories'
    # Vamos a extraer las categorías de forma segura
    stats_data = datos.get('results', {})
    categorias = stats_data.get('stats', {}).get('categories', [])

    if categorias:
        st.subheader(f"Temporada {stats_data.get('season', 'Actual')}")
        
        # Creamos las métricas principales arriba
        col1, col2, col3 = st.columns(3)
        
        for cat in categorias:
            # Buscamos la categoría de pases
            if cat['name'] == 'passing':
                for s in cat['stats']:
                    if s['name'] == 'passingYards':
                        col1.metric("Yardas Pase", s['displayValue'])
            
            # Buscamos la categoría de carrera
            if cat['name'] == 'rushing':
                for s in cat['stats']:
                    if s['name'] == 'rushingYards':
                        col2.metric("Yardas Tierra", s['displayValue'])
            
            # Buscamos la categoría de anotación
            if cat['name'] == 'scoring':
                for s in cat['stats']:
                    if s['name'] == 'totalPoints':
                        col3.metric("Puntos Totales", s['displayValue'])

        # Tabla completa para ver todo
        st.divider()
        st.write("### Desglose Completo")
        for cat in categorias:
            with st.expander(f"📊 {cat['displayName']}"):
                for s in cat['stats']:
                    st.write(f"**{s['displayName']}:** {s['displayValue']}")
    else:
        st.warning("No se encontraron categorías de estadísticas en este momento.")
else:
    st.error("No se pudo conectar con ESPN o los datos no están disponibles.")
