import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Gestão de Combustível PRO", layout="wide")

# 2. Estilização Azul Royal e Números Grandes
st.markdown("""
    <style>
    /* Fundo Azul Royal Degradê */
    .stApp {
        background: linear-gradient(135deg, #002366 0%, #000080 100%);
        color: white;
    }
    
    /* Títulos e textos */
    h1, h2, h3, p { color: white !important; }

    /* Estilização dos Números (KPIs) - Tamanho 30, Negrito e Contraste */
    [data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: bold !important;
        color: #00f2ff !important; /* Ciano para contraste com azul royal */
    }
    
    /* Estilização dos Rótulos dos KPIs */
    [data-testid="stMetricLabel"] {
        font-size: 18px !important;
        color: #ffffff !important;
    }

    /* Bordas dos Gráficos */
    .stPlotlyChart {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Link da sua Planilha
ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    st.title("🚢 Painel Executivo - Gestão de Combustível")
    st.markdown("---")

    # --- KPIs TOPO (Números 30px Negrito) ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Volume Total", f"{df['QTOS LTS'].sum():,.0f} L")
    c2.metric("Total Abastecimentos", len(df))
    c3.metric("Localidades", df['LOCAL'].nunique())

    st.markdown("---")

    # --- GRÁFICOS COM DESIGN ELEGANTE ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⛽ Litros por Empurrador")
        resumo_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index()
        fig_litros = px.bar(resumo_emp, x='EMPURRADOR', y='QTOS LTS', 
                            text_auto='.2s',
                            template="plotly_dark")
        fig_litros.update_traces(marker_color='#00f2ff') # Cor das barras para contraste
        st.plotly_chart(fig_litros, use_container_width=True)

    with col2:
        st.subheader("📍 Frequência por Localidade")
        df_local = df.groupby('LOCAL').size().reset_index(name='Vezes')
        fig_local = px.pie(df_local, values='Vezes', names='LOCAL', 
                           hole=0.4, template="plotly_dark")
        fig_local.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_local, use_container_width=True)

    # Tabela detalhada
    with st.expander("🔍 Ver base de dados completa"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Aguardando conexão com os dados... {e}")
