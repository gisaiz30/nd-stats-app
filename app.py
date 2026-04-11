# Tu llave de la API (Asegúrate de que sea la que te enviaron al correo)
# Si no tienes una, regístrate en https://collegefootballdata.com/key
api_key = "+4QJIvbSYN9xIB8BJOVwqmgnEPcR7DfhlNZzssapv5jQkYba5zXfXUMYo8lPYtLy" 
headers = {"Authorization": f"Bearer {api_key}"}

def obtener_datos():
    # Probamos con el año 2025 que es el más reciente con datos completos
    url = "https://api.collegefootballdata.com/teams/stats?year=2025&team=Notre%20Dame"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error de la API: Código {response.status_code}. Revisa tu API Key.")
        return None

datos = obtener_datos()

if datos:
    # Mostramos el nombre del equipo y el año
    st.success(f"Datos cargados para {datos[0]['team']} (Temporada {datos[0]['year']})")
    
    stats = datos[0]['stats']
    
    # Organizamos en columnas atractivas
    col1, col2, col3 = st.columns(3)
    
    # Diccionario para traducir o filtrar categorías importantes
    importantes = {
        'offenseScore': "Puntos Ofensivos",
        'defenseScore': "Puntos Defensivos",
        'games': "Partidos Jugados"
    }

    for s in stats:
        cat = s['category']
        val = s['stat']
        
        if cat == 'offenseScore':
            col1.metric("Puntos Ofensivos", val)
        elif cat == 'defenseScore':
            col2.metric("Puntos Defensivos", val)
        elif cat == 'games':
            col3.metric("Partidos", val)

    # Mostrar todas las estadísticas en una tabla bonita
    with st.expander("Ver todas las estadísticas detalladas"):
        st.table(stats)
else:
    st.warning("No hay datos disponibles para mostrar en este momento.")
