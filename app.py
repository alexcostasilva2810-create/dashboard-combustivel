import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mapa de Abastecimento", layout="wide")

ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

st.title("📍 Mapa de Localização de Abastecimentos")

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()

    # --- LÓGICA DO MAPA ---
    # Contamos quantas vezes cada LOCAL aparece
    df_mapa = df.groupby(['LOCAL', 'ESTADO']).size().reset_index(name='Frequência')

    st.subheader("Frequência por Localidade")
    
    # Criando o mapa (usando as coordenadas aproximadas pelo nome do local)
    # Nota: Para precisão total, seriam necessárias colunas de Latitude e Longitude
    fig_mapa = px.scatter_geo(df_mapa, 
                             locations="ESTADO", 
                             locationmode="USA-states", # Ou usar 'country names' se for Brasil
                             hover_name="LOCAL", 
                             size="Frequência",
                             projection="natural earth",
                             title="Onde ocorrem os abastecimentos")
    
    st.plotly_chart(fig_mapa, use_container_width=True)

    # --- TABELA DE RESUMO ---
    st.write("Contagem por Localidade:")
    st.dataframe(df_mapa.sort_values(by='Frequência', ascending=False))

except Exception as e:
    st.error(f"Erro ao gerar o mapa: {e}")
