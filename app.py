import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Configuração e Limpeza
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO: FUNDO AZUL ESCURO E KPIs GIGANTES (50px) ---
st.markdown("""
    <style>
    .stApp { background-color: #001529; color: white; }
    .zion-header {
        background-color: #002140;
        color: #00d4ff;
        padding: 15px;
        border-radius: 10px;
        font-size: 35px;
        font-weight: bold;
        text-align: center;
        border: 1px solid #00d4ff;
        margin-bottom: 20px;
    }
    /* Estilo dos Cards KPIs */
    div[data-testid="stMetric"] {
        background-color: #002140;
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    /* NÚMEROS TAMANHO 50 COLORIDOS */
    div[data-testid="stMetricValue"] {
        font-size: 50px !important;
        font-weight: bold !important;
    }
    /* Cores específicas para cada informação */
    [data-testid="stMetric"]:nth-child(1) div[data-testid="stMetricValue"] { color: #00ff88 !important; } /* Volume */
    [data-testid="stMetric"]:nth-child(2) div[data-testid="stMetricValue"] { color: #ffbb00 !important; } /* Qtd */
    [data-testid="stMetric"]:nth-child(3) div[data-testid="stMetricValue"] { color: #00d4ff !important; } /* Top Forn */
    [data-testid="stMetric"]:nth-child(4) div[data-testid="stMetricValue"] { color: #ff4d4d !important; } /* Cidades */
    
    label[data-testid="stMetricLabel"] { color: white !important; font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho
st.markdown('<div class="zion-header">ZION MONITORAMENTO - GESTÃO NAVAL</div>', unsafe_allow_html=True)

# Dados
URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # --- DROPDOWN DE FORNECEDORES ---
    lista_forn = ["TODOS"] + sorted(df['FORNECEDOR'].unique().tolist())
    forn_selecionado = st.selectbox("🔍 Filtrar por Fornecedor:", lista_forn)

    if forn_selecionado != "TODOS":
        df = df[df['FORNECEDOR'] == forn_selecionado]

    # --- LINHA 1: KPIs GIGANTES ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Abastecimentos", len(df))
    top_f = df['FORNECEDOR'].value_counts().idxmax() if not df.empty else "---"
    c3.metric("Líder Atual", top_f)
    c4.metric("Cidades", df['LOCAL'].nunique())

    st.markdown("---")

    # --- LINHA 2: MAPA E RANKING ---
    col_mapa, col_rank = st.columns([2, 1])

    with col_mapa:
        st.subheader("📍 Localização dos Abastecimentos (Mapa Nítido)")
        # Mapa de pontos coloridos (Funciona 100% sem erro de BRA-states)
        fig_mapa = px.scatter_geo(df,
                                 locations="ESTADO",
                                 locationmode="country names",
                                 color="EMPURRADOR",
                                 size="QTOS LTS",
                                 hover_name="LOCAL",
                                 scope="south america",
                                 template="plotly_dark",
                                 color_discrete_sequence=px.colors.qualitative.Light24)
        fig_mapa.update_geos(showcountries=True, countrycolor="#222")
        fig_mapa.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_mapa, use_container_width=True)

    with col_rank:
        st.subheader("🚢 Volume por Empurrador")
        df_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS')
        fig_emp = px.bar(df_emp, y='EMPURRADOR', x='QTOS LTS', orientation='h', text_auto=True, color='QTOS LTS')
        fig_emp.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_emp, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")

# Atualização 30s
st.markdown("""<script>setTimeout(function(){ window.location.reload(); }, 30000);</script>""", unsafe_allow_html=True)
