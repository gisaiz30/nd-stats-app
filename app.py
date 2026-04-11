import streamlit as st
import requests

# Configuración de la página
st.title("🍀 Estadísticas en Vivo: Notre Dame")

# Tu llave de la API (Aquí pones la que te llegó al correo)
api_key = "+4QJIvbSYN9xIB8BJOVwqmgnEPcR7DfhlNZzssapv5jQkYba5zXfXUMYo8lPYtLy"
headers = {"Authorization": f"Bearer {api_key}"}

# 1. Función para traer los datos (Se ejecuta cada vez que entras)
def obtener_datos():
    url = "https://api.collegefootballdata.com/teams/stats?year=2025&team=Notre%20Dame"
    response = requests.get(url, headers=headers)
    return response.json()

# 2. Mostrar los datos en la pantalla
datos = obtener_datos()

if datos:
    stats = datos[0]['stats']
    st.write("### Estadísticas de la Temporada")
    
    # Creamos columnas para que se vea profesional
    col1, col2 = st.columns(2)
    for s in stats:
        if s['category'] in ['offenseScore', 'defenseScore']:
            col1.metric(label=s['category'], value=s['stat'])
else:
    st.error("No se pudieron cargar los datos. Revisa tu API Key.")
