import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz

# Forçar atualização e limpar memória
st.cache_data.clear()

st.set_page_config(page_title="Gestão de Frota Naval", layout="wide")

# --- DESIGN CLARO E MODERNO (ESTILO POWER BI LIGHT) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f4f8;
        color: #1e3a8a;
    }
    /* Estilização dos Cards Brancos */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #0077ff;
    }
    /* Números: 30px, Negrito, Azul Escuro */
    div[data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: bold !important;
        color: #1e3a8a !important;
    }
    h1, h2, h3 { color: #1e3a8a !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Configuração de Horário de Brasília
fuso_br = pytz.timezone('America/Sao_Paulo')
horario_br = datetime.now(fuso_br).strftime('%d/%m/%Y %H:%M:%S')

ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    # Converte para número e garante que não use abreviação (k)
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    st.title("⚓ MONITORAMENTO GEOGRÁFICO DE FROTA")
    st.markdown(f"🕒 **Horário de Brasília:** {horario_br}")

    # --- LINHA 1: KPIs (VALORES INTEIROS) ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Total Abastecimentos", f"{len(df)}")
    c3.metric("Principais Fornecedores", f"{df['FORNECEDOR'].nunique()}")
    c4.metric("Localidades", f"{df['LOCAL'].nunique()}")

    st.markdown("---")

    # --- LINHA 2: MAPA COLORIDO E INTERATIVO ---
    st.subheader("📍 Mapa de Calor e Localização")
    # Mapa focado na Região Norte/Brasil com cores vibrantes
    fig_mapa = px.scatter_geo(df, 
                             locations="ESTADO", 
                             locationmode='country names',
                             color="LOCAL", # Cores diferentes por cidade
                             size="QTOS LTS", 
                             hover_name="LOCAL",
                             hover_data={"QTOS LTS": True, "EMPURRADOR": True, "ESTADO": False},
                             projection="mercator",
                             color_discrete_sequence=px.colors.qualitative.Bold)

    fig_mapa.update_geos(
        scope='south america',
        showland=True, landcolor="#e5ecf6",
        showocean=True, oceancolor="#cde4ff",
        showlakes=True, lakecolor="#cde4ff",
        fitbounds="locations"
    )
    fig_mapa.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_mapa, use_container_width=True)

    # --- LINHA 3: FORNECEDORES E RANKING ---
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🏢 Compras por Fornecedor")
        df_forn = df.groupby('FORNECEDOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS')
        fig_forn = px.bar(df_forn, x='QTOS LTS', y='FORNECEDOR', orientation='h',
                          text_auto='.0f', # Mostra o número inteiro na barra
                          color='QTOS LTS', color_continuous_scale='Blues')
        st.plotly_chart(fig_forn, use_container_width=True)

    with col_b:
        st.subheader("🚢 Volume por Empurrador")
        df_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index()
        fig_emp = px.pie(df_emp, values='QTOS LTS', names='EMPURRADOR', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_emp, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")

# Refresh automático para monitoramento em tempo real
st.markdown("<script>setTimeout(function(){window.location.reload();}, 60000);</script>", unsafe_allow_html=True)
