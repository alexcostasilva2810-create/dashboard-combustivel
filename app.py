import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração Básica
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO: FUNDO AZUL ESCURO + NÚMEROS GIGANTES (50px) ---
st.markdown("""
    <style>
    .stApp { background-color: #000b1a; color: white; }
    .zion-header {
        background-color: #001f3f; color: #00d4ff; padding: 20px; 
        border-radius: 10px; font-size: 35px; font-weight: bold; 
        text-align: center; border: 2px solid #00d4ff; margin-bottom: 25px;
    }
    div[data-testid="stMetric"] {
        background-color: #001529; border: 1px solid #00d4ff;
        border-radius: 15px; padding: 20px;
    }
    /* NÚMEROS EM TAMANHO 50 */
    div[data-testid="stMetricValue"] { font-size: 50px !important; font-weight: bold !important; color: #00ffcc !important; }
    label[data-testid="stMetricLabel"] { color: white !important; font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="zion-header">ZION MONITORAMENTO - RESUMO DE OPERAÇÕES</div>', unsafe_allow_html=True)

# Link da Planilha
URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    
    # GARANTE QUE OS NÚMEROS SEJAM NÚMEROS (Evita o erro da imagem)
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # 1. TOTAL COMPRADO NO PERÍODO & TOTAL GERAL DE ABASTECIMENTOS
    c1, c2 = st.columns(2)
    c1.metric("Total Comprado (Litros)", f"{int(df['QTOS LTS'].sum()):,}".replace(",", "."))
    c2.metric("Total de Abastecimentos", len(df))

    st.markdown("---")

    col_esq, col_dir = st.columns(2)

    with col_esq:
        # 2. QUANTOS LITROS CADA EMPURRADOR RECEBEU
        st.subheader("🚢 Litros por Empurrador")
        df_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
        fig_emp = px.bar(df_emp, x='EMPURRADOR', y='QTOS LTS', text_auto=True, 
                         color_discrete_sequence=['#00d4ff'])
        fig_emp.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_emp, use_container_width=True)

    with col_dir:
        # 3. RANKING DOS FORNECEDORES QUE MAIS ATENDERAM
        st.subheader("🏢 Ranking de Fornecedores (Qtd. Atendimentos)")
        df_forn = df['FORNECEDOR'].value_counts().reset_index()
        df_forn.columns = ['FORNECEDOR', 'ATENDIMENTOS']
        fig_forn = px.bar(df_forn, x='ATENDIMENTOS', y='FORNECEDOR', orientation='h', 
                          text_auto=True, color_discrete_sequence=['#00ffcc'])
        fig_forn.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_forn, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao ler os dados: {e}")
