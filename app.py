import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")

#------------------------------------------------------------------------------#
#       BLOCO 1: TÍTULO PRINCIPAL (ZION MONITORAMENTO)
#------------------------------------------------------------------------------#
# Aumente ou diminua o 'size' para mudar o tamanho do título no topo.
TAMANHO_TITULO_TOPO = "75px" 
COR_TITULO_TOPO = "#00ffcc"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #000b1a; color: white; }}
    .zion-titulo {{
        text-align: center; color: {COR_TITULO_TOPO}; 
        font-size: {TAMANHO_TITULO_TOPO}; font-weight: 900; 
        margin-bottom: 30px; border-bottom: 4px solid {COR_TITULO_TOPO};
    }}
    </style>
    <div class="zion-titulo">ZION MONITORAMENTO</div>
    """, unsafe_allow_html=True)


#------------------------------------------------------------------------------#
#       BLOCO 2: PAINÉIS SUPERIORES (KPIs - NÚMEROS GIGANTES)
#------------------------------------------------------------------------------#
# Ajuste aqui o tamanho dos números de Litros e Abastecimentos.
TAMANHO_NUMEROS_PAINEL = "95px"   # O número grande
TAMANHO_LETRAS_PAINEL = "50px"    # O texto explicativo
COR_VALOR_PAINEL = "#00ffcc"

st.markdown(f"""
    <style>
    div[data-testid="stMetricValue"] {{ 
        font-size: {TAMANHO_NUMEROS_PAINEL} !important; 
        font-weight: 900 !important; color: {COR_VALOR_PAINEL} !important; 
    }}
    label[data-testid="stMetricLabel"] {{ 
        font-size: {TAMANHO_LETRAS_PAINEL} !important; 
        font-weight: 800 !important; color: white !important; 
    }}
    div[data-testid="stMetric"] {{
        background-color: #001529; border: 4px solid #00d4ff;
        border-radius: 20px; padding: 40px !important; text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# Conexão com os Dados
URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"
try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        v_total = int(df['QTOS LTS'].sum())
        st.metric("TOTAL COMPRADO (L)", f"{v_total:,}".replace(",", "."))
    with col_kpi2:
        st.metric("TOTAL ABASTECIMENTOS", len(df))
except:
    st.error("Erro na Planilha")


#------------------------------------------------------------------------------#
#       BLOCO 3: LITROS POR EMPURRADOR (GRÁFICO ESQUERDA)
#------------------------------------------------------------------------------#
# Mexa aqui para aumentar o tamanho do gráfico e das letras da esquerda.
ALTURA_GR_EMPURRADOR = 650
FONTE_NOMES_EMPURRADOR = 35    # Nomes dos barcos (Samauma, etc)
FONTE_VALOR_BARRA_EMP = 30     # Números em cima das barras

st.markdown("---")
col_esq, col_dir = st.columns(2)

with col_esq:
    st.markdown("<h2 style='text-align:center; font-size:35px;'>🚢 LITROS POR EMPURRADOR</h2>", unsafe_allow_html=True)
    df_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
    fig_emp = px.bar(df_emp, x='EMPURRADOR', y='QTOS LTS', text_auto='.2s')
    
    fig_emp.update_traces(marker_color='#00ffcc', textfont_size=FONTE_VALOR_BARRA_EMP, textposition='outside')
    fig_emp.update_layout(
        height=ALTURA_GR_EMPURRADOR, template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(size=FONTE_NOMES_EMPURRADOR), title=None),
        yaxis=dict(tickfont=dict(size=FONTE_NOMES_EMPURRADOR), title=None)
    )
    st.plotly_chart(fig_emp, use_container_width=True)


#------------------------------------------------------------------------------#
#       BLOCO 4: RANKING FORNECEDORES (GRÁFICO DIREITA)
#------------------------------------------------------------------------------#
# Mexa aqui para aumentar o tamanho das letras do ranking.
ALTURA_GR_FORNECEDOR = 650
FONTE_NOMES_FORNECEDOR = 35    # Nomes das empresas
FONTE_VALOR_BARRA_FORN = 40    # Quantidade de atendimentos

with col_dir:
    st.markdown("<h2 style='text-align:center; font-size:35px;'>🏢 RANKING FORNECEDORES</h2>", unsafe_allow_html=True)
    df_forn = df['FORNECEDOR'].value_counts().reset_index()
    fig_forn = px.bar(df_forn, x='count', y='FORNECEDOR', orientation='h', text_auto=True)
    
    fig_forn.update_traces(marker_color='#00d4ff', textfont_size=FONTE_VALOR_BARRA_FORN, textposition='outside')
    fig_forn.update_layout(
        height=ALTURA_GR_FORNECEDOR, template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(size=FONTE_NOMES_FORNECEDOR), title=None),
        yaxis=dict(tickfont=dict(size=FONTE_NOMES_FORNECEDOR), title=None)
    )
    st.plotly_chart(fig_forn, use_container_width=True)

# Atualização da Tela (30 segundos)
st.markdown("<script>setTimeout(function(){window.location.reload();},30000);</script>", unsafe_allow_html=True)
