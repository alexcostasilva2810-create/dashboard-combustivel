import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração de Página
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO "SUPER VISÃO" (70px) COM BRILHO NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000b1a; color: white; }
    
    .zion-header {
        background-color: #001f3f; 
        color: #00ffcc; 
        padding: 20px; 
        border-radius: 15px; 
        font-size: 38px; 
        font-weight: 800; 
        text-align: center; 
        border: 3px solid #00ffcc; 
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* ESTILO DOS CARDS DOS NÚMEROS */
    div[data-testid="stMetric"] {
        background-color: #001529; 
        border: 3px solid #00d4ff;
        border-radius: 20px; 
        padding: 40px !important; 
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }

    /* NÚMEROS EM TAMANHO 70px - FOCO TOTAL NA INFORMAÇÃO */
    div[data-testid="stMetricValue"] {
        font-size: 70px !important; 
        font-weight: 900 !important; 
        color: #00ffcc !important;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5); /* Efeito de brilho */
        line-height: 1.1;
    }

    /* Rótulos dos cards (O que é a informação) */
    label[data-testid="stMetricLabel"] { 
        color: #ffffff !important; 
        font-size: 26px !important; 
        font-weight: 700 !important;
        margin-bottom: 15px !important;
    }
    
    /* Ajuste para telas menores não cortarem o número */
    @media (max-width: 1200px) {
        div[data-testid="stMetricValue"] { font-size: 50px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="zion-header">ZION MONITORAMENTO - GESTÃO DE ABASTECIMENTO</div>', unsafe_allow_html=True)

URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    # Carregamento e tratamento rigoroso
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # --- KPIs GIGANTES (70px) ---
    c1, c2 = st.columns(2)
    with c1:
        # Formatação com ponto para facilitar leitura de milhares
        total_lts = int(df['QTOS LTS'].sum())
        st.metric("TOTAL COMPRADO (L)", f"{total_lts:,}".replace(",", "."))
    with c2:
        st.metric("QTD ABASTECIMENTOS", len(df))

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- GRÁFICOS DE APOIO ---
    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.subheader("🚢 Litros por Empurrador")
        df_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
        fig_emp = px.bar(df_emp, x='EMPURRADOR', y='QTOS LTS', text_auto='.2s', 
                         color_discrete_sequence=['#00ffcc'])
        fig_emp.update_layout(
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=18)
        )
        st.plotly_chart(fig_emp, use_container_width=True)

    with col_dir:
        st.subheader("🏢 Ranking de Fornecedores")
        df_forn = df['FORNECEDOR'].value_counts().reset_index()
        df_forn.columns = ['FORNECEDOR', 'ATENDIMENTOS']
        fig_forn = px.bar(df_forn, x='ATENDIMENTOS', y='FORNECEDOR', orientation='h', 
                          text_auto=True, color_discrete_sequence=['#00d4ff'])
        fig_forn.update_layout(
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=18)
        )
        st.plotly_chart(fig_forn, use_container_width=True)

except Exception as e:
    st.error("Erro ao carregar dados. Verifique a planilha.")
