import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONTROLE DE TAMANHOS (AJUSTE AQUI SE PRECISAR)
# =========================================================
TAMANHO_TITULO_ZION = "65px"
TAMANHO_KPI_NUMERO = "85px"
TAMANHO_KPI_TEXTO = "35px"
TAMANHO_LETRAS_GRAFICOS = 28  # Eixos e legendas
TAMANHO_VALOR_BARRAS = 35    # Números em cima das barras

st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")

# --- ESTILO VISUAL ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000b1a; color: white; }}
    
    /* TÍTULO PRINCIPAL */
    .zion-main-title {{
        text-align: center; 
        color: #00ffcc; 
        font-size: {TAMANHO_TITULO_ZION}; 
        font-weight: 900; 
        margin-bottom: 40px;
        text-transform: uppercase;
        letter-spacing: 5px;
        border-bottom: 3px solid #00ffcc;
        padding-bottom: 10px;
    }}

    /* CARDS DE NÚMEROS (KPIs) */
    div[data-testid="stMetric"] {{
        background-color: #001529; border: 4px solid #00d4ff;
        border-radius: 20px; padding: 40px !important; text-align: center;
    }}
    div[data-testid="stMetricValue"] {{ 
        font-size: {TAMANHO_KPI_NUMERO} !important; 
        font-weight: 900 !important; 
        color: #00ffcc !important; 
    }}
    label[data-testid="stMetricLabel"] {{ 
        font-size: {TAMANHO_KPI_TEXTO} !important; 
        font-weight: bold !important; 
        color: white !important; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO NO TOPO ---
st.markdown('<div class="zion-main-title">ZION MONITORAMENTO</div>', unsafe_allow_html=True)

URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    # Carregamento e Limpeza
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # --- LINHA 1: KPIs GIGANTES ---
    c1, c2 = st.columns(2)
    with c1:
        total_lts = int(df['QTOS LTS'].sum())
        st.metric("TOTAL COMPRADO (L)", f"{total_lts:,}".replace(",", "."))
    with c2:
        st.metric("QTD ABASTECIMENTOS", len(df))

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- LINHA 2: GRÁFICOS REFORÇADOS ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h3 style='text-align:center; font-size:30px;'>🚢 LITROS POR EMPURRADOR</h3>", unsafe_allow_html=True)
        resumo_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
        fig1 = px.bar(resumo_emp, x='EMPURRADOR', y='QTOS LTS', text_auto='.2s', color_discrete_sequence=['#00ffcc'])
        
        fig1.update_traces(textfont_size=TAMANHO_VALOR_BARRAS, textposition='outside')
        fig1.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(size=TAMANHO_LETRAS_GRAFICOS), title=None),
            yaxis=dict(tickfont=dict(size=TAMANHO_LETRAS_GRAFICOS), title=None),
            margin=dict(t=50)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown(f"<h3 style='text-align:center; font-size:30px;'>🏢 RANKING FORNECEDORES</h3>", unsafe_allow_html=True)
        df_forn = df['FORNECEDOR'].value_counts().reset_index()
        fig2 = px.bar(df_forn, x='count', y='FORNECEDOR', orientation='h', text_auto=True, color_discrete_sequence=['#00d4ff'])
        
        fig2.update_traces(textfont_size=TAMANHO_VALOR_BARRAS, textposition='outside')
        fig2.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(size=TAMANHO_LETRAS_GRAFICOS), title=None),
            yaxis=dict(tickfont=dict(size=TAMANHO_LETRAS_GRAFICOS), title=None),
            margin=dict(t=50)
        )
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados da Planilha: {e}")

# Refresh automático a cada 30 segundos
st.markdown("<script>setTimeout(function(){window.location.reload();},30000);</script>", unsafe_allow_html=True)
