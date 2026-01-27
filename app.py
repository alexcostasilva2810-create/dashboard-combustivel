import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Limpeza de cache para atualização em tempo real
st.cache_data.clear()

st.set_page_config(page_title="ZION MINITORAMENTO", layout="wide")

# --- CSS: DESIGN CLARO COM NÚMEROS GRANDES (30px) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    div[data-testid="stMetricValue"] { 
        font-size: 35px !important; 
        font-weight: bold !important; 
        color: #1e40af !important; 
    }
    .main-title { color: #1e3a8a; font-weight: bold; text-align: center; font-size: 32px; }
    </style>
    """, unsafe_allow_html=True)

# Horário de Brasília
fuso_br = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(fuso_br).strftime('%d/%m/%Y %H:%M:%S')

ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    st.markdown(f'<p class="main-title">⚓ DASHBOARD DE ABASTECIMENTO NAVAL</p>', unsafe_allow_html=True)
    st.write(f"⏱️ **Sincronizado em:** {agora}")

    # --- KPIs ---
    c1, c2, c3, c4 = st.columns(4)
    # Formatação para exibir números inteiros sem 'k'
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Abastecimentos", f"{len(df)}")
    c3.metric("Cidades", f"{df['LOCAL'].nunique()}")
    c4.metric("Fornecedores", f"{df['FORNECEDOR'].nunique()}")

    st.markdown("---")

    # --- MAPA DE ALTA NITIDEZ (MAPBOX) ---
    st.subheader("📍 Localização Exata dos Abastecimentos")
    
    # Criando o mapa com estilo 'open-street-map' que é muito mais nítido
    # Se você tiver Latitude e Longitude na planilha, substitua 'LOCAL' por elas abaixo.
    # Caso contrário, o Plotly usará os nomes das cidades/estados.
    
    fig_mapa = px.scatter_mapbox(df, 
                                lat=None, lon=None, # Caso tenha coordenadas, use aqui
                                color="LOCAL", 
                                size="QTOS LTS",
                                hover_name="LOCAL",
                                hover_data=["EMPURRADOR", "QTOS LTS", "FORNECEDOR"],
                                zoom=4, 
                                height=600)

    # Estilo do mapa: 'carto-positron' (Claro e nítido) ou 'open-street-map'
    fig_mapa.update_layout(
        mapbox_style="open-street-map", 
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend=True
    )
    
    # Tenta centralizar o mapa no Brasil/Região Norte se não houver coordenadas
    fig_mapa.update_layout(mapbox_center={"lat": -3.11, "lon": -60.02}) # Foco inicial próximo a Manaus/Belém

    st.plotly_chart(fig_mapa, use_container_width=True)

    # --- RANKING DE FORNECEDORES ---
    st.markdown("---")
    st.subheader("🏢 Ranking de Compras por Fornecedor")
    df_forn = df.groupby('FORNECEDOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=True)
    
    fig_forn = px.bar(df_forn, x='QTOS LTS', y='FORNECEDOR', orientation='h',
                      text_auto=True, color='QTOS LTS', 
                      color_continuous_scale='Blues')
    
    fig_forn.update_layout(xaxis_title="Total de Litros", yaxis_title="Fornecedor")
    st.plotly_chart(fig_forn, use_container_width=True)

except Exception as e:
    st.error(f"Erro na conexão: {e}")

# Atualização automática
st.markdown("<script>setTimeout(function(){window.location.reload();}, 60000);</script>", unsafe_allow_html=True)
