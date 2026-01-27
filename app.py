import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Fiscal", layout="wide")

# Conexão com os dados
ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

st.title("📊 Painel de Controle - Gestão de Combustível")
st.markdown("---")

try:
    df = pd.read_csv(URL)

    # --- LINHA 1: KPIs (Números Grandes) ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Pedidos", len(df))
    col2.metric("Total de Litros", f"{df['QTOS LTS'].sum():,.0f}")
    col3.metric("Média por Abastecimento", f"{df['QTOS LTS'].mean():,.2f}")

    st.markdown("---")

    # --- LINHA 2: GRÁFICOS ---
    graf_col1, graf_col2 = st.columns(2)

    with graf_col1:
        st.subheader("Volume por Empurrador")
        fig_barras = px.bar(df, x="EMPURRADOR", y="QTOS LTS", color="EMPURRADOR", 
                            title="Litros por Empurrador")
        st.plotly_chart(fig_barras, use_container_width=True)

    with graf_col2:
        st.subheader("Distribuição por Estado")
        fig_pizza = px.pie(df, values="QTOS LTS", names="ESTADO", 
                           title="Consumo por Estado", hole=0.4)
        st.plotly_chart(fig_pizza, use_container_width=True)

except Exception as e:
    st.error("Erro ao carregar gráficos. Verifique se as colunas 'QTOS LTS', 'EMPURRADOR' e 'ESTADO' estão escritas corretamente na planilha.")
