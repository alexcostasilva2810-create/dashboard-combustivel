import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Configurações Iniciais
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO LIMPO (BASEADO NA IMAGEM 2) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .zion-header {
        background-color: #1a4d80;
        color: white;
        padding: 15px;
        border-radius: 5px;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 15px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: bold !important;
        color: #2c3e50 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="zion-header">ZION MONITORAMENTO</div>', unsafe_allow_html=True)

# Fuso Horário
fuso_br = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(fuso_br).strftime('%d/%m/%Y %H:%M:%S')

# Link Direto da Planilha
URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

# Carregamento sem mensagens de espera travadas
df = pd.read_csv(URL)
df.columns = df.columns.str.strip()
df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

if not df.empty:
    # --- KPIs ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Abastecimentos", len(df))
    c3.metric("Top Fornecedor", df['FORNECEDOR'].value_counts().idxmax())
    c4.metric("Cidades", df['LOCAL'].nunique())

    st.write(f"⏱️ **Sincronizado em:** {agora}")
    st.markdown("---")

    # --- LAYOUT PRINCIPAL (MAPA À DIREITA) ---
    col_lateral, col_mapa = st.columns([1, 2])

    with col_lateral:
        st.subheader("🏢 Fornecedores")
        df_f = df.groupby('FORNECEDOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS')
        fig_f = px.bar(df_f, x='QTOS LTS', y='FORNECEDOR', orientation='h', 
                       text_auto=True, color_discrete_sequence=['#3498db'])
        fig_f.update_layout(height=300, margin=dict(t=0, b=0))
        st.plotly_chart(fig_f, use_container_width=True)

        st.subheader("🚢 Empurradores")
        df_emp_pie = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index()
        fig_pie = px.pie(df_emp_pie, values='QTOS LTS', names='EMPURRADOR', hole=0.5)
        fig_pie.update_layout(height=250, margin=dict(t=0, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_mapa:
        st.subheader("📍 Cobertura por Estado (UF)")
        df_uf = df.groupby('ESTADO')['QTOS LTS'].sum().reset_index()
        # Mapa Coroplético que funciona sem Lat/Long
        fig_mapa = px.choropleth(df_uf,
                                locations='ESTADO',
                                locationmode='BRA-states',
                                color='QTOS LTS',
                                color_continuous_scale="Blues",
                                scope='south america',
                                labels={'QTOS LTS':'Litros'})
        fig_mapa.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_mapa, use_container_width=True)

    # --- GRÁFICO FINAL ---
    st.markdown("---")
    st.subheader("📊 Volume Detalhado por Empurrador")
    df_emp_bar = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
    fig_bar = px.bar(df_emp_bar, x='EMPURRADOR', y='QTOS LTS', text_auto=True, color_discrete_sequence=['#1a4d80'])
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.error("Erro ao ler dados da planilha. Verifique as colunas.")

# Refresh Automático (30 segundos)
st.markdown("""<script>setTimeout(function(){ window.location.reload(); }, 30000);</script>""", unsafe_allow_html=True)
