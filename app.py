import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração e Limpeza de Cache
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO: FUNDO ESCURO + KPIs GIGANTES (50px) ---
st.markdown("""
    <style>
    .stApp { background-color: #000b1a; color: white; }
    .zion-header {
        background: #001f3f; color: #00d4ff; padding: 20px; 
        border-radius: 15px; font-size: 40px; font-weight: bold; 
        text-align: center; border: 2px solid #00d4ff; margin-bottom: 25px;
    }
    div[data-testid="stMetric"] {
        background-color: #001529; border: 1px solid #00d4ff;
        border-radius: 15px; padding: 20px;
    }
    /* NÚMEROS TAMANHO 50px COLORIDOS */
    div[data-testid="stMetricValue"] { font-size: 50px !important; font-weight: bold !important; }
    
    /* Cores dos KPIs */
    [data-testid="stMetric"]:nth-child(1) div[data-testid="stMetricValue"] { color: #00ffcc !important; } 
    [data-testid="stMetric"]:nth-child(2) div[data-testid="stMetricValue"] { color: #ffcc00 !important; }
    [data-testid="stMetric"]:nth-child(3) div[data-testid="stMetricValue"] { color: #0099ff !important; }
    [data-testid="stMetric"]:nth-child(4) div[data-testid="stMetricValue"] { color: #ff3333 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="zion-header">ZION MONITORAMENTO</div>', unsafe_allow_html=True)

# TABELA DE COORDENADAS (Para o mapa nunca mais vir vazio)
coords = {
    'PA': [-1.45, -48.50], 'AM': [-3.11, -60.02], 'RR': [2.82, -60.67],
    'AP': [0.03, -51.06], 'MA': [-2.53, -44.30], 'MT': [-12.64, -55.42],
    'RO': [-8.76, -63.90], 'TO': [-10.18, -48.33], 'AC': [-9.97, -67.81]
}

URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    # Lendo e forçando tipos para evitar o erro de 'float' e 'str'
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)
    df['ESTADO'] = df['ESTADO'].astype(str).str.upper().str.strip()

    # Dropdown de Fornecedores
    lista_forn = ["TODOS"] + sorted(df['FORNECEDOR'].dropna().unique().tolist())
    forn_sel = st.selectbox("🔍 FILTRAR POR FORNECEDOR:", lista_forn)

    if forn_sel != "TODOS":
        df = df[df['FORNECEDOR'] == forn_sel]

    # --- KPIs GIGANTES (50px) ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Abastecimentos", len(df))
    top_f = df['FORNECEDOR'].value_counts().idxmax() if not df.empty else "---"
    c3.metric("Líder de Vendas", top_f)
    c4.metric("Cidades", df['LOCAL'].nunique())

    # --- MAPA QUE FUNCIONA ---
    st.subheader("📍 Localização Exata das Operações")
    df['lat'] = df['ESTADO'].map(lambda x: coords.get(x, [None, None])[0])
    df['lon'] = df['ESTADO'].map(lambda x: coords.get(x, [None, None])[1])
    
    # Mapa de Pontos (Scatter Mapbox) - O mais robusto que existe
    fig_mapa = px.scatter_mapbox(df.dropna(subset=['lat']), 
                                lat="lat", lon="lon", 
                                size="QTOS LTS", color="EMPURRADOR",
                                hover_name="LOCAL", zoom=3.5, height=500)
    fig_mapa.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_mapa, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")

# Auto-refresh
st.markdown("""<script>setTimeout(function(){ window.location.reload(); }, 30000);</script>""", unsafe_allow_html=True)
