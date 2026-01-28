import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Configuração e Limpeza de Cache
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO: FUNDO ESCURO, TEXTO COLORIDO E KPIs GIGANTES (50px) ---
st.markdown("""
    <style>
    .stApp { background-color: #001529; color: white; }
    .zion-header {
        background-color: #002140;
        color: #00d4ff;
        padding: 20px;
        border-radius: 10px;
        font-size: 38px;
        font-weight: bold;
        text-align: center;
        border: 2px solid #00d4ff;
        margin-bottom: 30px;
    }
    /* Cards de Informação */
    div[data-testid="stMetric"] {
        background-color: #002140;
        border: 1px solid #00d4ff;
        border-radius: 15px;
        padding: 20px;
    }
    /* NÚMEROS TAMANHO 50 E COLORIDOS */
    div[data-testid="stMetricValue"] {
        font-size: 50px !important;
        font-weight: bold !important;
    }
    /* Cores dos KPIs */
    [data-testid="stMetric"]:nth-child(1) div[data-testid="stMetricValue"] { color: #00ff88 !important; } 
    [data-testid="stMetric"]:nth-child(2) div[data-testid="stMetricValue"] { color: #ffbb00 !important; }
    [data-testid="stMetric"]:nth-child(3) div[data-testid="stMetricValue"] { color: #00d4ff !important; }
    [data-testid="stMetric"]:nth-child(4) div[data-testid="stMetricValue"] { color: #ff4d4d !important; }
    
    label[data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="zion-header">ZION MONITORAMENTO - GESTÃO NAVAL</div>', unsafe_allow_html=True)

# Conexão com a Planilha
URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    # Lendo e limpando dados para evitar erros de tipo
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    # Garante que a coluna de litros seja numérica
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)
    # Garante que as colunas de texto não tenham valores nulos
    df['FORNECEDOR'] = df['FORNECEDOR'].astype(str).fillna("N/A")
    df['EMPURRADOR'] = df['EMPURRADOR'].astype(str).fillna("N/A")

    # --- FILTRO DROPDAWN ---
    lista_fornecedores = ["TODOS"] + sorted(df['FORNECEDOR'].unique().tolist())
    selecionado = st.selectbox("🎯 Filtrar por Fornecedor:", lista_fornecedores)
    
    if selecionado != "TODOS":
        df = df[df['FORNECEDOR'] == selecionado]

    # --- KPIs GIGANTES ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Abastecimentos", len(df))
    top_f = df['FORNECEDOR'].value_counts().idxmax() if not df.empty else "---"
    c3.metric("Líder de Vendas", top_f)
    c4.metric("Cidades", df['LOCAL'].nunique())

    st.markdown("---")

    # --- MAPA E RANKING (ESTILO DASHBOARD PROFISSIONAL) ---
    col_mapa, col_info = st.columns([2, 1])

    with col_mapa:
        st.subheader("📍 Mapa Geográfico de Operações")
        # Mapa de bolhas que não depende de fronteiras internas (evita erro BRA-states)
        fig_mapa = px.scatter_geo(df,
                                 locations="ESTADO",
                                 locationmode="country names",
                                 color="EMPURRADOR",
                                 size="QTOS LTS",
                                 scope="south america",
                                 template="plotly_dark")
        fig_mapa.update_geos(lataxis_range=[-35, 10], lonaxis_range=[-75, -35]) # Foca no Brasil
        fig_mapa.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_mapa, use_container_width=True)

    with col_info:
        st.subheader("🏢 Ranking Fornecedores")
        df_f = df.groupby('FORNECEDOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS')
        fig_f = px.bar(df_f, x='QTOS LTS', y='FORNECEDOR', orientation='h', text_auto=True)
        fig_f.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig_f, use_container_width=True)

        st.subheader("🚢 Uso da Frota")
        df_p = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index()
        fig_p = px.pie(df_p, values='QTOS LTS', names='EMPURRADOR', hole=0.5)
        fig_p.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=250, showlegend=False)
        st.plotly_chart(fig_p, use_container_width=True)

except Exception as e:
    st.error(f"Aguardando dados válidos da planilha... (Certifique-se que não há células vazias nos Litros)")

# Script de Refresh (30s)
st.markdown("""<script>setTimeout(function(){ window.location.reload(); }, 30000);</script>""", unsafe_allow_html=True)
