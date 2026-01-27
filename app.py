import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz

# Forçar atualização (Sem Cache)
st.cache_data.clear()

st.set_page_config(page_title="Dashboard Naval PRO", layout="wide")

# --- CONFIGURAÇÃO DE HORÁRIO BRASILEIRO ---
fuso_br = pytz.timezone('America/Sao_Paulo')
horario_atual = datetime.now(fuso_br).strftime('%d/%m/%Y %H:%M:%S')

# --- ESTILO POWER BI (AZUL ROYAL + CIANO) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #001f3f 0%, #000a1a 100%); color: white; }
    [data-testid="stMetricValue"] { font-size: 30px !important; font-weight: bold !important; color: #00f2ff !important; }
    .stPlotlyChart { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # --- TÍTULO E RELÓGIO ---
    st.title("⚓ MONITORAMENTO DE FROTA (ESTILO BI)")
    st.markdown(f"🕒 **Horário de Brasília:** {horario_atual}")

    # --- KPIs ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{df['QTOS LTS'].sum():,.0f}")
    c2.metric("Abastecimentos", f"{len(df)}")
    c3.metric("Principais Fornecedores", df['FORNECEDOR'].nunique())
    c4.metric("Localidades Atendidas", df['LOCAL'].nunique())

    st.markdown("---")

    # --- MAPA E FORNECEDORES ---
    col_mapa, col_forn = st.columns([6, 4])

    with col_mapa:
        st.subheader("📍 Mapa de Distribuição Geográfica")
        # Usando gráfico de dispersão geográfico para simular mapa de calor
        fig_mapa = px.scatter_geo(df, 
                                 locations="ESTADO", 
                                 locationmode='country names', # Ajuste para cidades se tiver lat/long
                                 size="QTOS LTS", 
                                 hover_name="LOCAL",
                                 color="EMPURRADOR",
                                 projection="natural earth",
                                 template="plotly_dark")
        fig_mapa.update_geos(scope='south america', showcountries=True)
        fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_mapa, use_container_width=True)

    with col_forn:
        st.subheader("🏢 Ranking de Fornecedores (Compras)")
        df_forn = df.groupby('FORNECEDOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
        fig_forn = px.bar(df_forn, y='FORNECEDOR', x='QTOS LTS', orientation='h',
                          color='QTOS LTS', color_continuous_scale='Blues',
                          text_auto='.2s')
        fig_forn.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_forn, use_container_width=True)

    # --- ANÁLISE POR EMPURRADOR ---
    st.markdown("---")
    st.subheader("📊 Performance por Empurrador (LTS vs QTD)")
    resumo_emp = df.groupby('EMPURRADOR').agg({'QTOS LTS': 'sum', 'EMPURRADOR': 'count'}).rename(columns={'EMPURRADOR': 'QTD'}).reset_index()
    
    fig_mix = go.Figure()
    fig_mix.add_trace(go.Bar(x=resumo_emp['EMPURRADOR'], y=resumo_emp['QTOS LTS'], name='Volume Litros', marker_color='#0077ff'))
    fig_mix.add_trace(go.Scatter(x=resumo_emp['EMPURRADOR'], y=resumo_emp['QTD'], name='Qtd Vezes', yaxis='y2', mode='lines+markers', line=dict(color='#00f2ff', width=3)))
    
    fig_mix.update_layout(yaxis=dict(title="Litros"), yaxis2=dict(title="Qtd Vezes", overlaying='y', side='right'),
                          template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_mix, use_container_width=True)

except Exception as e:
    st.error(f"Erro: {e}. Verifique se a planilha está pública!")

# Auto-refresh de 60 segundos
st.markdown("<script>setTimeout(function(){window.location.reload();}, 60000);</script>", unsafe_allow_html=True)
