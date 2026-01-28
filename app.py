import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração de Página
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO GIGANTE (70px) E CORES FORTES ---
st.markdown("""
    <style>
    .stApp { background-color: #000b1a; color: white; }
    
    .zion-header {
        background-color: #001f3f; color: #00ffcc; padding: 20px; 
        border-radius: 15px; font-size: 40px; font-weight: 800; 
        text-align: center; border: 3px solid #00ffcc; margin-bottom: 30px;
    }

    /* CARDS DOS NÚMEROS */
    div[data-testid="stMetric"] {
        background-color: #001529; border: 3px solid #00d4ff;
        border-radius: 20px; padding: 40px !important; text-align: center;
    }

    /* NÚMEROS EM TAMANHO 70px - PARA LER DE LONGE */
    div[data-testid="stMetricValue"] {
        font-size: 70px !important; 
        font-weight: 900 !important; 
        color: #00ffcc !important;
        line-height: 1.1;
    }

    /* TEXTO DOS PAINÉIS (LETRAS GRANDES) */
    label[data-testid="stMetricLabel"] { 
        color: #ffffff !important; 
        font-size: 30px !important; 
        font-weight: 700 !important;
        margin-bottom: 15px !important;
    }
    
    /* AUMENTAR LETRAS DOS GRÁFICOS */
    .js-plotly-plot .plotly .xaxis-title, .js-plotly-plot .plotly .yaxis-title, .js-plotly-plot .plotly .tick text {
        font-size: 20px !important;
        font-weight: bold !important;
        fill: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="zion-header">ZION MONITORAMENTO</div>', unsafe_allow_html=True)

URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    # Corrige erro de tipo
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # --- PAINÉIS DE APRESENTAÇÃO (LETRA 70px) ---
    c1, c2 = st.columns(2)
    with c1:
        total_comprado = int(df['QTOS LTS'].sum())
        st.metric("TOTAL COMPRADO (L)", f"{total_comprado:,}".replace(",", "."))
    with c2:
        st.metric("ABASTECIMENTOS", len(df))

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- GRÁFICOS COM LETRAS GRANDES ---
    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.markdown("### 🚢 LITROS POR EMPURRADOR")
        df_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
        fig_emp = px.bar(df_emp, x='EMPURRADOR', y='QTOS LTS', text_auto='.2s', color_discrete_sequence=['#00ffcc'])
        fig_emp.update_traces(textfont_size=20) # Número dentro da barra maior
        fig_emp.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=20))
        st.plotly_chart(fig_emp, use_container_width=True)

    with col_dir:
        st.markdown("### 🏢 RANKING DE FORNECEDORES")
        df_forn = df['FORNECEDOR'].value_counts().reset_index()
        df_forn.columns = ['FORNECEDOR', 'ATENDIMENTOS']
        fig_forn = px.bar(df_forn, x='ATENDIMENTOS', y='FORNECEDOR', orientation='h', text_auto=True, color_discrete_sequence=['#00d4ff'])
        fig_forn.update_traces(textfont_size=20) # Número dentro da barra maior
        fig_forn.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=20))
        st.plotly_chart(fig_forn, use_container_width=True)

except Exception as e:
    st.error("Erro na leitura da Planilha Google.")
