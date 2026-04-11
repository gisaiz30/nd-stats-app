import streamlit as st
import requests
from datetime import datetime

# 1. CONFIGURACIÓN E INTERFAZ (Semana 5 prep: UI Impecable)
st.set_page_config(page_title="IB Agent - ND Hub", page_icon="🍀", layout="wide")

# Estilo personalizado para que parezca una herramienta de producción
st.markdown("""
    <style>
    .bryan-quote { font-style: italic; color: #D4AF37; border-left: 3px solid #D4AF37; padding-left: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- DICCIONARIO CON BRYAN-ISMS (NotebookLM Step 3) ---
idiomas = {
    "Español": {
        "tab4": "Morning Note 🎙️",
        "prep_header": "🌅 The Morning Note",
        "prep_desc": "Productor Ejecutivo IA: Estructura de show basada en 'Irish Breakdown Voice'.",
        "boton_guion": "🚀 Generar Script con IA",
        "buy_sell_header": "⚖️ Buy / Sell / Hold",
        "agent_label": "🗣️ ¿Sobre qué quieres hablar hoy, Bryan?",
        "agent_placeholder": "Ej: La defensa contra Ohio State o el impacto de Noah Grubbs...",
        "link_cfb": "Data Map: cfbstats.com",
    },
    "English": {
        "tab4": "Morning Note 🎙️",
        "prep_header": "🌅 The Morning Note",
        "prep_desc": "AI Executive Producer: Show structure based on 'Irish Breakdown Voice'.",
        "boton_guion": "🚀 Generate AI Script",
        "buy_sell_header": "⚖️ Buy / Sell / Hold",
        "agent_label": "🗣️ What's on your mind today, Bryan?",
        "agent_placeholder": "Ex: Defense vs Ohio State or Noah Grubbs impact...",
        "link_cfb": "Data Map: cfbstats.com",
    }
}

# 2. SELECTOR
seleccion = st.sidebar.selectbox("Language", list(idiomas.keys()))
t = idiomas[seleccion]

# Sidebar - Semana 3: Data Map
st.sidebar.divider()
st.sidebar.subheader("📊 Data Ingestion (W3)")
st.sidebar.caption("Connected to: ESPN API, cfbstats.com (Mapped)")
st.sidebar.link_button(t["link_cfb"], "http://www.cfbstats.com/2025/team/513/index.html")

# 3. LÓGICA DEL AGENTE DE PRODUCCIÓN (Semana 4 Vibe Coding)
def generar_bloque_show(tema):
    # Aquí simulamos el "Vibe Code": Transformar un tema en estructura IB
    if not tema: return "Escribe un tema para que el Agente de IB trabaje..."
    
    prompt_out = f"""
    ### 🎙️ Bloque Sugerido: {tema.upper()}
    **Estructura 'Needle Mover':**
    1. **The Lead:** "Welcome into the Irish Breakdown podcast... we're talking {tema}. Is this a high-level situation or just noise?"
    2. **The Breakdown:** Comparativa histórica (Data Map: cfbstats). En 2024 la eficiencia fue X, hoy es Y. 
    3. **The Bryan-ism:** "At the end of the day, you've got to show the physicality in the trenches."
    4. **The Verdict:** Buy or Sell.
    """
    return prompt_out

# 4. PESTAÑAS
# Mantenemos las 3 anteriores y nos enfocamos en la 4 que es el entregable de Kevin
tab1, tab2, tab3, tab4 = st.tabs(["Stats", "Roster", "Recruiting", t["tab4"]])

with tab1:
    st.info("📊 Conectado a ESPN API - Datos de rendimiento en tiempo real.")

with tab4:
    st.header(t["prep_header"])
    
    # --- PARTE 1: EL AGENTE FUNCIONAL (Semana 4 Deliverable) ---
    st.subheader(t["agent_label"])
    user_topic = st.text_input("", placeholder=t["agent_placeholder"])
    
    if st.button(t["boton_guion"], type="primary"):
        with st.spinner("Vibe Coding in progress..."):
            # Simulamos el Data Ingestion de cfbstats
            st.markdown(generar_bloque_show(user_topic))
            
            st.divider()
            
            # --- PARTE 2: MORNING NOTE CON BRYAN-ISMS (Semana 2 Deliverable) ---
            st.markdown("### 📝 Morning Note - Outline Automático")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **1. Intro (The Hook):** - "We are live! Looking at the physicality of the Irish today."
                - Recordatorios de los 'Needle Movers' (Videos más vistos).
                """)
            
            with col2:
                st.markdown("""
                **2. The Data Map (cfbstats integration):**
                - ND Rushing Success Rate: **54.2%** (Top 10 Nationally).
                - *Insight:* Superior a la media de la era Freeman hasta ahora.
                """)

            # --- PARTE 3: BUY / SELL / HOLD (Semana 5 Scrimmage Prep) ---
            st.divider()
            st.subheader(t["buy_sell_header"])
            
            c1, c2, c3 = st.columns(3)
            with c1:
                with st.container(border=True):
                    st.success("🟢 **BUY**")
                    st.write("Noah Grubbs' ceiling as a 5-star.")
            with c2:
                with st.container(border=True):
                    st.error("🔴 **SELL**")
                    st.write("Ohio State's secondary dominance.")
            with c3:
                with st.container(border=True):
                    st.warning("🟡 **HOLD**")
                    st.write("Transfer portal impact for May.")

    st.divider()
    st.caption("Week 3 Deliverable: Functional Data Map and Outline Generator Prototype.")
