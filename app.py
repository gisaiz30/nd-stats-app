import streamlit as st
import requests

# 1. Configuración de la página
st.set_page_config(page_title="ND Stats - ESPN Source", page_icon="🍀")
st.title("🍀 Estadísticas Notre Dame (Vía ESPN)")

# 2. Función para traer datos de ESPN (ID 87 es Notre Dame)
@st.cache_data(ttl=3600) # Esto hace que la app sea rápida y no sature a ESPN
def obtener_datos_espn():
    # Esta es la URL de la API interna de ESPN para el equipo 87
    url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/87/statistics"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# 3. Ejecución
datos = obtener_datos_espn()

if datos:
    # Extraemos las estadísticas principales
    # ESPN las organiza por grupos (defensive, offensive, etc.)
    st.subheader("Resumen de Temporada")
    
    # Buscamos algunas estadísticas clave para mostrar en grande
    col1, col2, col3 = st.columns(3)
    
    # Navegamos por el JSON de ESPN
    categorias = datos.get('results', {}).get('stats', [])
    
    for grupo in categorias:
        if grupo['name'] == 'passing':
            # Ejemplo: Total de yardas por pase
            total_yards = grupo['stats'][1] # 'netPassingYards'
            col1.metric("Yardas Pase", total_yards['displayValue'])
        
        if grupo['name'] == 'rushing':
            # Ejemplo: Total de yardas por tierra
            rush_yards = grupo['stats'][1] # 'rushingYards'
            col2.metric("Yardas Tierra", rush_yards['displayValue'])

        if grupo['name'] == 'scoring':
            # Puntos totales
            puntos = grupo['stats'][0] # 'totalPoints'
            col3.metric("Puntos Totales", puntos['displayValue'])

    # 4. Tabla Detallada
    with st.expander("Ver todas las estadísticas detalladas (Modo Tabla)"):
        for grupo in categorias:
            st.write(f"**Categoría: {grupo['displayName']}**")
            # Creamos una lista de diccionarios para mostrarlo bonito
            tabla_datos = [{"Estadística": s['displayName'], "Valor": s['displayValue']} for s in grupo['stats']]
            st.table(tabla_datos)

else:
    st.warning("No se pudieron cargar los datos de ESPN. Intenta refrescar la página.")

st.info("Nota: Los datos se actualizan automáticamente desde ESPN cada vez que entras.")
