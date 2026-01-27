import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz

# Forçar atualização em tempo real (Sem Cache)
st.cache_data.clear()

st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")

# --- ESTILO VISUAL PREMIUM (AZUL ROYAL + CONTRASTE) ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; }
    /* Topo Zion */
    .zion-header {
        background-color: #1e3a8a;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        letter-spacing: 5px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    /* Cards de Métricas */
    div[data-testid="stMetricValue"] { 
        font-size: 40px !important; 
        font-weight: bold !important; 
        color: #1e3a8a !important; 
    }
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho Fixo
st.markdown('<div class="zion-header">ZION MONITORAMENTO</div>', unsafe_allow_html=True)

# Horário de Brasília
fuso_br = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(fuso_br).strftime('%d/%m/%Y %H:%M:%S')

ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    st.write(f"⏱️ **Sincronização Ativa:** {agora}")

    # --- LINHA 1: KPIs ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("VOLUME TOTAL", f"{int(df['QTOS LTS'].sum())} L")
    c2.metric("ABASTECIMENTOS", len(df))
    
    # Top Fornecedor
    top_forn = df['FORNECEDOR'].value_counts().idxmax() if not df.empty else "N/A"
    c3.metric("TOP FORNECEDOR", top_forn)
    
    c4.metric("CIDADES", df['LOCAL'].nunique())

    st.markdown("---")

    # --- LINHA 2: MAPA UF E RANKING ---
    col_mapa, col_forn = st.columns([6, 4])

    with col_mapa:
        st.subheader("📍 Cobertura por Estado (UF)")
        df_uf = df.groupby('ESTADO')['QTOS LTS'].sum().reset_index()
        # Mapa coroplético focado no Brasil
        fig_mapa = px.choropleth(df_uf,
                                locations='ESTADO',
                                locationmode='BRA-states',
                                color='QTOS LTS',
                                color_continuous_scale="Blues",
                                scope='south america')
        fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_mapa, use_container_width=True)

    with col_forn:
        st.subheader("🏢 Ranking de Fornecedores")
        df_f = df.groupby('FORNECEDOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS')
        fig_f = px.bar(df_f, x='QTOS LTS', y='FORNECEDOR', orientation='h', 
                       text_auto='.0f', color='QTOS LTS', color_continuous_scale='Blues')
        fig_f.update_layout(showlegend=False)
        st.plotly_chart(fig_f, use_container_width=True)

    st.markdown("---")

    # --- LINHA 3: ANÁLISE EMPURRADOR ---
    st.subheader("🚢 Performance por Empurrador")
    resumo_emp = df.groupby('EMPURRADOR').agg({'QTOS LTS': 'sum', 'ID': 'count'}).reset_index()
    resumo_emp.columns = ['EMPURRADOR', 'LITROS', 'QTD']

    c_emp1, c_emp2 = st.columns(2)
    with c_emp1:
        fig_l = px.bar(resumo_emp, x='EMPURRADOR', y='LITROS', text_auto='.0f', title="Total de Litros")
        st.plotly_chart(fig_l, use_container_width=True)
    with c_emp2:
        fig_q = px.pie(resumo_emp, values='QTD', names='EMPURRADOR', hole=0.4, title="Qtd de Abastecimentos")
        st.plotly_chart(fig_q, use_container_width=True)

except Exception as e:
    st.error("Conectando à base de dados...")

# Script de Refresh Automático (30 segundos)
st.markdown("""
    <script>
    setTimeout(function(){ window.location.reload(); }, 30000);
    </script>
    """, unsafe_allow_html=True)
