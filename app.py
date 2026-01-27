import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Configurações de Página e Cache
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO "WEBSITE ANALYTICS" (IGUAL À IMAGEM 2) ---
st.markdown("""
    <style>
    .stApp { background-color: #f1f3f6; }
    .zion-header {
        background-color: #1a4d80;
        color: white;
        padding: 15px;
        border-radius: 5px;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 20px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: bold !important;
        color: #1a4d80 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Horário de Brasília
fuso_br = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(fuso_br).strftime('%d/%m/%Y %H:%M:%S')

# Cabeçalho Zion
st.markdown(f'<div class="zion-header"><span>ZION MONITORAMENTO</span><span style="font-size:14px">Atualizado em: {agora}</span></div>', unsafe_allow_html=True)

# Carregamento Direto dos Dados
URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # --- LINHA 1: KPIs ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Total Abastecimentos", len(df))
    
    # Lógica de Fornecedor
    top_forn = df['FORNECEDOR'].value_counts().idxmax() if not df.empty else "N/A"
    c3.metric("Top Fornecedor", top_forn)
    c4.metric("Cidades Atendidas", df['LOCAL'].nunique())

    st.markdown("<br>", unsafe_allow_html=True)

    # --- LINHA 2: LAYOUT ANALYTICS (Ranking à esquerda, Mapa à direita) ---
    col_rank, col_mapa = st.columns([1, 2])

    with col_rank:
        st.subheader("🏢 Ranking Fornecedores")
        df_forn = df.groupby('FORNECEDOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS')
        fig_f = px.bar(df_forn, x='QTOS LTS', y='FORNECEDOR', orientation='h', text_auto=True)
        fig_f.update_layout(height=300, margin=dict(t=10, b=10, l=0, r=0), paper_bgcolor='white', plot_bgcolor='white')
        st.plotly_chart(fig_f, use_container_width=True)

        st.subheader("🚢 Empurradores")
        df_pie = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index()
        fig_pie = px.pie(df_pie, values='QTOS LTS', names='EMPURRADOR', hole=0.6)
        fig_pie.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_mapa:
        st.subheader("📍 Cobertura Geográfica")
        df_uf = df.groupby('ESTADO')['QTOS LTS'].sum().reset_index()
        # Mapa Coroplético corrigido para evitar o erro de validação
        fig_mapa = px.choropleth(df_uf,
                                locations='ESTADO',
                                locationmode='BRA-states',
                                color='QTOS LTS',
                                color_continuous_scale="Blues",
                                scope='south america')
        fig_mapa.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='white')
        st.plotly_chart(fig_mapa, use_container_width=True)

    # --- LINHA 3: VOLUME POR EMPURRADOR ---
    st.markdown("---")
    st.subheader("📊 Volume Detalhado por Empurrador")
    df_bar = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
    fig_bar = px.bar(df_bar, x='EMPURRADOR', y='QTOS LTS', text_auto=True, color_discrete_sequence=['#1a4d80'])
    st.plotly_chart(fig_bar, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar os dados. Verifique a planilha: {e}")

# Atualização Automática (30 Segundos)
st.markdown("""<script>setTimeout(function(){ window.location.reload(); }, 30000);</script>""", unsafe_allow_html=True)
