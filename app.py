import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONFIGURAÇÃO DE TAMANHO - MEXA SÓ AQUI PARA MUDAR A FONTE
# =========================================================
TAMANHO_FONTE_KPI = "50px"    # <--- AQUI MUDA O NÚMERO GIGANTE
TAMANHO_FONTE_TEXTO = "45px"  # <--- AQUI MUDA O NOME EM CIMA DO NÚMERO
COR_DO_NUMERO = "#00ffcc"      # VERDE NEON
# =========================================================

st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# Este bloco abaixo aplica o tamanho que você escolheu ali em cima
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000b1a; color: white; }}
    
    /* ESTILO DOS CARDS */
    div[data-testid="stMetric"] {{
        background-color: #001529; border: 4px solid #00d4ff;
        border-radius: 40px; padding: 50px !important; text-align: center;
    }}

    /* AQUI É ONDE A MÁGICA ACONTECE NO NÚMERO (KPI) */
    div[data-testid="stMetricValue"] {{
        font-size: {TAMANHO_FONTE_KPI} !important; 
        font-weight: 900 !important; 
        color: {COR_DO_NUMERO} !important;
        line-height: 1;
    }}

    /* AQUI É ONDE A MÁGICA ACONTECE NA LEGENDA */
    label[data-testid="stMetricLabel"] {{ 
        font-size: {TAMANHO_FONTE_TEXTO} !important; 
        font-weight: 800 !important;
        color: white !important;
        text-transform: uppercase;
    }}
    </style>
    """, unsafe_allow_html=True)

# CONEXÃO COM A PLANILHA
URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    # Corrige o erro de 'float' e 'str' que apareceu na sua imagem
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    st.markdown(f"<h1 style='text-align:center; color:{COR_DO_NUMERO}; font-size:50px;'>ZION MONITORAMENTO</h1>", unsafe_allow_html=True)

    # EXIBIÇÃO DOS PAINÉIS LADO A LADO
    c1, c2 = st.columns(2)
    with c1:
        total_lts = int(df['QTOS LTS'].sum())
        st.metric("TOTAL COMPRADO (L)", f"{total_lts:,}".replace(",", "."))
    with c2:
        st.metric("ABASTECIMENTOS", len(df))

    st.markdown("---")

    # GRÁFICOS QUE VOCÊ PEDIU
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h2 style='text-align:center;'>LITROS POR EMPURRADOR</h2>", unsafe_allow_html=True)
        # Agrupa os litros por empurrador como você exigiu
        resumo_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index()
        fig1 = px.bar(resumo_emp, x='EMPURRADOR', y='QTOS LTS', text_auto='.2s', color_discrete_sequence=[COR_DO_NUMERO])
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', font=dict(size=20))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("<h2 style='text-align:center;'>RANKING FORNECEDORES</h2>", unsafe_allow_html=True)
        # Conta os atendimentos por fornecedor
        df_forn = df['FORNECEDOR'].value_counts().reset_index()
        fig2 = px.bar(df_forn, x='count', y='FORNECEDOR', orientation='h', text_auto=True, color_discrete_sequence=['#00d4ff'])
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', font=dict(size=20))
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")

# Refresh automático
st.markdown("<script>setTimeout(function(){window.location.reload();},30000);</script>", unsafe_allow_html=True)
