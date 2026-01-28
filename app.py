import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Configuração de Página
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO LIMPO (IMAGEM 2) COM NÚMEROS TAMANHO 50 ---
st.markdown("""
    <style>
    .stApp { background-color: #f1f3f6; }
    .zion-header {
        background-color: #1a4d80;
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 25px;
    }
    /* Estilo dos Cards Brancos */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* NÚMEROS EM TAMANHO 50 */
    div[data-testid="stMetricValue"] {
        font-size: 50px !important;
        font-weight: bold !important;
        color: #1a4d80 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Título Zion
st.markdown('<div class="zion-header">ZION MONITORAMENTO</div>', unsafe_allow_html=True)

# Horário
fuso_br = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(fuso_br).strftime('%d/%m/%Y %H:%M:%S')

# Carregar Dados sem travar
URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # --- LINHA 1: KPIs GIGANTES (50px) ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Abastecimentos", len(df))
    top_f = df['FORNECEDOR'].value_counts().idxmax() if not df.empty else "---"
    c3.metric("Top Fornecedor", top_f)
    c4.metric("Cidades", df['LOCAL'].nunique())

    st.write(f"🔄 **Sincronizado:** {agora}")
    st.markdown("<br>", unsafe_allow_html=True)

    # --- LINHA 2: LAYOUT SEMELHANTE À IMAGEM 2 ---
    col_lateral, col_central = st.columns([1, 2])

    with col_lateral:
        st.subheader("🏢 Fornecedores")
        df_forn = df.groupby('FORNECEDOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS')
        fig_f = px.bar(df_forn, x='QTOS LTS', y='FORNECEDOR', orientation='h', text_auto=True)
        fig_f.update_layout(height=350, paper_bgcolor='white', plot_bgcolor='white')
        st.plotly_chart(fig_f, use_container_width=True)

        st.subheader("🚢 Frota")
        df_pie = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index()
        fig_pie = px.pie(df_pie, values='QTOS LTS', names='EMPURRADOR', hole=0.5)
        fig_pie.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_central:
        st.subheader("📍 Cobertura de Abastecimento")
        # MAPA SIMPLIFICADO PARA EVITAR ERROS DE VALIDAÇÃO (BRA-states)
        df_uf = df.groupby('ESTADO')['QTOS LTS'].sum().reset_index()
        fig_mapa = px.scatter_geo(df_uf,
                                 locations='ESTADO',
                                 locationmode='country names', # Usando modo universal
                                 color='QTOS LTS',
                                 size='QTOS LTS',
                                 scope='south america',
                                 color_continuous_scale="Blues")
        
        fig_mapa.update_layout(height=650, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='white')
        st.plotly_chart(fig_mapa, use_container_width=True)

    # --- LINHA 3: VOLUME POR EMPURRADOR ---
    st.markdown("---")
    st.subheader("📊 Performance por Empurrador")
    df_bar = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
    fig_bar = px.bar(df_bar, x='EMPURRADOR', y='QTOS LTS', text_auto=True, color_discrete_sequence=['#1a4d80'])
    st.plotly_chart(fig_bar, use_container_width=True)

except Exception as e:
    st.warning("Aguardando atualização dos dados da planilha...")

# Auto-refresh 30s
st.markdown("""<script>setTimeout(function(){ window.location.reload(); }, 30000);</script>""", unsafe_allow_html=True)
