import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração de Página
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO GIGANTE (60px) E CORES NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000b1a; color: white; }
    .zion-header {
        background-color: #001f3f; color: #00ffcc; padding: 15px; 
        border-radius: 10px; font-size: 35px; font-weight: bold; 
        text-align: center; border: 2px solid #00ffcc; margin-bottom: 25px;
    }
    /* Estilo dos Cards */
    div[data-testid="stMetric"] {
        background-color: #001529; border: 2px solid #00ffcc;
        border-radius: 15px; padding: 30px; text-align: center;
    }
    /* NÚMEROS EM TAMANHO 60px - PARA ENXERGAR DE LONGE */
    div[data-testid="stMetricValue"] {
        font-size: 60px !important; 
        font-weight: 800 !important; 
        color: #00ffcc !important;
        line-height: 1.2;
    }
    /* Tamanho das etiquetas dos cards */
    label[data-testid="stMetricLabel"] { 
        color: #ffffff !important; 
        font-size: 24px !important; 
        font-weight: bold !important;
    }
    /* Aumentar fonte dos gráficos */
    .js-plotly-plot .plotly .xaxis-title, .js-plotly-plot .plotly .yaxis-title { font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="zion-header">ZION MONITORAMENTO - RESUMO DE OPERAÇÕES</div>', unsafe_allow_html=True)

URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    
    # Limpeza rigorosa para evitar erros de tipo
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)
    df['FORNECEDOR'] = df['FORNECEDOR'].astype(str).fillna("N/A")
    df['EMPURRADOR'] = df['EMPURRADOR'].astype(str).fillna("N/A")

    # --- KPIs GIGANTES NO TOPO ---
    c1, c2 = st.columns(2)
    with c1:
        st.metric("TOTAL COMPRADO (LITROS)", f"{int(df['QTOS LTS'].sum()):,}".replace(",", "."))
    with c2:
        st.metric("TOTAL DE ABASTECIMENTOS", len(df))

    st.markdown("<br><br>", unsafe_allow_html=True)

    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.subheader("🚢 Litros por Empurrador")
        df_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
        fig_emp = px.bar(df_emp, x='EMPURRADOR', y='QTOS LTS', text_auto='.2s', 
                         color_discrete_sequence=['#00ffcc'])
        fig_emp.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font=dict(size=16))
        st.plotly_chart(fig_emp, use_container_width=True)

    with col_dir:
        st.subheader("🏢 Ranking de Fornecedores")
        df_forn = df['FORNECEDOR'].value_counts().reset_index()
        df_forn.columns = ['FORNECEDOR', 'ATENDIMENTOS']
        fig_forn = px.bar(df_forn, x='ATENDIMENTOS', y='FORNECEDOR', orientation='h', 
                          text_auto=True, color_discrete_sequence=['#00d4ff'])
        fig_forn.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               font=dict(size=16))
        st.plotly_chart(fig_forn, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados. Verifique a planilha.")
