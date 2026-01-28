import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# BLOCO 1: CONFIGURAÇÕES DE TAMANHO E COR (MEXA AQUI)
# =========================================================
TAMANHO_NUMERO = "100px"      # Tamanho do número (80, 90, 100...)
TAMANHO_LEGENDA = "40px"     # Tamanho do texto acima do número
COR_NEON = "#00ffcc"         # Cor Verde Água Neon
FONTE_PESO = "900"           # Grossura da letra (Negrito Máximo)

st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

st.markdown(f"""
    <style>
    .stApp {{ background-color: #000b1a; color: white; }}
    
    .zion-header {{
        background-color: #001f3f; color: {COR_NEON}; padding: 20px; 
        border-radius: 15px; font-size: 45px; font-weight: 900; 
        text-align: center; border: 4px solid {COR_NEON}; margin-bottom: 40px;
    }}

    /* CARDS DOS NÚMEROS */
    div[data-testid="stMetric"] {{
        background-color: #001529; border: 4px solid #00d4ff;
        border-radius: 25px; padding: 50px !important; text-align: center;
    }}

    /* NÚMEROS GIGANTES */
    div[data-testid="stMetricValue"] {{
        font-size: {TAMANHO_NUMERO} !important; 
        font-weight: {FONTE_PESO} !important; 
        color: {COR_NEON} !important;
        line-height: 1.0;
    }}

    /* TEXTO DOS PAINÉIS */
    label[data-testid="stMetricLabel"] {{ 
        color: #ffffff !important; 
        font-size: {TAMANHO_LEGENDA} !important; 
        font-weight: 800 !important;
        text-transform: uppercase;
    }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# BLOCO 2: DADOS (NÃO MEXER AQUI)
# =========================================================
URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)
    df['FORNECEDOR'] = df['FORNECEDOR'].astype(str)
    df['EMPURRADOR'] = df['EMPURRADOR'].astype(str)

    # TÍTULO NO TOPO
    st.markdown('<div class="zion-header">ZION MONITORAMENTO</div>', unsafe_allow_html=True)

    # EXIBIÇÃO DOS PAINÉIS
    c1, c2 = st.columns(2)
    with c1:
        total_lts = int(df['QTOS LTS'].sum())
        st.metric("TOTAL COMPRADO (L)", f"{total_lts:,}".replace(",", "."))
    with c2:
        st.metric("ABASTECIMENTOS", len(df))

    st.markdown("<br><br>", unsafe_allow_html=True)

    # GRÁFICOS ABAIXO
    col_esq, col_dir = st.columns(2)
    with col_esq:
        st.markdown("<h3 style='text-align:center;'>🚢 LITROS POR EMPURRADOR</h3>", unsafe_allow_html=True)
        fig1 = px.bar(df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index(), 
                      x='EMPURRADOR', y='QTOS LTS', text_auto='.2s')
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', font=dict(size=18))
        st.plotly_chart(fig1, use_container_width=True)

    with col_dir:
        st.markdown("<h3 style='text-align:center;'>🏢 RANKING FORNECEDORES</h3>", unsafe_allow_html=True)
        df_forn = df['FORNECEDOR'].value_counts().reset_index()
        fig2 = px.bar(df_forn, x='count', y='FORNECEDOR', orientation='h', text_auto=True)
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', font=dict(size=18))
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Erro nos dados: {e}")

# REFRESH AUTOMÁTICO
st.markdown("<script>setTimeout(function(){window.location.reload();},30000);</script>", unsafe_allow_html=True)
