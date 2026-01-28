import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração de Página
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO GIGANTE EXTREMO (80px) ---
st.markdown("""
    <style>
    .stApp { background-color: #000b1a; color: white; }
    
    .zion-header {
        background-color: #001f3f; color: #00ffcc; padding: 20px; 
        border-radius: 15px; font-size: 45px; font-weight: 900; 
        text-align: center; border: 4px solid #00ffcc; margin-bottom: 40px;
        text-transform: uppercase;
    }

    /* CARDS DOS NÚMEROS */
    div[data-testid="stMetric"] {
        background-color: #001529; border: 4px solid #00d4ff;
        border-radius: 25px; padding: 50px !important; text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    /* NÚMEROS EM TAMANHO 80px E NEGRITO EXTRA */
    div[data-testid="stMetricValue"] {
        font-size: 80px !important; 
        font-weight: 900 !important; 
        color: #00ffcc !important;
        line-height: 1.0;
        letter-spacing: -2px;
    }

    /* TEXTO DOS PAINÉIS (LEGENDA) */
    label[data-testid="stMetricLabel"] { 
        color: #ffffff !important; 
        font-size: 35px !important; 
        font-weight: 800 !important;
        margin-bottom: 20px !important;
        text-transform: uppercase;
    }
    
    /* AJUSTE DOS GRÁFICOS PARA TAMANHO GRANDE */
    .js-plotly-plot .plotly .xaxis-title, .js-plotly-plot .plotly .yaxis-title {
        font-size: 24px !important;
        font-weight: 900 !important;
    }
    .js-plotly-plot .plotly .tick text {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="zion-header">ZION MONITORAMENTO</div>', unsafe_allow_html=True)

URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # --- PAINÉIS DE APRESENTAÇÃO (80px) ---
    c1, c2 = st.columns(2)
    with c1:
        total_comprado = int(df['QTOS LTS'].sum())
        # Formatação com ponto para milhares
        st.metric("TOTAL COMPRADO (L)", f"{total_comprado:,}".replace(",", "."))
    with c2:
        st.metric("ABASTECIMENTOS", len(df))

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- GRÁFICOS REFORÇADOS ---
    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.markdown("<h2 style='text-align: center; font-size: 30px;'>🚢 LITROS POR EMPURRADOR</h2>", unsafe_allow_html=True)
        df_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
        fig_emp = px.bar(df_emp, x='EMPURRADOR', y='QTOS LTS', text_auto='.2s', color_discrete_sequence=['#00ffcc'])
        fig_emp.update_traces(textfont_size=22, textposition='outside')
        fig_emp.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
        st.plotly_chart(fig_emp, use_container_width=True)

    with col_dir:
        st.markdown("<h2 style='text-align: center; font-size: 30px;'>🏢 RANKING FORNECEDORES</h2>", unsafe_allow_html=True)
        df_forn = df['FORNECEDOR'].value_counts().reset_index()
        df_forn.columns = ['FORNECEDOR', 'ATENDIMENTOS']
        fig_forn = px.bar(df_forn, x='ATENDIMENTOS', y='FORNECEDOR', orientation='h', text_auto=True, color_discrete_sequence=['#00d4ff'])
        fig_forn.update_traces(textfont_size=22, textposition='outside')
        fig_forn.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
        st.plotly_chart(fig_forn, use_container_width=True)

except Exception as e:
    st.error("Erro na leitura dos dados. Verifique a planilha.")

# Auto-refresh de 30 segundos
st.markdown("""<script>setTimeout(function(){ window.location.reload(); }, 30000);</script>""", unsafe_allow_html=True)
