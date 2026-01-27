import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz

# Configuração de alta performance e visual
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO CSS PARA COPIAR A IMAGEM 2 ---
st.markdown("""
    <style>
    /* Fundo da página cinza claro */
    .stApp { background-color: #f4f7f9; }
    
    /* Cabeçalho Zion azul escuro */
    .zion-header {
        background-color: #1a4d80;
        color: white;
        padding: 15px;
        border-radius: 5px;
        text-align: left;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    /* Cards brancos para os números (KPIs) */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 15px;
    }
    
    /* Números grandes e nítidos */
    div[data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: bold !important;
        color: #2c3e50 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Título fixo no topo
st.markdown('<div class="zion-header">ZION MONITORAMENTO</div>', unsafe_allow_html=True)

# Horário de Brasília
fuso_br = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(fuso_br).strftime('%d/%m/%Y %H:%M:%S')

ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

try:
    # Lendo os dados
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # --- LINHA 1: MÉTRICAS TIPO DASHBOARD ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Total Abastecimentos", len(df))
    
    # Lógica para fornecedor e cidades
    top_forn = df['FORNECEDOR'].value_counts().idxmax() if not df.empty else "N/A"
    c3.metric("Top Fornecedor", top_forn)
    c4.metric("Cidades Atendidas", df['LOCAL'].nunique())

    st.write(f"📊 Dados atualizados em: {agora}")
    st.markdown("---")

    # --- LINHA 2: DISTRIBUIÇÃO E MAPA (LAYOUT IMAGEM 2) ---
    col_lateral, col_mapa = st.columns([1, 2])

    with col_lateral:
        st.subheader("🏢 Ranking Fornecedores")
        df_f = df.groupby('FORNECEDOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS')
        fig_f = px.bar(df_f, x='QTOS LTS', y='FORNECEDOR', orientation='h',
                       text_auto=True, color_discrete_sequence=['#3498db'])
        fig_f.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig_f, use_container_width=True)

        st.subheader("🚢 Uso por Empurrador")
        df_emp_pie = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index()
        fig_pie = px.pie(df_emp_pie, values='QTOS LTS', names='EMPURRADOR', hole=0.5,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_mapa:
        st.subheader("📍 Cobertura Geográfica por Estado")
        df_uf = df.groupby('ESTADO')['QTOS LTS'].sum().reset_index()
        # Mapa com cores nítidas e claras
        fig_mapa = px.choropleth(df_uf,
                                locations='ESTADO',
                                locationmode='BRA-states',
                                color='QTOS LTS',
                                color_continuous_scale="Blues",
                                scope='south america')
        fig_mapa.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_mapa, use_container_width=True)

    # --- LINHA 3: GRÁFICO DE BARRAS POR EMPURRADOR (VOLUME REAL) ---
    st.markdown("---")
    st.subheader("📊 Volume Abastecido por Empurrador")
    df_emp_bar = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
    fig_bar = px.bar(df_emp_bar, x='EMPURRADOR', y='QTOS LTS', text_auto=True,
                     color='QTOS LTS', color_continuous_scale='Blues')
    fig_bar.update_layout(xaxis_title="", yaxis_title="Litros (L)")
    st.plotly_chart(fig_bar, use_container_width=True)

except Exception as e:
    st.info("🔄 Sincronizando com a planilha Google... Por favor, aguarde alguns segundos.")

# Refresh automático de 30s para ser 100% automático
st.markdown("""<script>setTimeout(function(){ window.location.reload(); }, 30000);</script>""", unsafe_allow_html=True)
