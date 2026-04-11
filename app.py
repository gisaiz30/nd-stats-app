import streamlit as st
import requests

# 1. Configuración de la página
st.set_page_config(page_title="ND Stats - ESPN", page_icon="🍀")
st.title("🍀 Estadísticas Notre Dame (ESPN)")
# --- AQUÍ VA EL BOTÓN ---
if st.button('🔄 Actualizar Estadísticas ahora'):
    st.cache_data.clear() # Esto borra la memoria vieja
    st.rerun()           # Esto reinicia la app para buscar datos nuevos
# ------------------------
# --- DICCIONARIO DE TRADUCCIONES ---
idiomas = {
    "Español": {
        "titulo": "🍀 Estadísticas Notre Dame",
        "boton": "🔄 Actualizar ahora",
        "resumen": "Resumen de Temporada",
        "pase": "Yardas Pase",
        "tierra": "Yardas Tierra",
        "puntos": "Puntos Totales",
        "desglose": "Desglose Completo",
        "error": "Error al conectar con ESPN"
    },
    "English": {
        "titulo": "🍀 Notre Dame Statistics",
        "boton": "🔄 Refresh Now",
        "resumen": "Season Summary",
        "pase": "Passing Yards",
        "tierra": "Rushing Yards",
        "puntos": "Total Points",
        "desglose": "Full Breakdown",
        "error": "Error connecting to ESPN"
    },
    "Français": {
        "titulo": "🍀 Statistiques de Notre Dame",
        "boton": "🔄 Actualiser maintenant",
        "resumen": "Résumé de la Saison",
        "pase": "Yards de Passe",
        "tierra": "Yards de Course",
        "puntos": "Points Totaux",
        "desglose": "Répartition Complète",
        "error": "Erreur de connexion à ESPN"
    }
}
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
